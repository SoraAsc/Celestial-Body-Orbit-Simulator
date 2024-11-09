import numpy as np
from celestial_body import CelestialBody
from config import DELTA_T
from pygame_manager import PygameManager
from simulation import Simulation


sun = CelestialBody("Sun", 1.989e30, np.array([0.0, 0.0], dtype=np.float64), np.array([0.0, 0.0]), (255, 255, 255))
earth = CelestialBody("Earth", 5.972e24, np.array([1.496e11, 0.0], dtype=np.float64), np.array([0.0, 29780.0], dtype=np.float64), (0, 0, 255))
jupiter = CelestialBody("Jupiter", 5.972e24, np.array([0.0, 7.785e11], dtype=np.float64), np.array([-13070.0, 0.0], dtype=np.float64), (226, 84, 33))

bodies = [sun, earth, jupiter]
sim = Simulation(bodies, DELTA_T)
pygame_manager = PygameManager(sim)
pygame_manager.run()