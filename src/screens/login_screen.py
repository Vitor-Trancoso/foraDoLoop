# src/screens/login_screen.py

import pygame
from ..ui import Button
from ..constants import WHITE, RED, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM

class LoginScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font

        self.input_box = pygame.Rect(self.screen.get_width() / 2 - 150, self.screen.get_height() / 2 - 55, 300, 40)
        self.active = False
        self.color_inactive = BLUE_GRAY  # Azul acinzentado quando inativo
        self.color_active = WHITE        # Branco quando ativo
        self.color = self.color_inactive
        self.text = ''

        self.login_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 20, 200, 50, "Login", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.register_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 90, 200, 50, "Registrar-se", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

        self.error_message = ""

    def draw(self):
        # Desenha o fundo com gradiente
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)

        # Desenha o texto de instrução
        self.game.draw_text('Digite seu código de acesso:', self.screen.get_width() / 2, self.screen.get_height() / 2 - 100, font_size=42, color=WHITE)

        # Renderiza o texto inserido na caixa de entrada
        txt_surface = self.font.render(self.text, True, WHITE)
        width = max(300, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.color, self.input_box, border_radius=15, width=2)

        # Desenha os botões de login e registro
        self.login_button.draw(self.screen)
        self.register_button.draw(self.screen)

        # Exibe mensagem de erro, se houver
        if self.error_message:
            self.display_error_message()

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
                self.color = self.color_active if self.active else self.color_inactive
            else:
                self.active = False
                self.color = self.color_inactive

            if self.login_button.is_clicked(event):
                if not self.game.player_manager.validate_login(self.text):
                    self.error_message = "Código inválido! Digite um código válido ou registre-se."
                else:
                    self.error_message = ""  # Limpar mensagem de erro ao fazer login com sucesso
                    self.game.screen_manager.show_main_menu()

            if self.register_button.is_clicked(event):
                self.game.screen_manager.show_register_screen()

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if not self.game.player_manager.validate_login(self.text):
                        self.error_message = "Código inválido! Digite um código válido ou registre-se."
                    else:
                        self.error_message = ""  # Limpar mensagem de erro ao fazer login com sucesso
                        self.game.screen_manager.show_main_menu()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def display_error_message(self):
        # Renderiza o texto do erro
        font = pygame.font.Font(None, 27)
        text_surface = font.render(self.error_message, True, RED)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 160))
        self.screen.blit(text_surface, text_rect)

    def update(self):
        # Método update vazio, pode ser preenchido conforme necessário
        pass

    def draw_gradient_background(self, color_top, color_bottom):
        """Desenha um gradiente vertical de cima para baixo."""
        for y in range(self.screen.get_height()):
            ratio = y / self.screen.get_height()
            color = (
                int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio),
                int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio),
                int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))
