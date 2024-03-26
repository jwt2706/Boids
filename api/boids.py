from http.server import BaseHTTPRequestHandler
import json
import random
import math

WIDTH, HEIGHT = 800, 600
NUM_BOIDS = 100
BOID_RADIUS = 3
MAX_SPEED = 3
MAX_FORCE = 0.1
NEIGHBOR_DIST = 50

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # create a boid and apply alignment force
        position = Vector(WIDTH / 2, HEIGHT / 2)
        boid = Boid(position)
        boids = [Boid(Vector(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))) for _ in range(100)]
        alignment_force = alignment(boid, boids)
        boid.apply_force(alignment_force)
        boid.update()

        # send boid position as JSON response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'boid_position': {'x': boid.position.x, 'y': boid.position.y}}).encode())
        return

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    def normalize(self):
        magnitude = self.magnitude()
        if magnitude == 0:
            return Vector(0, 0)
        return self * (1 / magnitude)

class Boid:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector(random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))

    def apply_force(self, force):
        self.velocity += force
        self.velocity.x = max(-MAX_SPEED, min(MAX_SPEED, self.velocity.x))
        self.velocity.y = max(-MAX_SPEED, min(MAX_SPEED, self.velocity.y))

    def update(self):
        self.position += self.velocity
        self.position.x = self.position.x % WIDTH
        self.position.y = self.position.y % HEIGHT

def separation(boid, boids):
    steering = Vector(0, 0)
    count = 0
    for other in boids:
        if boid == other:
            continue
        dist = (boid.position - other.position).magnitude()
        if dist < NEIGHBOR_DIST:
            steering += (boid.position - other.position) * (1 / dist ** 2)
            count += 1
    if count > 0:
        steering *= (1 / count)
        steering = steering.normalize() * MAX_SPEED - boid.velocity
        steering.x = max(-MAX_FORCE, min(MAX_FORCE, steering.x))
        steering.y = max(-MAX_FORCE, min(MAX_FORCE, steering.y))
    return steering

def alignment(boid, boids):
    steering = Vector(0, 0)
    count = 0
    for other in boids:
        if boid == other:
            continue
        dist = (boid.position - other.position).magnitude()
        if dist < NEIGHBOR_DIST:
            steering += other.velocity
            count += 1
    if count > 0:
        steering *= (1 / count)
        steering = steering.normalize() * MAX_SPEED - boid.velocity
        steering.x = max(-MAX_FORCE, min(MAX_FORCE, steering.x))
        steering.y = max(-MAX_FORCE, min(MAX_FORCE, steering.y))
    return steering

def cohesion(boid, boids):
    steering = Vector(0, 0)
    count = 0
    for other in boids:
        if boid == other:
            continue
        dist = (boid.position - other.position).magnitude()
        if dist < NEIGHBOR_DIST:
            steering += other.position
            count += 1
    if count > 0:
        steering *= (1 / count)
        steering = (steering - boid.position).normalize() * MAX_SPEED - boid.velocity
        steering.x = max(-MAX_FORCE, min(MAX_FORCE, steering.x))
        steering.y = max(-MAX_FORCE, min(MAX_FORCE, steering.y))
    return steering