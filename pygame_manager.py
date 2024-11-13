import sys
import pygame

from config import CENTER, DELTA_T, SCALE, SCREEN_SIZE, WORLD_SIZE
from simulation import Simulation
from template_loader import TemplateLoader
from ui_manager import UIManager

class PygameManager:
    """This classs handles the render and pygame interaction"""

    def __init__(self):
        """Initialize the Pygame Manager"""

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.trail_surface = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]), pygame.SRCALPHA)  # Allow transparency
        self.trail_surface.set_alpha(30)
        self.template_loader = TemplateLoader("templates.json")
        self.simulation = Simulation(self.template_loader.get_template("solar_system"), DELTA_T)
        self.clock = pygame.time.Clock()
        self.ui_manager = UIManager()
        self.trail_limit = 200

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
        self.trail_surface.fill((0, 0, 0)) # Clear screen

        for body in self.simulation.bodies:
            body.update_trail(self.trail_limit)
            x = int((body.position[0] / SCALE - self.camera_pos[0])  * self.zoom + CENTER[0])
            y = int((body.position[1] / SCALE - self.camera_pos[1])  * self.zoom + CENTER[1])
            pygame.draw.circle(self.screen, body.color, (x, y), 8 * self.zoom)

            for trail_pos in body.trails_pos:
                trail_x = int((trail_pos[0] / SCALE - self.camera_pos[0]) * self.zoom + CENTER[0])
                trail_y = int((trail_pos[1] / SCALE - self.camera_pos[1]) * self.zoom + CENTER[1])

                pygame.draw.circle(self.trail_surface, body.color, (trail_x, trail_y), 2 * self.zoom)

        self.screen.blit(self.trail_surface, (0, 0))

        self.ui_manager.draw(self.screen)

        pygame.display.flip()
    
    def run(self):
        """Main Render Loop"""
        running = True
        while running:
            delta_time = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif event.type == pygame.MOUSEWHEEL: # Handle Zoom
                    if(event.y > 0): # Zoom in
                        self.zoom = min(self.zoom * 1.1, 5)
                    elif event.y < 0: # Zoom out
                        self.zoom = max(self.zoom / 1.1, 0.2)
                elif event.type == pygame.MOUSEBUTTONDOWN: # Start dragging
                    if event.button == 1:  # Left mouse button
                        self.is_dragging = True
                        self.last_mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP: # Stop dragging
                    if event.button == 1:
                        self.is_dragging = False
                self.ui_manager.handle_event(event)
                
            if self.is_dragging: # Handle panning
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.last_mouse_pos:
                    dx = (mouse_x - self.last_mouse_pos[0]) / self.zoom
                    dy = (mouse_y - self.last_mouse_pos[1]) / self.zoom
                    self.camera_pos[0] -= dx
                    self.camera_pos[1] -= dy
                    self.last_mouse_pos = (mouse_x, mouse_y)
            
            self.ui_manager.manager.update(delta_time)
            self.simulation.run()  # Update simulation state
            self.draw()

        pygame.quit()
