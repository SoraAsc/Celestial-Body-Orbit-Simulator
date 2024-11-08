import pygame
import numpy as np

from celestial_body import CelestialBody

# Pygame Initialization
pygame.init()
running = True
SCREEN_SIZE = np.array([600.0, 600.0])
screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
pygame.display.set_caption("Orbit Simulation")

# Constants
G = 6.67430e-11             # Gravitational constant
DELTA_T = 800000            # Time interval (adjusted for display)
SCALE = 3e9                 # Scale to convert meters into pixels (adjusted to reduce values)
CENTER = SCREEN_SIZE / 2    # Screen center in pixels

earth = CelestialBody("Terra", 0.0, np.array([2, 3]), np.array([2,3]))
print(earth)

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

pygame.quit()