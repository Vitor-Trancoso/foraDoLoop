# instructions_screen.py

import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM, BLACK

class InstructionsScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = self.game.font
        self.large_font = pygame.font.Font(None, 40)  # Fonte maior para melhorar visibilidade
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

        # Centralizar o texto e ajustar a posição
        y_offset = self.screen.get_height() / 4  # Centralizar verticalmente
        line_spacing = 50  # Espaçamento entre as linhas
        shadow_offset = 2  # Deslocamento para o sombreamento

        for line in instructions:
            # Desenhar o sombreamento branco
            self.draw_text_with_shadow(line, self.screen.get_width() / 2, y_offset, font_size=36, text_color=WHITE, shadow_color=BLACK, shadow_offset=shadow_offset)
            y_offset += line_spacing
        
        # Desenha o botão de voltar
        self.back_button.draw(self.screen)
        pygame.display.flip()

    def draw_text_with_shadow(self, text, x, y, font_size, text_color, shadow_color, shadow_offset):
        """Desenha o texto com sombra branca."""
        font = pygame.font.Font(None, font_size)
        # Renderizar o sombreamento (preto)
        shadow_surface = font.render(text, True, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(x + shadow_offset, y + shadow_offset))
        self.screen.blit(shadow_surface, shadow_rect)

        # Renderizar o texto principal (na cor desejada)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

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
