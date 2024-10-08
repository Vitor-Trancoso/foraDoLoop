import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM, RED
import time

class LoginScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = self.game.font

        # Caixa de entrada para o código de acesso
        self.input_box = pygame.Rect(self.screen.get_width() / 2 - 150, self.screen.get_height() / 2 - 55, 300, 40)
        self.active = False
        self.color_inactive = BLUE_GRAY
        self.color_active = WHITE
        self.color = self.color_inactive
        self.text = ''

        # Botões
        self.login_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 20, 200, 50, "Login", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.register_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 90, 200, 50, "Registrar-se", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.recover_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 160, 200, 50, "Recuperar Código", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

        # Mensagem de erro
        self.error_message = ""
        self.cursor_visible = True
        self.cursor_timer = time.time()

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

        # Desenha os botões
        self.login_button.draw(self.screen)
        self.register_button.draw(self.screen)
        self.recover_button.draw(self.screen)

        # Lógica para fazer o cursor piscar
        if self.active:
            if time.time() - self.cursor_timer > 0.5:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = time.time()

            if self.cursor_visible:
                cursor_pos = self.input_box.x + 5 + txt_surface.get_width()
                pygame.draw.line(self.screen, WHITE, (cursor_pos, self.input_box.y + 5), (cursor_pos, self.input_box.y + 35), 2)

        # Exibe mensagem de erro, se houver
        if self.error_message:
            self.display_error_message()

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica se clicou na caixa de texto
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
                self.color = self.color_active if self.active else self.color_inactive
            else:
                self.active = False
                self.color = self.color_inactive

            # Verifica se clicou nos botões
            if self.login_button.is_clicked(event):
                self.attempt_login()

            if self.register_button.is_clicked(event):
                self.game.screen_manager.show_register_screen()

            if self.recover_button.is_clicked(event):
                self.game.screen_manager.show_recover_code_screen()  # Navega para a tela de recuperação de código

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.attempt_login()  # Tentativa de login ao pressionar Enter
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def attempt_login(self):
        """Verifica se o código de acesso é válido e exibe mensagem de erro, se necessário."""
        if not self.game.player_manager.validate_login(self.text):
            self.error_message = "Código inválido! Digite um código válido ou registre-se."
        else:
            self.error_message = ""
            self.game.screen_manager.show_main_menu()

    def display_error_message(self):
        # Renderiza a mensagem de erro
        font = pygame.font.Font(None, 27)
        text_surface = font.render(self.error_message, True, RED)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 160))
        self.screen.blit(text_surface, text_rect)

    def update(self):
        # Método vazio para evitar o erro
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
