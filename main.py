import pygame
import numpy as np

from celestial_body import CelestialBody
from config import SCREEN_SIZE

# Pygame Initialization
pygame.init()
running = True
screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
pygame.display.set_caption("Orbit Simulation")

earth = CelestialBody("Terra", 0.0, np.array([2, 3]), np.array([2,3]))
print(earth)

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

pygame.quit()