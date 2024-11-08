from numpy import double, ndarray
import numpy as np

class CelestialBody:
    def __init__(self, name: str, mass: double, position: ndarray, velocity: ndarray):
        """Initialize the celestial body"""
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = np.zeros(position.shape)