from typing import Tuple
from numpy import double, ndarray
import numpy as np
from celestial_body import CelestialBody
from config import G
from integrator import Integrator

class Simulation:
    """Class responsible for handling the simulation and the calculations involving it"""

    def __init__(self, bodies: list[CelestialBody], delta_t: double = 60, method: str = "RK4"):
        """Initialize the Simulation

        Args:
            bodies (list[CelestialBody]): All the bodies on the simulation
            delta_t (double, optional): Time steps (how much each iteration advance in time). Defaults to 60.
            method (str, optional): The name of the method to be selected (RK4 | Euler). Defaults to "RK4".
        """

        self.bodies = bodies
        self.delta_t = delta_t
        self.method = method
        self.integrator = Integrator(method, self.f)

    def f(self, body: CelestialBody, t: double, position: ndarray, velocity: ndarray) -> Tuple[ndarray, ndarray]:
        """Calculate the derivatives (velocity and acceleration) for a given body at a given time and state.

        Args:
            body (CelestialBody): The body that will be calculated
            t (double): The timestep
            position (ndarray): The current position of the body
            velocity (ndarray): The current velocity of the body

        Returns:
            Tuple[ndarray, ndarray]: A tuple (velocity, acceleration) containing the deri vatives of the body
        """

        acceleration = np.zeros(2)

        # Calculate the gravitational force from other bodies
        for other_body in self.bodies:
            if other_body != body:
                distance_vector = other_body.position - position
                distance = np.linalg.norm(distance_vector)
                if distance > 0:
                    force_magnitude = G * body.mass * other_body.mass / distance ** 2
                    force_vector = force_magnitude * (distance_vector / distance) # Normalize
                    acceleration += force_vector / body.mass

        # Return the derivative of position (velocity) and the derivative of velocity (acceleration)
        return velocity, acceleration

    def run(self):
        for body in self.bodies:
            self.integrator.integrate(body, self.delta_t)
