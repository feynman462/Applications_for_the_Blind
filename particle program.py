import random
from math import sqrt

class Particle:
    def __init__(self, x, y, vx, vy, mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def update_velocity(self, ax, ay, dt):
        self.vx += ax * dt
        self.vy += ay * dt

def generate_particles(num_particles):
    particles = []
    for _ in range(num_particles):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        vx = random.uniform(-1, 1)
        vy = random.uniform(-1, 1)
        mass = random.uniform(1, 10)
        particles.append(Particle(x, y, vx, vy, mass))
    return particles

def distance(p1, p2):
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def simulate(particles, time_steps, dt, boundary):
    for _ in range(time_steps):
        for i, p1 in enumerate(particles):
            ax, ay = 0, 0
            for p2 in particles:
                if p1 is not p2:
                    d = distance(p1, p2)
                    force = p1.mass * p2.mass / (d ** 2)
                    direction_x = (p2.x - p1.x) / d
                    direction_y = (p2.y - p1.y) / d
                    ax += force * direction_x / p1.mass
                    ay += force * direction_y / p1.mass

            p1.update_velocity(ax, ay, dt)
            p1.update_position(dt)

            # Boundary conditions
            if p1.x < 0 or p1.x > boundary:
                p1.vx = -p1.vx
            if p1.y < 0 or p1.y > boundary:
                p1.vy = -p1.vy

def print_particle_data(particles):
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles[i + 1:], i + 1):
            dist = distance(p1, p2)
            print(f"Distance between particle {i + 1} and particle {j + 1}: {dist:.2f} units")

num_particles = int(input("Enter the number of particles: "))
time_steps = int(input("Enter the number of time steps: "))
dt = float(input("Enter the time step size (e.g., 0.1 for small steps): "))
boundary = float(input("Enter the boundary size (e.g., 100 for a 100x100 square): "))

particles = generate_particles(num_particles)
simulate(particles, time_steps, dt, boundary)
print_particle_data(particles)
