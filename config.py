import numpy as np

# Constants
WORLD_SIZE = np.array([2000, 2000])
SCREEN_SIZE = np.array([600.0, 600.0])
CENTER = SCREEN_SIZE // 2    # Screen center in pixels
G = 6.67430e-11             # Gravitational constant
DELTA_T = 800000            # Time interval (adjusted for display)
SCALE = 3e9                 # Scale to convert meters into pixels (adjusted to reduce values)