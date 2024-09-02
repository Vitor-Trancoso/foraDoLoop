# src/screens/voting_screen.py

import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY

class VotingScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.vote_results = {}

        # Criar o botão de voltar ao menu principal
        self.back_button = Button(self.screen.get_width() / 2 - 75, self.screen.get_height() / 2 + 220, 150, 40, "Voltar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

        # Inicializar a fase de votação
        self.initialize_voting()

    def initialize_voting(self):
        self.vote_results = {player.name: 0 for player in self.game.player_manager.active_players}

    def draw(self):
        self.screen.fill(WHITE)
        self.game.draw_text('Votação em progresso...', self.screen.get_width() / 2, self.screen.get_height() / 2 - 100, font_size=36)

        # Desenhar o botão de voltar
        self.back_button.draw(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event):
                self.game.main_menu()

    def update(self):
        pass  # Implementar lógica de votação aqui
