import numpy as np

from celestial_body import CelestialBody

class Integrator():
    """The Integrator class contains the methods for the integration algorithms that update the position and velocity of the bodies"""

    def __init__(self, method: str = "RK4", derivative_function = None):
        """Initialize the Integrator

        Args:
            method (str, optional): The name of the method to be selected (RK4 | Euler). Defaults to "RK4".
            derivative_function (Function, optional): The function that will be used in the integrator. Defaults to None.
        """
        
        self.choose_method(method)
        self.derivative_function = derivative_function

    def choose_method(self, method: str = "RK4"):
        """Choose the integration method

        Args:
            method (str, optional): The name of the method to be selected. Defaults to "RK4".
        """

        self.method = method
        if self.method == "RK4":
            self.method_implementation = self.rk4_step
        else: 
            self.method_implementation = self.euler_step

    def integrate(self, body, delta_t):
        self.method_implementation(body, delta_t)

    def euler_step(self, body: CelestialBody, delta_t: np.double):
        """Calculate and update the position and velocity of the body using Euler Method

        Args:
            body (CelestialBody): The body that will be updated
            delta_t (np.double): The time steps
        """

        velocity, acceleration = self.derivative_function(body, 0, body.position, body.velocity)
        body.position += velocity * delta_t
        body.velocity += acceleration * delta_t

    def rk4_step(self, body: CelestialBody, delta_t: np.double):
        """Calculate the k-values and update the position and velocity of the body using RK4 method

        Args:
            body (CelestialBody): The body that will be updated
            delta_t (np.double): The time steps
        """

        # Initial State
        t = 0 # In this simulation, I'm not taking time into consideration
        initial_position = np.copy(body.position)
        initial_velocity = np.copy(body.velocity)
        
        # k1
        k1_vel, k1_acc = self.derivative_function(body, t, initial_position, initial_velocity)

        # k2: halfway step
        k2_vel, k2_acc = self.derivative_function(
            body, t + 0.5 * delta_t,
            initial_position + 0.5 * delta_t * k1_vel,
            initial_velocity + 0.5 * delta_t * k1_acc
        )

        # k3: another halfway step
        k3_vel, k3_acc = self.derivative_function(
            body, t + 0.5 * delta_t,
            initial_position + 0.5 * delta_t * k2_vel,
            initial_velocity + 0.5 * delta_t * k2_acc
        )

        # k4: full step
        k4_vel, k4_acc = self.derivative_function(
            body, t + delta_t,
            initial_position + delta_t * k3_vel,
            initial_velocity + delta_t * k3_acc
        )

        # Update position and velocity using the RK4 weighted average
        body.position += (delta_t / 6) * (k1_vel + 2 * k2_vel + 2 * k3_vel + k4_vel)
        body.velocity += (delta_t / 6) * (k1_acc + 2 * k2_acc + 2 * k3_acc + k4_acc)



