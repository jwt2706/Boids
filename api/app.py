from http.server import BaseHTTPRequestHandler
from boids import Boid, Vector, MAX_SPEED, WIDTH, HEIGHT, BOID_RADIUS, NEIGHBOR_DIST, MAX_FORCE
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        position = Vector(WIDTH / 2, HEIGHT / 2)
        boid = Boid(position)
        boid.update()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'boid_position': {'x': boid.position.x, 'y': boid.position.y}}).encode())
        return