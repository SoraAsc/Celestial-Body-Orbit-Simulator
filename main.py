import pygame
import numpy as np

from celestial_body import CelestialBody
from config import CENTER, DELTA_T, SCALE, SCREEN_SIZE
from simulation import Simulation

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
pygame.display.set_caption("Orbit Simulation")
clock = pygame.time.Clock()

running = True

sun = CelestialBody("Sun", 1.989e30, np.array([0.0, 0.0], dtype=np.float64), np.array([0.0, 0.0]), (255, 255, 255))
earth = CelestialBody("Earth", 5.972e24, np.array([1.496e11, 0.0], dtype=np.float64), np.array([0.0, 29780.0], dtype=np.float64), (0, 0, 255))
jupiter = CelestialBody("Jupiter", 5.972e24, np.array([0.0, 7.785e11], dtype=np.float64), np.array([-13070.0, 0.0], dtype=np.float64), (226, 84, 33))

bodies = [sun, earth, jupiter]
sim = Simulation(bodies, DELTA_T)



def draw_bodies():
    screen.fill((0, 0, 0))  # Limpa a tela

    for body in sim.bodies:
        x = int(body.position[0] / SCALE + CENTER[0])
        y = int(body.position[1] / SCALE + CENTER[1])
        pygame.draw.circle(screen, body.color, (x, y), 8)
    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sim.run()
    draw_bodies()
    clock.tick(60)

pygame.quit()