import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM, BLACK, RED

class GroupEditScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = self.game.font

        # Lista de jogadores convidados, armazenados apenas na memória (não no banco de dados)
        self.invited_players = []

        # Dimensões e espaçamento dos botões
        button_width = 200
        button_height = 50
        button_spacing = 20
        total_button_height = (button_height + button_spacing) * 4
        start_y = (self.screen.get_height() - total_button_height) / 2

        # Botões centrais
        self.add_button = Button(self.screen.get_width() / 2 - button_width / 2, start_y, button_width, button_height, "Adicionar Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.edit_button = Button(self.screen.get_width() / 2 - button_width / 2, start_y + (button_height + button_spacing), button_width, button_height, "Editar Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.remove_button = Button(self.screen.get_width() / 2 - button_width / 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, "Remover Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.back_button = Button(self.screen.get_width() / 2 - button_width / 2, start_y + 3 * (button_height + button_spacing), button_width, button_height, "Voltar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

        # Botão "Iniciar Jogo"
        self.start_game_button = None  # Só será mostrado quando jogadores forem adicionados

        # Campo de entrada para novo nome
        self.input_box = pygame.Rect(self.screen.get_width() / 2 - 150, 100, 300, 40)
        self.active_input = True
        self.input_color_inactive = BLUE_GRAY
        self.input_color_active = WHITE
        self.input_color = self.input_color_inactive
        self.new_name = ''
        self.selected_player = None

        # Estados de controle
        self.is_editing = False
        self.is_removing = False
        self.is_adding = True  # Começa no modo de adição de jogadores

        # Controle do cursor piscante
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.cursor_blink_speed = 500  # Intervalo de piscar do cursor (milissegundos)

    def draw(self):
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)
        self.game.draw_text('Gerenciar Jogadores', self.screen.get_width() / 2, 50, font_size=42, color=WHITE)

        # Renderiza o campo de entrada e o cursor piscante
        self.draw_input_box()

        # Desenha botões
        self.add_button.draw(self.screen)
        self.edit_button.draw(self.screen)
        self.remove_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # Exibe os jogadores convidados em formato de matriz 5x5
        self.draw_players_matrix()

        # Se houver jogadores, desenha o botão "Iniciar Jogo"
        if len(self.invited_players) > 0:
            if not self.start_game_button:
                # Inicializa o botão "Iniciar Jogo" quando há jogadores
                self.start_game_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 100, 200, 50, "Iniciar Jogo", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
            self.start_game_button.draw(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active_input = True
                self.input_color = self.input_color_active
            else:
                self.active_input = False
                self.input_color = self.input_color_inactive

            if self.add_button.is_clicked(event):
                self.activate_add_mode()

            if self.edit_button.is_clicked(event):
                self.activate_edit_mode()

            if self.remove_button.is_clicked(event):
                self.activate_remove_mode()

            if self.back_button.is_clicked(event):
                self.game.show_main_menu()

            if self.start_game_button and self.start_game_button.is_clicked(event):
                self.start_game()

            # Detecta clique no "X" ao remover jogador
            if self.is_removing:
                self.check_remove_click(event.pos)

            # Detecta clique no nome para editar
            if self.is_editing:
                self.check_select_click(event.pos)

        elif event.type == pygame.KEYDOWN:
            if self.active_input:
                if event.key == pygame.K_RETURN:
                    if self.is_adding:
                        self.add_player()
                    elif self.is_editing:
                        self.edit_player()
                elif event.key == pygame.K_BACKSPACE:
                    self.new_name = self.new_name[:-1]
                else:
                    self.new_name += event.unicode

    def activate_add_mode(self):
        """Ativa o modo de adição de jogadores."""
        self.is_adding = True
        self.is_editing = False
        self.is_removing = False
        self.new_name = ""  # Limpa o campo para nova entrada

    def activate_edit_mode(self):
        """Ativa o modo de edição de jogadores."""
        self.is_editing = True
        self.is_adding = False
        self.is_removing = False

    def activate_remove_mode(self):
        """Ativa o modo de remoção de jogadores."""
        self.is_removing = True
        self.is_editing = False
        self.is_adding = False

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

    def add_player(self):
        """Adiciona um jogador à lista temporária de convidados."""
        if self.new_name.strip():  # Certifica-se de que o nome não está vazio
            new_player_name = self.new_name.strip()
            self.invited_players.append(new_player_name)  # Adiciona o jogador à lista
            self.new_name = ''  # Limpa o campo de entrada
        else:
            print("Nome do jogador não pode estar vazio.")

    def edit_player(self):
        """Edita o nome do jogador convidado selecionado."""
        if self.selected_player and self.new_name.strip():
            player_index = self.invited_players.index(self.selected_player)
            self.invited_players[player_index] = self.new_name.strip()
            self.game.players = self.invited_players[:]  # Atualiza a lista de jogadores ativos no jogo
            self.new_name = ''
            self.selected_player = None  # Reseta o jogador após edição
            self.is_editing = False  # Sai do modo de edição

    def remove_player(self, player):
        """Remove o jogador convidado da lista temporária."""
        if player in self.invited_players:
            self.invited_players.remove(player)
            self.game.players = self.invited_players[:]  # Atualiza a lista de jogadores ativos no jogo

    def check_remove_click(self, pos):
        """Verifica se o jogador clicou no 'X' para remover um jogador."""
        x_start = self.screen.get_width() / 10
        y_start = 200
        row_height = 40
        col_width = self.screen.get_width() / 5

        for i, player in enumerate(self.invited_players):
            x = x_start + (i % 5) * col_width + 100  # Posição X do "X" de remoção
            y = y_start + (i // 5) * row_height
            if pygame.Rect(x, y, 20, 20).collidepoint(pos):
                self.remove_player(player)
                break

    def check_select_click(self, pos):
        """Verifica se o jogador clicou no nome de um jogador para editar."""
        x_start = self.screen.get_width() / 10
        y_start = 200
        row_height = 40
        col_width = self.screen.get_width() / 5

        for i, player in enumerate(self.invited_players):
            x = x_start + (i % 5) * col_width  # Posição do nome do jogador
            y = y_start + (i // 5) * row_height
            if pygame.Rect(x, y, col_width, row_height).collidepoint(pos):
                self.selected_player = player
                self.new_name = player  # Preenche o campo de edição com o nome atual

    def start_game(self):
        """Inicia o jogo após adicionar jogadores."""
        if self.invited_players:
            if not self.game.selected_category:
                self.game.show_choose_theme()  # Mostra a tela de seleção de temas se nenhuma categoria foi selecionada
            else:
                self.game.show_player_words(self.invited_players)  # Mostra a lista de jogadores para palavras ou impostor
        else:
            print("Adicione jogadores para iniciar o jogo.")


    def draw_players_matrix(self):
        """Desenha os jogadores convidados em formato de matriz 5x5."""
        x_start = self.screen.get_width() / 10
        y_start = 200
        row_height = 40
        col_width = self.screen.get_width() / 5

        for i, player in enumerate(self.invited_players):
            x = x_start + (i % 5) * col_width
            y = y_start + (i // 5) * row_height
            self.game.draw_text(player, x, y, font_size=24, color=WHITE)

            # Desenha o "X" de remoção ao lado do nome
            if self.is_removing:
                remove_x_pos = x + 100  # Posição do "X" ao lado do nome
                self.game.draw_text("X", remove_x_pos, y, font_size=24, color=RED)

    def update(self):
        # Atualiza o estado do cursor piscante
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_timer > self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time

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
