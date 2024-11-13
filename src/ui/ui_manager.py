import os
import time
from typing import List
import pygame
import pygame_gui
from config import SCREEN_SIZE, FUNCTIONS_MANAGER

class UIManager:
    """This class handles all UI interaction"""

    def __init__(self, funcs: FUNCTIONS_MANAGER):
        """Initialize the UI Manager"""

        self.funcs = funcs
        theme_path = os.path.join(os.path.dirname(__file__), "theme.json")
        self.manager = pygame_gui.UIManager((SCREEN_SIZE[0], SCREEN_SIZE[1]), theme_path)
        self.text_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, SCREEN_SIZE[0] - 30), (SCREEN_SIZE[1], 30)), manager=self.manager)
        self.text_entry.set_text("")
        self.text_entry.hide()

        self.feedback_box = pygame_gui.elements.ui_text_box.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((0, SCREEN_SIZE[0] - 150), (SCREEN_SIZE[1], 150)),
            manager=self.manager,
            object_id='#text_box',
            visible = 0
        )

        self.input_active = False
        self.feedback_timer = None
        # Define the command dictionary with specific function signatures
        self.commands = {
            "restart": self.restart_simulation,
            "template": self.change_template,
            "method": self.change_method,
            "toggle_trails": self.toggle_trails,
            "generate_chart": self.change_template,
            "help": self.show_help,
        }
    
    def toggle_trails(self, _):
        self.set_feedback(f"Trails is {'actived' if self.funcs.toggle_trails() else 'desactived'}!")

    def change_method(self, args: List[str]):
        if args:
            method_name = args[0]
            try:
                self.funcs.change_method(method_name)
                self.set_feedback(f"Method changed to '{method_name}'.")
            except Exception:
                self.set_feedback(f"Method '{method_name}' not exist.")
        else:
            self.set_feedback("Please specify a method name. Usage: /method [method_name]")

    def restart_simulation(self, _):        
        self.funcs.refresh_simulation()
        self.set_feedback("Simulation restarted!")
        pass

    def set_feedback(self, message: str, duration: int = 5):
        """Set the feedback message and display it for a specified duration."""

        self.feedback_box.set_text(message)
        self.feedback_box.show()
        self.feedback_timer = time.time() + duration

    def clear_feedback(self):
        """Clear and Hide the feedback box"""
        self.feedback_box.hide()
        self.feedback_box.set_text("")
        self.feedback_timer = None
    
    def toggle_text_input(self):
        """Toggles the visibility of the text input box"""

        self.input_active = not self.input_active
        if self.input_active:
            self.text_entry.show()
            self.feedback_box.hide()
            self.text_entry.focus()
        else:
            self.text_entry.hide()
            self.text_entry.set_text("")

    def handle_command(self, command: str):
        """Parses and executes a command based on input string."""

        if command.strip() == "":
            self.set_feedback("Empty command. Type '/help' for a list of commands.")
            return
        
        parts = command.strip().split()
        cmd_name = parts[0][1:]
        args = parts[1:]

        if cmd_name in self.commands:
            self.commands[cmd_name](args)
        else:
            self.set_feedback(f"Command '{cmd_name}' not recognized. Type '/help' for a list of commands.")
    
    def change_template(self, args: List[str]):
        if args:
            template_name = args[0]
            try:
                self.funcs.load_template(template_name)
                self.set_feedback(f"Template changed to '{template_name}'.")
            except TypeError:
                self.set_feedback(f"Template '{template_name}' not exist.")
        else:
            self.set_feedback("Please specify a template name. Usage: /template [template_name]")

    def show_help(self, _):
        """Displays all available commands."""

        self.set_feedback(
            "Available commands:\n"
            "/template [name] - Change template\n"
            "/method [name] - Change integration method(Euler, RK4)\n"
            "/toggle_trails - Enable or Disable trail visualization\n"
            "/restart - restart the current template\n"
            "/set_time_interval [number] - Set Simulation Time Interval\n"
            "/positions_size [number] - Change The limit of positions to save\n"
            "/generate_chart [type] [name] - Generate a graph with the lasts positions\n"
            "/help - Show commands list"
        )
    
    def draw(self, screen: pygame.Surface):
        """Draws the UI elements onto the given screen surface."""

        if self.feedback_timer and time.time() > self.feedback_timer:
            self.clear_feedback()
        self.manager.draw_ui(screen)
    
    def handle_event(self, event: pygame.Event):
        """Processes UI inputs events."""

        self.manager.process_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_active:
                    command = self.text_entry.get_text()
                    self.handle_command(command)
                    self.toggle_text_input()
                else:
                    self.toggle_text_input()
            elif event.key == pygame.K_SLASH and not self.input_active:
                self.toggle_text_input()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button not in [4, 5]:
            self.clear_feedback()
            if self.input_active and not (self.text_entry.get_relative_rect().collidepoint(event.pos)):
                self.toggle_text_input()