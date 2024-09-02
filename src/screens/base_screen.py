# admin_screen.py

import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM, GREEN

class AdminScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.players = self.game.player_manager.get_all_players()  # Carrega todos os jogadores

        # Definição dos botões
        self.add_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2, 200, 50, "Adicionar Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.remove_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 70, 200, 50, "Remover Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.edit_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 140, 200, 50, "Editar Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.back_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 210, 200, 50, "Voltar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

    def draw(self):
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)
        self.game.draw_text('Administração do Jogo', self.screen.get_width() / 2, self.screen.get_height() / 2 - 100, font_size=42, color=WHITE)

        # Desenha os botões
        self.add_button.draw(self.screen)
        self.remove_button.draw(self.screen)
        self.edit_button.draw(self.screen)
        self.back_button.draw(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.add_button.is_clicked(event):
                self.add_player()
            elif self.remove_button.is_clicked(event):
                self.remove_player()
            elif self.edit_button.is_clicked(event):
                self.edit_player()
            elif self.back_button.is_clicked(event):
                self.game.show_main_menu()

    def update(self):
        pass

    def add_player(self):
        # Lógica para adicionar um jogador
        player_name = "Jogador " + str(len(self.players) + 1)
        self.players.append(player_name)
        self.game.player_manager.add_player(player_name)
        self.game.player_manager.save_players()

    def remove_player(self):
        # Função para remover jogadores - lógica para remover um jogador específico
        if self.players:
            player_name = self.players.pop()  # Remove o último jogador adicionado como exemplo
            self.game.player_manager.remove_player(player_name)
            self.game.player_manager.save_players()

    def edit_player(self):
        # Função para editar jogadores - lógica para editar o nome do jogador
        if self.players:
            old_name = self.players[-1]  # Exemplo: pega o último jogador da lista
            new_name = old_name + "_editado"
            self.game.player_manager.update_player_name(old_name, new_name)
            self.players[-1] = new_name
            self.game.player_manager.save_players()

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
