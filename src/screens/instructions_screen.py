# instructions_screen.py

import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM

class InstructionsScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.back_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 100, 200, 50, "Voltar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

    def draw(self):
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)
        instructions = [
            "Como jogar Out of the Loop:",
            "1. Selecione o número de jogadores e um tema.",
            "2. Cada jogador receberá uma palavra, exceto o impostor.",
            "3. Os jogadores fazem perguntas uns aos outros para descobrir quem é o impostor.",
            "4. Após a rodada de perguntas, os jogadores votam no impostor.",
            "5. O impostor tenta adivinhar a palavra secreta."
        ]

        y_offset = 100
        for line in instructions:
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
