import matplotlib.pyplot as plt
import numpy as np

# from core.celestial_body import CelestialBody

class Visualization:
    """Class containing all the plot/chart generation functions"""

    def plot_orbital_trajectories(self, bodies):
        plt.figure(figsize=(8, 8))
        
        for body in bodies:
            trails = np.array(body.trails_pos)  # Convert trails_pos to a numpy array for easier plotting
            if trails.shape[0] > 0:  # Ensure there are positions to plot
                normalized_color = normalize_color(body.color)
                plt.plot(trails[:, 0], trails[:, 1], color=normalized_color, label=body.name)
                plt.scatter(trails[-1, 0], trails[-1, 1], color=normalized_color, marker="o", s=50)  # Current position

        plt.xlabel("X Position (m)")
        plt.ylabel("Y Position (m)")
        plt.title("Orbital Trajectories")
        plt.legend(loc="upper right")
        plt.grid(True)
        plt.axis("equal")
        plt.show()

def normalize_color(color):
    return tuple(c / 255 for c in color)

