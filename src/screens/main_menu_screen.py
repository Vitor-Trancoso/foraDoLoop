import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM, BLACK

class MainMenuScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font

        # Fonte e tamanho para o título
        self.title_font = pygame.font.Font(None, 72)  # Usar um tamanho grande
        self.title_text = "Fora do Loop"

        # Definição dos botões
        self.buttons = [
            Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 - 100, 200, 50, "Iniciar Jogo", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25),
            Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 - 30, 200, 50, "Editar Grupo", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25),  # Botão Editar Grupo
            Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 40, 200, 50, "Instruções", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25),
            Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 110, 200, 50, "Configurações", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25),
            Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 180, 200, 50, "Créditos", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25),
            Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 250, 200, 50, "Sair", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        ]

    def draw(self):
        # Desenha o fundo com gradiente
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)

        # Desenha o título
        self.draw_title()

        # Desenha cada botão
        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.is_clicked(event):
                    self.handle_button_click(button.text)

    def handle_button_click(self, button_text):
        if button_text == "Iniciar Jogo":
            self.game.start_game()
        elif button_text == "Editar Grupo":  # Ação do botão Editar Grupo
            self.game.show_group_edit_screen()
        elif button_text == "Instruções":
            self.game.show_instructions()
        elif button_text == "Configurações":
            self.game.show_settings()
        elif button_text == "Créditos":
            self.game.show_credits()
        elif button_text == "Sair":
            self.game.exit_game()

    def update(self):
        # Método update vazio, pode ser preenchido conforme necessário
        pass

    def draw_title(self):
        """Desenha o título na parte superior da tela."""
        title_surface = self.title_font.render(self.title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() / 2, 150))  # Centraliza horizontalmente, movido mais para baixo
        shadow_surface = self.title_font.render(self.title_text, True, BLACK)  # Sombra
        shadow_rect = shadow_surface.get_rect(center=(self.screen.get_width() / 2 + 3, 153))  # Leve deslocamento para sombra
        self.screen.blit(shadow_surface, shadow_rect)  # Desenha a sombra
        self.screen.blit(title_surface, title_rect)  # Desenha o título

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
