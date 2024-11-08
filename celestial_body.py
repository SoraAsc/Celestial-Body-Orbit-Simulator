from typing import Optional, Tuple
from numpy import double, ndarray
import numpy as np
import random

# Keep track of used colors to avoid duplicates
used_colors = set()

class CelestialBody:
    def __init__(self, name: str, mass: double, position: ndarray, velocity: ndarray, color: Optional[Tuple[int, int, int]] = None):
        """Initialize the celestial body"""
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = np.zeros(position.shape)
        self.color = color if color is not None else self.generate_unique_color()

    def generate_unique_color(self) -> Tuple[int, int, int]:
        """Generate a unique RGB color that hasn't been used yet"""
        while True:
            # Generate a random color
            new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if new_color not in used_colors:
                # Add the color to the used set and return it
                used_colors.add(new_color)
                return new_color
            
    def __str__(self):
        """String representation of the object"""
        return f"CelestialBody(name={self.name}, mass={self.mass}, position={self.position}, velocity={self.velocity}, color={self.color})"