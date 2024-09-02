# choose_theme_screen.py

import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM

class ChooseThemeScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(None, 42)  # Fonte para temas
        self.small_font = pygame.font.Font(None, 36)  # Fonte para botões

        # Botão Voltar
        button_width = 200
        button_height = 50
        button_x = (self.screen.get_width() - button_width) / 2
        button_y = self.screen.get_height() - 100

        self.back_button = Button(button_x, button_y, button_width, button_height, "Voltar", self.small_font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

        # Definindo os temas
        self.themes = list(self.game.categories.keys())
        self.buttons = []

        # Criando botões para cada tema
        y_offset = 150
        for theme in self.themes:
            theme_button = Button(
                self.screen.get_width() / 2 - 100, y_offset, 200, 50, theme, self.small_font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15
            )
            self.buttons.append(theme_button)
            y_offset += 70  # Espaçamento entre botões

    def draw(self):
        # Desenha o fundo com gradiente
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)

        # Desenha o título
        self.game.draw_text('Escolha um Tema', self.screen.get_width() / 2, 80, font_size=54, color=WHITE)

        # Desenha botões para temas
        for button in self.buttons:
            button.draw(self.screen)

        # Desenha o botão Voltar
        self.back_button.draw(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event):
                self.game.screen_manager.show_main_menu()
            for button in self.buttons:
                if button.is_clicked(event):
                    self.game.selected_category = button.text
                    self.game.screen_manager.show_player_setup()

    def update(self):
        pass  # Método update vazio

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
