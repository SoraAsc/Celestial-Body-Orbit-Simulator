import pygame

from config import CENTER, SCALE, SCREEN_SIZE, WORLD_SIZE
from simulation import Simulation

class PygameManager:
    """This classs handles the render and pygame interaction"""

    def __init__(self, simulation: Simulation):
        """Initialize the Pygame Manager

        Args:
            simulation (Simulation): The orbit simulator
        """

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.simulation = simulation
        self.clock = pygame.time.Clock()

        # Initial variabels
        self.zoom = 1
        self.camera_pos = [0, 0]
        self.is_dragging = False
        self.last_mouse_pos = None

    def draw(self):
        """Draw Simulation elements on the pygame screen"""

        # Center the camera in the world bounds
        half_screen_width = self.screen.get_width() / (2 * self.zoom)
        half_screen_height = self.screen.get_height() / (2 * self.zoom)
        self.camera_pos[0] = max(-WORLD_SIZE[0] + half_screen_width, min(self.camera_pos[0], WORLD_SIZE[0] - half_screen_width))
        self.camera_pos[1] = max(-WORLD_SIZE[1] + half_screen_height, min(self.camera_pos[1], WORLD_SIZE[1] - half_screen_height))

        self.screen.fill((0, 0, 0)) # Clear screen

        for body in self.simulation.bodies:
            x = int((body.position[0] / SCALE - self.camera_pos[0])  * self.zoom + CENTER[0])
            y = int((body.position[1] / SCALE - self.camera_pos[1])  * self.zoom + CENTER[1])
            pygame.draw.circle(self.screen, body.color, (x, y), 8 * self.zoom)

        pygame.display.flip()
    
    def run(self):
        """Main Render Loop"""

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEWHEEL: # Handle Zoom
                    if(event.y > 0): # Zoom in
                        self.zoom = min(self.zoom * 1.1, 5)
                    elif event.y < 0: # Zoom out
                        self.zoom = max(self.zoom / 1.1, 0.1)
                elif event.type == pygame.MOUSEBUTTONDOWN: # Start dragging
                    if event.button == 1:  # Left mouse button
                        self.is_dragging = True
                        self.last_mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP: # Stop dragging
                    if event.button == 1:
                        self.is_dragging = False

                
            if self.is_dragging: # Handle panning
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.last_mouse_pos:
                    dx = (mouse_x - self.last_mouse_pos[0]) / self.zoom
                    dy = (mouse_y - self.last_mouse_pos[1]) / self.zoom
                    self.camera_pos[0] -= dx
                    self.camera_pos[1] -= dy
                    self.last_mouse_pos = (mouse_x, mouse_y)
            
            self.simulation.run()  # Update simulation state
            self.draw()
            self.clock.tick(60)

        pygame.quit()
