import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600
NUM_BOIDS = 100
BOID_RADIUS = 3
MAX_SPEED = 3
MAX_FORCE = 0.1
NEIGHBOR_DIST = 50

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

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), BOID_RADIUS)

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    boids = [Boid(Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT))) for _ in range(NUM_BOIDS)]

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for boid in boids:
            separation_force = separation(boid, boids)
            alignment_force = alignment(boid, boids)
            cohesion_force = cohesion(boid, boids)

            boid.apply_force(separation_force + alignment_force + cohesion_force)
            boid.update()
            boid.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
