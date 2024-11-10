import numpy as np

# Constants
WORLD_SIZE = np.array([8000, 8000])
SCREEN_SIZE = np.array([600.0, 600.0])
CENTER = SCREEN_SIZE // 2    # Screen center in pixels
G = 6.67430e-11             # Gravitational constant
DELTA_T = 200000            # Time interval (adjusted for display)
SCALE = 12e8                 # Scale to convert meters into pixels (adjusted to reduce values)