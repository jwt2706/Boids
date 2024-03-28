const NUMBER_OF_BOIDS = 100;

class Boid {
  constructor(p) {
    this.p = p; // p5 instance
    // init in a random position in the canvas
    this.position = this.p.createVector(
      this.p.random(this.p.width),
      this.p.random(this.p.height)
    );
    this.velocity = p5.Vector.random2D();
    this.acceleration = this.p.createVector();
    this.maxForce = 0.2;
    this.maxSpeed = 4;
  }

  // make boids wrap around the canvas
  edges() {
    if (this.position.x > this.p.width) {
      this.position.x = 0;
    } else if (this.position.x < 0) {
      this.position.x = this.p.width;
    }
    if (this.position.y > this.p.height) {
      this.position.y = 0;
    } else if (this.position.y < 0) {
      this.position.y = this.p.height;
    }
  }

  // align boid with nearby boids
  align(boids) {
    let perceptionRadius = 50;
    let steering = this.p.createVector();
    let total = 0;
    for (let other of boids) {
      let d = this.p.dist(
        this.position.x,
        this.position.y,
        other.position.x,
        other.position.y
      );
      if (other != this && d < perceptionRadius) {
        steering.add(other.velocity);
        total++;
      }
    }
    if (total > 0) {
      steering.div(total);
      steering.setMag(this.maxSpeed);
      steering.sub(this.velocity);
      steering.limit(this.maxForce);
    }
    return steering;
  }

  // steer boid towards the average position of nearby boids
  cohesion(boids) {
    let perceptionRadius = 50;
    let steering = this.p.createVector();
    let total = 0;
    for (let other of boids) {
      let d = this.p.dist(
        this.position.x,
        this.position.y,
        other.position.x,
        other.position.y
      );
      if (other != this && d < perceptionRadius) {
        steering.add(other.position);
        total++;
      }
    }
    if (total > 0) {
      steering.div(total);
      steering.sub(this.position);
      steering.setMag(this.maxSpeed);
      steering.sub(this.velocity);
      steering.limit(this.maxForce);
    }
    return steering;
  }

  // steer boid away from nearby boids to prevent collisions and crowding other boids
  separation(boids) {
    let perceptionRadius = 50;
    let steering = this.p.createVector();
    let total = 0;
    for (let other of boids) {
      let d = this.p.dist(
        this.position.x,
        this.position.y,
        other.position.x,
        other.position.y
      );
      if (other != this && d < perceptionRadius) {
        let diff = p5.Vector.sub(this.position, other.position);
        diff.div(d * d);
        steering.add(diff);
        total++;
      }
    }
    if (total > 0) {
      steering.div(total);
      steering.setMag(this.maxSpeed);
      steering.sub(this.velocity);
      steering.limit(this.maxForce);
    }
    return steering;
  }

  // using align, cohesion and separation to make the magic happen
  flock(boids) {
    this.acceleration.add(this.align(boids));
    this.acceleration.add(this.cohesion(boids));
    this.acceleration.add(this.separation(boids));
  }

  // update position, velocity and acceleration
  update() {
    this.position.add(this.velocity);
    this.velocity.add(this.acceleration);
    this.velocity.limit(this.maxSpeed);
    this.acceleration.mult(0);
  }

  // draw boid
  show() {
    this.p.stroke(255);
    this.p.fill(255);
    this.p.push();
    this.p.translate(this.position.x, this.position.y);
    this.p.rotate(this.velocity.heading() + this.p.PI / 2);
    this.p.beginShape();
    this.p.vertex(0, -8); // top point
    this.p.vertex(-5, 5); // bottom left point
    this.p.vertex(5, 5); // bottom right point
    this.p.endShape(this.p.CLOSE);
    this.p.pop();
  }
}

// p5 sketch
const sim = (p) => {
  const flock = [];

  p.setup = () => {
    p.createCanvas(p.windowWidth, p.windowHeight);
    // spawn boids
    for (let i = 0; i < NUMBER_OF_BOIDS; i++) {
      flock.push(new Boid(p));
    }
  };

  p.draw = () => {
    p.background(0);
    for (let boid of flock) {
      boid.edges();
      boid.flock(flock);
      boid.update();
      boid.show();
    }
  };
};

new p5(sim);
