import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM, BLACK, RED
from .add_player import AddPlayer
from .edit_player import EditPlayer
from .remove_player import RemovePlayer

class GroupEditScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = self.game.font

        self.invited_players = []  # Lista temporária de jogadores convidados

        # Instâncias das classes de adicionar, editar e remover
        self.add_player_obj = AddPlayer(self.invited_players)
        self.edit_player_obj = EditPlayer(self.invited_players)
        self.remove_player_obj = RemovePlayer(self.invited_players)

        # Botões
        button_width = 200
        button_height = 50
        button_spacing = 20
        total_button_height = (button_height + button_spacing) * 4
        start_y = (self.screen.get_height() - total_button_height) / 2

        self.add_button = Button(self.screen.get_width() / 2 - button_width / 2, start_y, button_width, button_height, "Adicionar Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.edit_button = Button(self.screen.get_width() / 2 - button_width / 2, start_y + (button_height + button_spacing), button_width, button_height, "Editar Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.remove_button = Button(self.screen.get_width() / 2 - button_width / 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, "Remover Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.back_button = Button(self.screen.get_width() / 2 - button_width / 2, start_y + 3 * (button_height + button_spacing), button_width, button_height, "Voltar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

        # Botão "OK" para finalizar a adição de jogadores
        self.ok_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 150, 200, 50, "OK", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.show_ok_button = False  # Controla a visibilidade do botão OK

        # Inicializa o campo de entrada para nome do jogador
        self.input_box = pygame.Rect(self.screen.get_width() / 2 - 150, 100, 300, 40)
        self.active_input = False  # Campo de entrada inativo por padrão
        self.input_color_inactive = BLUE_GRAY
        self.input_color_active = WHITE
        self.input_color = self.input_color_inactive
        self.new_name = ''
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.cursor_blink_speed = 500  # Intervalo de piscar do cursor (milissegundos)

        # Mensagem para escolher uma opção
        self.message = "Escolha uma opção"  # Texto padrão antes de escolher funcionalidade

        # Guarda as hitboxes dos jogadores
        self.player_hitboxes = []

    def draw(self):
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)
        self.game.draw_text('Gerenciar Jogadores', self.screen.get_width() / 2, 50, font_size=42, color=WHITE)

        # Desenha a mensagem
        self.game.draw_text(self.message, self.screen.get_width() / 2, 150, font_size=32, color=WHITE)

        # Desenha botões (somente se não estiver no modo de adicionar jogador)
        if not self.active_input:
            self.add_button.draw(self.screen)
            self.edit_button.draw(self.screen)
            self.remove_button.draw(self.screen)
            self.back_button.draw(self.screen)

        # Renderiza o campo de entrada se ativo
        if self.active_input:
            self.draw_input_box()
            if self.show_ok_button:
                self.ok_button.draw(self.screen)

        # Exibe os jogadores convidados
        self.draw_players_matrix()

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Se clicou em uma área fora da caixa de entrada, desativa o input
            if not self.input_box.collidepoint(event.pos):
                self.active_input = False

            if not self.active_input:
                if self.add_button.is_clicked(event):
                    self.activate_input("add")

                if self.edit_button.is_clicked(event):
                    self.activate_input("edit")

                if self.remove_button.is_clicked(event):
                    self.activate_input("remove")

                if self.back_button.is_clicked(event):
                    self.game.show_main_menu()

            # Detecta clique no botão OK
            if self.active_input and self.show_ok_button and self.ok_button.is_clicked(event):
                self.finish_action()

            # Detecta cliques nas hitboxes dos jogadores
            for index, hitbox in enumerate(self.player_hitboxes):
                if hitbox.collidepoint(event.pos):
                    print(f"Jogador clicado: {self.invited_players[index]}")
                    # Aqui você pode adicionar a lógica para editar/remover o jogador clicado

        elif event.type == pygame.KEYDOWN and self.active_input:
            if event.key == pygame.K_RETURN:
                if self.message == "Adicionar Jogador":
                    self.add_player_obj.add_player(self.new_name)
                elif self.message == "Editar Jogador":
                    self.edit_player_obj.edit_player(self.new_name)
                elif self.message == "Remover Jogador":
                    self.remove_player_obj.remove_player(self.new_name)

                self.new_name = ''  # Limpa o campo de entrada
            elif event.key == pygame.K_BACKSPACE:
                self.new_name = self.new_name[:-1]
            else:
                self.new_name += event.unicode

    def activate_input(self, action_type):
        """Ativa a caixa de entrada e esconde os outros botões."""
        self.active_input = True
        self.new_name = ''  # Limpa o campo de entrada
        self.show_ok_button = True  # Mostra o botão OK
        if action_type == "add":
            self.message = "Adicionar Jogador"
        elif action_type == "edit":
            self.message = "Editar Jogador"
        elif action_type == "remove":
            self.message = "Remover Jogador"

    def finish_action(self):
        """Finaliza a ação de adicionar/editar/remover jogador e restaura os botões."""
        self.active_input = False
        self.show_ok_button = False
        self.message = "Escolha uma opção"  # Retorna a mensagem padrão

    def update(self):
        """Atualiza o estado do cursor piscante."""
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_timer > self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time

    def draw_input_box(self):
        """Desenha o campo de entrada de nome com o cursor piscante."""
        txt_surface = self.font.render(self.new_name, True, BLACK)
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.input_color, self.input_box, border_radius=15, width=2)

        # Desenha cursor piscante
        if self.cursor_visible:
            cursor_x = self.input_box.x + txt_surface.get_width() + 5
            cursor_y = self.input_box.y + 5
            pygame.draw.rect(self.screen, BLACK, (cursor_x, cursor_y, 2, self.font.get_height()))

    def draw_players_matrix(self):
        """Desenha os jogadores convidados em formato de matriz e cria hitboxes."""
        x_start = self.screen.get_width() / 10
        y_start = 200
        row_height = 40
        col_width = self.screen.get_width() / 5

        self.player_hitboxes = []  # Limpa as hitboxes antes de desenhar novamente

        for i, player in enumerate(self.invited_players):
            x = x_start + (i % 5) * col_width
            y = y_start + (i // 5) * row_height
            player_rect = pygame.Rect(x - 10, y - 10, col_width, row_height)  # Cria uma hitbox ao redor do nome
            pygame.draw.rect(self.screen, BLUE_GRAY, player_rect, 2)  # Desenha o contorno (hitbox)
            self.game.draw_text(player, x, y, font_size=24, color=WHITE)

            self.player_hitboxes.append(player_rect)  # Armazena a hitbox do jogador

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
