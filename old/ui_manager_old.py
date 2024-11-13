import time


class UIManager:

    def __init__(self):
        self.input_active = False
        self.text_input = ""
        self.commands = {
            "template": self.change_template,
            "set_time_interval": self.set_time_interval,
            "help": self.show_help
        }
        self.message = ""
        self.message_time = 0
        self.cursor_visible = True
        self.time_interval = 1.0
    
    def open_text_input(self, initial_text = ""):
        self.input_active = True
        self.text_input = initial_text
        self.cursor_visible = True

    def close_text_input(self):
        self.input_active = False
        self.text_input = ""

    def handle_command(self, command):
        if command.strip() == "":
            self.message = "Empty command. Type '/help' for a list of commands."
            self.message_time = time.time()
            return
        
        parts = command.strip().split()
        cmd_name = parts[0][1:]  # Remove "/"
        args = parts[1:]

        # If command exist execute if not give error
        if cmd_name in self.commands:
            self.commands[cmd_name](args)
        else:
            self.message = f"Command '{cmd_name}' not recognized. Type '/help' for a list of commands."
            self.message_time = time.time()
    
    def change_template(self, args):
        if args:
            # Aqui você pode implementar a lógica para mudar o template com base em args[0]
            template_name = args[0]
            self.message = f"Template changed to {template_name}."
        else:
            self.message = "Please specify a template name. Usage: /template [template_name]"

    def set_time_interval(self, args):
        if args and args[0].isdigit():
            time_interval = float(args[0])
            if 0.1 <= time_interval <= 5.0:
                self.time_interval = time_interval
                self.message = f"Time interval set to {time_interval}."
            else:
                self.message = "Time interval out of range (0.1 - 5.0)."
        else:
            self.message = "Invalid input. Usage: /set_time_interval [number]"
        self.message_time = time.time()

    def show_help(self, args):
        self.message = "Available commands:\n/template [template_name]\n/help"

    def draw(self, screen, pygame):
        if self.input_active:
            self.update_cursor(pygame)
            pygame.draw.rect(screen, (50, 50, 50), (0, 550, 800, 50))
            font = pygame.font.Font(None, 36)
            text_display = self.text_input + ("|" if self.cursor_visible else "")
            text_surface = font.render(text_display, True, (255, 255, 255))
            screen.blit(text_surface, (10, 560))

        # Verifica o tempo da mensagem e apaga se necessário
        if time.time() - self.message_time < 3:
            font = pygame.font.Font(None, 24)
            message_lines = self.message.split("\n")
            for i, line in enumerate(message_lines):
                message_surface = font.render(line, True, (200, 200, 200))
                screen.blit(message_surface, (10, 520 + i * 20))

    def update_cursor(self, pygame):
        # Alterna a visibilidade do cursor a cada meio segundo
        if pygame.time.get_ticks() % 500 < 250:
            self.cursor_visible = True
        else:
            self.cursor_visible = False

    def handle_event(self, event, pygame):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_active:
                    self.handle_command(self.text_input)
                    self.close_text_input()
                else:
                    self.open_text_input()
            elif event.key == pygame.K_SLASH:
                self.open_text_input("/")
            elif self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                else:
                    self.text_input += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN and self.input_active:
            # Fecha a caixa de entrada se clicar fora dela
            mouse_x, mouse_y = event.pos
            if not (0 <= mouse_x <= 800 and 550 <= mouse_y <= 600):
                self.close_text_input()