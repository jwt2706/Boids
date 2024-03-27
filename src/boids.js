class Boid {
    constructor() {
      this.position = createVector(random(width), random(height));
      this.velocity = p5.Vector.random2D();
      this.acceleration = createVector();
      this.maxForce = 0.2;
      this.maxSpeed = 4;
    }
  
    edges() {
      if (this.position.x > width) {
        this.position.x = 0;
      } else if (this.position.x < 0) {
        this.position.x = width;
      }
      if (this.position.y > height) {
        this.position.y = 0;
      } else if (this.position.y < 0) {
        this.position.y = height;
      }
    }
  
    align(boids) {
      let perceptionRadius = 50;
      let steering = createVector();
      let total = 0;
      for (let other of boids) {
        let d = dist(this.position.x, this.position.y, other.position.x, other.position.y);
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
  
    cohesion(boids) {
      let perceptionRadius = 50;
      let steering = createVector();
      let total = 0;
      for (let other of boids) {
        let d = dist(this.position.x, this.position.y, other.position.x, other.position.y);
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
  
    separation(boids) {
      let perceptionRadius = 50;
      let steering = createVector();
      let total = 0;
      for (let other of boids) {
        let d = dist(this.position.x, this.position.y, other.position.x, other.position.y);
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
  
    flock(boids) {
      this.acceleration.add(this.align(boids));
      this.acceleration.add(this.cohesion(boids));
      this.acceleration.add(this.separation(boids));
    }
  
    update() {
      this.position.add(this.velocity);
      this.velocity.add(this.acceleration);
      this.velocity.limit(this.maxSpeed);
      this.acceleration.mult(0);
    }
  
    show() {
      strokeWeight(8);
      stroke(255);
      point(this.position.x, this.position.y);
    }
  }
  
  const flock = [];
  
  function setup() {
    createCanvas(640, 360);
    for (let i = 0; i < 100; i++) {
      flock.push(new Boid());
    }
  }
  
  function draw() {
    background(51);
    for (let boid of flock) {
      boid.edges();
      boid.flock(flock);
      boid.update();
      boid.show();
    }
  }