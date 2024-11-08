from numpy import double
from celestial_body import CelestialBody

class Simulation:
    def __init__(self, bodies: list[CelestialBody], delta_t: double, method: str):
        """docstring"""
        self.bodies = bodies
        self.delta_t = delta_t
        self.method = method