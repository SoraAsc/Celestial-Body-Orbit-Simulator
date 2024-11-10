from typing import Optional, Tuple
from numpy import double, ndarray
import numpy as np
import random

# Keep track of used colors to avoid duplicates
used_colors = set()

class CelestialBody:
    """Class that contains all the information and details of celestial bodies (Planets, Stars, Satellites, etc.)"""
    
    def __init__(self, name: str, mass: double, position: ndarray, velocity: ndarray, color: Optional[Tuple[int, int, int]] = None):
        """Initialize the celestial body

        Args:
            name (str): The Celestial Body name
            mass (double): The mass of the celestial body
            position (ndarray): The initial position of the body
            velocity (ndarray): The initial velocity of the body
            color (Optional[Tuple[int, int, int]], optional): The color, if not provided is a random color. Defaults to None.
        """

        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = np.zeros(position.shape)
        self.color = color if color is not None else self.generate_unique_color()
        self.trails_pos = []

    def update_trail(self, trail_limit: int):
        """Update the trails list, insert a new position and remove if is beyond the limit

        Args:
            trail_limit (int): The number of trails that the body can have
        """

        self.trails_pos.append((self.position[0], self.position[1]))
        if len(self.trails_pos) > trail_limit:
            self.trails_pos.pop(0)

    def generate_unique_color(self) -> Tuple[int, int, int]:
        """Generate a unique RGB color that hasn't been used yet

        Returns:
            color (Tuple[int, int, int]): The RGB color as a tuple (0...255, 0...255, 0...255)
        """

        while True:
            # Generate a random color
            new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if new_color not in used_colors:
                # Add the color to the used set and return it
                used_colors.add(new_color)
                return new_color
            
    def __str__(self):
        """String representation of the object

        Returns:
            str: The description of the object
        """
        
        return f"CelestialBody(name={self.name}, mass={self.mass}, position={self.position}, velocity={self.velocity}, color={self.color})"