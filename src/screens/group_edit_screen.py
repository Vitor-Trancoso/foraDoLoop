import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM, RED, GREEN, BLACK

class GroupEditScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font

        # Filtra a lista para excluir o administrador
        self.players = [player for player in self.game.player_manager.get_all_players() if player.name != "admin"]

        # Botões
        self.add_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 250, 200, 50, "Adicionar Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.edit_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 180, 200, 50, "Editar Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.remove_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 110, 200, 50, "Remover Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.back_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 40, 200, 50, "Voltar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

        # Campo de entrada para novo nome
        self.input_box = pygame.Rect(self.screen.get_width() / 2 - 150, 150, 300, 40)
        self.active_input = False
        self.input_color_inactive = BLUE_GRAY
        self.input_color_active = WHITE
        self.input_color = self.input_color_inactive
        self.new_name = ''
        self.selected_player = None

    def draw(self):
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)
        self.game.draw_text('Editar Grupo', self.screen.get_width() / 2, 50, font_size=42, color=WHITE)

        # Desenha campo de entrada
        txt_surface = self.font.render(self.new_name, True, BLACK)
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.input_color, self.input_box, border_radius=15, width=2)

        # Desenha botões
        self.add_button.draw(self.screen)
        self.edit_button.draw(self.screen)
        self.remove_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # Lista de jogadores, centralizada
        y_offset = 100
        for player in self.players:
            player_text = player.name
            self.game.draw_text(player_text, self.screen.get_width() / 2, y_offset, font_size=24, color=WHITE)
            y_offset += 30

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active_input = not self.active_input
                self.input_color = self.input_color_active if self.active_input else self.input_color_inactive
            else:
                self.active_input = False
                self.input_color = self.input_color_inactive

            if self.add_button.is_clicked(event):
                self.add_player()

            if self.edit_button.is_clicked(event):
                self.edit_player()

            if self.remove_button.is_clicked(event):
                self.remove_player()

            if self.back_button.is_clicked(event):
                self.game.show_main_menu()

        elif event.type == pygame.KEYDOWN:
            if self.active_input:
                if event.key == pygame.K_RETURN:
                    self.edit_player()
                elif event.key == pygame.K_BACKSPACE:
                    self.new_name = self.new_name[:-1]
                else:
                    self.new_name += event.unicode

    def add_player(self):
        if self.new_name.strip():
            new_player_name = self.new_name.strip()
            self.game.player_manager.add_player(new_player_name)
            self.players = [player for player in self.game.player_manager.get_all_players() if player.name != "admin"]
            self.new_name = ''  # Limpa o campo de entrada

    def edit_player(self):
        if self.selected_player and self.new_name.strip():
            self.game.player_manager.update_player_name(self.selected_player.name, self.new_name.strip())
            self.players = [player for player in self.game.player_manager.get_all_players() if player.name != "admin"]
            self.new_name = ''  # Limpa o campo de entrada

    def remove_player(self):
        if self.selected_player:
            self.game.player_manager.remove_player(self.selected_player.name)
            self.players = [player for player in self.game.player_manager.get_all_players() if player.name != "admin"]

    def update(self):
        # Pode ser usado para verificar mudanças no estado
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
