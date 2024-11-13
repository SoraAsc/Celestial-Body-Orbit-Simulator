import sys
import pygame

from config import CENTER, DELTA_T, SCALE, SCREEN_SIZE, WORLD_SIZE, FUNCTIONS_MANAGER
from simulation import Simulation
from template_loader import TemplateLoader
from ui_manager import UIManager

class PygameManager:
    """This classs handles the render and pygame interaction"""

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.trail_surface = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]), pygame.SRCALPHA)  # Allow transparency
        self.trail_surface.set_alpha(30)
        self.clock = pygame.time.Clock()

        funcs = FUNCTIONS_MANAGER(refresh_simulation=self.initialize_simulation, 
                                  load_template=self.load_template, change_method=self.change_method,
                                  toggle_trails=self.toggle_trails)
        self.ui_manager = UIManager(funcs)
        self.template_loader = TemplateLoader("templates.json", "solar_system")

        self.initialize_simulation()
    
    def initialize_simulation(self):
        self.simulation = Simulation(self.template_loader.get_template(self.template_loader.template_name), DELTA_T)
        
        # Initial variabels
        self.zoom = 1
        self.camera_pos = [0, 0]
        self.is_dragging = False
        self.is_trail_actived = True
        self.last_mouse_pos = None
        self.trail_limit = 200

    def toggle_trails(self) -> bool:
        self.is_trail_actived = not self.is_trail_actived
        return self.is_trail_actived

    def load_template(self, template_name: str):
        self.simulation.change_bodies(self.template_loader.get_template(template_name))
        
        # Reset variable values
        self.zoom = 1
        self.camera_pos = [0, 0]
        self.is_dragging = False
        self.last_mouse_pos = None
    
    def change_method(self, method_name: str):
        self.simulation.integrator.choose_method(method_name)

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

            if self.is_trail_actived:
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
