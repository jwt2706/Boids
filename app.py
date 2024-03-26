from flask import Flask, render_template
from boids import Boid, Vector, MAX_SPEED, WIDTH, HEIGHT, BOID_RADIUS, NEIGHBOR_DIST, MAX_FORCE

app = Flask(__name__)

@app.route('/')
def home():
    position = Vector(WIDTH / 2, HEIGHT / 2)
    boid = Boid(position)
    boid.update()
    return render_template('index.html', boid_position=boid.position)

if __name__ == '__main__':
    app.run(debug=False)