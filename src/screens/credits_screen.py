# credits_screen.py

import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM

class CreditsScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.back_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 100, 200, 50, "Voltar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

    def draw(self):
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)
        credits = [
            "Desenvolvedores:",
            "Thiago Melo Tonin",
            "Vitor Marconi Trancoso Albuquerque / 222006202",
            "Agradecimentos Especiais:",
            "Henrique"
        ]

        y_offset = 100
        for line in credits:
            self.game.draw_text(line, self.screen.get_width() / 2, y_offset, font_size=30, color=WHITE)
            y_offset += 40
        
        self.back_button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event):
                self.game.show_main_menu()

    def update(self):
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
