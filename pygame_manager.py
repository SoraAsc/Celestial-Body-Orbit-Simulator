import pygame

from config import CENTER, SCALE, SCREEN_SIZE
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

    def draw(self):
        """Draw Simulation elements on the pygame screen"""
        self.screen.fill((0, 0, 0)) # Clear screen

        for body in self.simulation.bodies:
            x = int(body.position[0] / SCALE + CENTER[0])
            y = int(body.position[1] / SCALE + CENTER[1])
            pygame.draw.circle(self.screen, body.color, (x, y), 8)

        pygame.display.flip()
    
    def run(self):
        """Main Render Loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.simulation.run()  # Update simulation state
            self.draw()
            self.clock.tick(60)

        pygame.quit()
