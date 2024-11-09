from numpy import double
from celestial_body import CelestialBody

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