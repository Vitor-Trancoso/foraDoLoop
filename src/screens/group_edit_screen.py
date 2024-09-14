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

        # Estado inicial da mensagem
        self.message = "Escolha uma opção"

        # Estado de controle
        self.is_adding = False
        self.is_editing = False
        self.is_removing = False
        self.selected_player = None

        # Configurações de botões e outros elementos
        self.setup_buttons()

        # Controle de piscar do cursor
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.cursor_blink_speed = 500  # Intervalo de piscar do cursor (milissegundos)
        self.new_name = ""

    def setup_buttons(self):
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

        # Botão "Okay" (somente aparece ao adicionar, editar ou remover jogador)
        self.okay_button = None
        self.confirm_button = None  # Botão de confirmar edição/remocao

    def draw(self):
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)
        self.game.draw_text(self.message, self.screen.get_width() / 2, 50, font_size=42, color=WHITE)

        if not self.is_adding and not self.is_editing and not self.is_removing:
            # Desenha os botões quando não está adicionando, editando ou removendo jogador
            self.add_button.draw(self.screen)
            self.edit_button.draw(self.screen)
            self.remove_button.draw(self.screen)
            self.back_button.draw(self.screen)
        elif self.is_adding:
            # Exibe campo de entrada para adicionar jogadores e o botão "Okay"
            self.draw_input_box()
            if self.okay_button:
                self.okay_button.draw(self.screen)
        elif self.is_editing:
            # Exibe o campo de entrada para editar jogador e o botão de confirmar
            self.draw_input_box()
            if self.confirm_button:
                self.confirm_button.draw(self.screen)
            if self.okay_button:
                self.okay_button.draw(self.screen)
        elif self.is_removing:
            # Exibe os jogadores para remoção com o botão "X" ao lado
            self.draw_players_matrix_for_removal()
            if self.okay_button:
                self.okay_button.draw(self.screen)

        # Exibe a lista de jogadores adicionados (em qualquer funcionalidade)
        if not self.is_removing:
            self.draw_players_matrix()

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.is_adding and not self.is_editing and not self.is_removing:
                # Ações quando não está adicionando, editando ou removendo jogador
                if self.add_button.is_clicked(event):
                    self.start_adding_player()
                elif self.edit_button.is_clicked(event):
                    self.start_editing_player()
                elif self.remove_button.is_clicked(event):
                    self.start_removing_player()
                elif self.back_button.is_clicked(event):
                    self.game.show_main_menu()
            elif self.is_adding:
                if self.okay_button and self.okay_button.is_clicked(event):
                    self.finish_adding_player()
            elif self.is_editing:
                if self.confirm_button and self.confirm_button.is_clicked(event):
                    self.confirm_editing_player()
                if self.okay_button and self.okay_button.is_clicked(event):
                    self.finish_editing_player()
                self.check_select_click(event.pos)
            elif self.is_removing:
                if self.okay_button and self.okay_button.is_clicked(event):
                    self.finish_removing_player()
                self.check_remove_click(event.pos)

        elif event.type == pygame.KEYDOWN:
            if self.is_adding:
                if event.key == pygame.K_RETURN:
                    self.add_player()
                elif event.key == pygame.K_BACKSPACE:
                    self.new_name = self.new_name[:-1]
                else:
                    self.new_name += event.unicode
            elif self.is_editing:
                if event.key == pygame.K_BACKSPACE:
                    self.new_name = self.new_name[:-1]
                else:
                    self.new_name += event.unicode

    def start_adding_player(self):
        """Inicia a ação de adicionar um jogador."""
        self.is_adding = True
        self.message = "Adicionar Jogador"
        self.new_name = ""
        self.okay_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 100, 200, 50, "Okay", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

    def finish_adding_player(self):
        """Finaliza a ação de adicionar jogador e volta para a tela com as opções."""
        self.is_adding = False
        self.message = "Escolha uma opção"  # Restaura a mensagem padrão
        self.okay_button = None  # Remove o botão "Okay"

    def add_player(self):
        """Adiciona um jogador à lista de convidados."""
        if self.new_name.strip():  # Verifica se o nome não está vazio
            self.invited_players.append(self.new_name.strip())
            self.new_name = ""  # Limpa o campo de entrada

    def start_editing_player(self):
        """Inicia a ação de editar um jogador."""
        self.is_editing = True
        self.message = "Editar Jogador"
        self.new_name = ""
        self.confirm_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 100, 200, 50, "Confirmar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)
        self.okay_button = None

    def confirm_editing_player(self):
        """Confirma a edição de um jogador selecionado."""
        if self.selected_player and self.new_name.strip():
            player_index = self.invited_players.index(self.selected_player)
            self.invited_players[player_index] = self.new_name.strip()
            self.new_name = ""  # Limpa o campo de entrada
            self.selected_player = None  # Reseta a seleção

            # Remove o botão Confirmar e exibe o botão Okay
            self.confirm_button = None
            self.okay_button = Button(
                self.screen.get_width() / 2 - 100, 
                self.screen.get_height() - 100, 
                200, 50, 
                "Okay", 
                self.font, 
                BLUE_GRAY, 
                DARK_BLUE_GRAY, 
                corner_radius=25
            )


    def finish_editing_player(self):
        """Finaliza a ação de editar jogador e volta para a tela com as opções."""
        self.is_editing = False
        self.message = "Escolha uma opção"  # Restaura a mensagem padrão
        self.okay_button = None  # Remove o botão "Okay"
        self.selected_player = None  # Limpa o jogador selecionado

    def start_removing_player(self):
        """Inicia a ação de remover um jogador."""
        self.is_removing = True
        self.message = "Remover Jogador"
        self.okay_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 100, 200, 50, "Okay", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

    def finish_removing_player(self):
        """Finaliza a ação de remover jogador e volta para a tela com as opções."""
        self.is_removing = False
        self.message = "Escolha uma opção"
        self.okay_button = None

    def check_remove_click(self, pos):
        """Verifica se o jogador clicou no 'X' para remover um jogador."""
        x_start = self.screen.get_width() / 10
        y_start = 200
        row_height = 50
        col_width = self.screen.get_width() / 5
        for i, player in enumerate(self.invited_players):
            x = x_start + (i % 5) * col_width
            y = y_start + (i // 5) * row_height
            player_surface = self.font.render(player, True, WHITE)
            text_width, text_height = player_surface.get_size()

            player_rect = pygame.Rect(
                x - 20 // 2,
                y - 10 // 2,
                text_width + 20,
                text_height + 10
            )

            # Posição do "X"
            remove_x_pos = x + text_width + 20
            remove_rect = pygame.Rect(remove_x_pos, y, 20, 20)

            # Verifica clique no "X"
            if remove_rect.collidepoint(pos):
                self.invited_players.remove(player)
                break

    def draw_players_matrix_for_removal(self):
        """Desenha os jogadores com um 'X' para remoção."""
        x_start = self.screen.get_width() / 10
        y_start = 200
        row_height = 50
        col_width = self.screen.get_width() / 5
        hitbox_padding_x = 20
        hitbox_padding_y = 10
        border_radius = 15
        dark_blue = (0, 51, 102)

        for i, player in enumerate(self.invited_players):
            x = x_start + (i % 5) * col_width
            y = y_start + (i // 5) * row_height
            player_surface = self.font.render(player, True, WHITE)
            text_width, text_height = player_surface.get_size()

            # Desenha hitbox ao redor do nome
            player_rect = pygame.Rect(
                x - hitbox_padding_x // 2,
                y - hitbox_padding_y // 2,
                text_width + hitbox_padding_x,
                text_height + hitbox_padding_y
            )
            pygame.draw.rect(self.screen, dark_blue, player_rect, width=2, border_radius=border_radius)
            self.screen.blit(player_surface, (player_rect.x + hitbox_padding_x // 2, player_rect.y + hitbox_padding_y // 2))

            # Desenha o "X" ao lado do nome
            remove_x_pos = x + text_width + hitbox_padding_x
            remove_surface = self.font.render("X", True, RED)
            self.screen.blit(remove_surface, (remove_x_pos, y))

    def draw_input_box(self):
        """Desenha a caixa de entrada de texto com cursor piscante."""
        input_box = pygame.Rect(self.screen.get_width() / 2 - 150, 100, 300, 40)
        pygame.draw.rect(self.screen, BLUE_GRAY, input_box, border_radius=15, width=2)
        txt_surface = self.font.render(self.new_name, True, BLACK)
        self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        # Desenha o cursor piscante
        if self.cursor_visible:
            cursor_x = input_box.x + txt_surface.get_width() + 5
            cursor_y = input_box.y + 5
            pygame.draw.rect(self.screen, BLACK, (cursor_x, cursor_y, 2, self.font.get_height()))

    def draw_players_matrix(self):
        """Desenha os jogadores adicionados com hitboxes."""
        x_start = self.screen.get_width() / 10
        y_start = 200
        row_height = 50
        col_width = self.screen.get_width() / 5
        hitbox_padding_x = 20
        hitbox_padding_y = 10
        border_radius = 15
        dark_blue = (0, 51, 102)
    
        for i, player in enumerate(self.invited_players):
            # Calcula a posição X e Y de cada jogador
            x = x_start + (i % 5) * col_width
            y = y_start + (i // 5) * row_height
            
            player_surface = self.font.render(player, True, WHITE)
            text_width, text_height = player_surface.get_size()
    
            # Cria o retângulo da hitbox ao redor do nome do jogador
            player_rect = pygame.Rect(
                x - hitbox_padding_x // 2,
                y - hitbox_padding_y // 2,
                text_width + hitbox_padding_x,
                text_height + hitbox_padding_y
            )
    
            # Desenha a hitbox com a cor normal (azul escuro)
            pygame.draw.rect(self.screen, dark_blue, player_rect, width=2, border_radius=border_radius)
    
            # Se o jogador estiver selecionado para edição, altera a cor da hitbox para vermelho
            if self.is_editing and player == self.selected_player:
                pygame.draw.rect(self.screen, RED, player_rect, width=2, border_radius=border_radius)
    
            # Desenha o nome do jogador dentro da hitbox
            self.screen.blit(player_surface, (player_rect.x + hitbox_padding_x // 2, player_rect.y + hitbox_padding_y // 2))
    

    def check_select_click(self, pos):
        """Verifica se o jogador clicou no nome de um jogador para editar."""
        x_start = self.screen.get_width() / 10
        y_start = 200
        row_height = 50
        col_width = self.screen.get_width() / 5

        for i, player in enumerate(self.invited_players):
            x = x_start + (i % 5) * col_width
            y = y_start + (i // 5) * row_height
            player_surface = self.font.render(player, True, WHITE)
            text_width, text_height = player_surface.get_size()

            player_rect = pygame.Rect(
                x - 20 // 2,
                y - 10 // 2,
                text_width + 20,
                text_height + 10
            )

            # Se clicar no nome do jogador, preenche o campo com o nome atual para edição
            if player_rect.collidepoint(pos):
                self.selected_player = player
                self.new_name = player
                self.confirm_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() - 150, 200, 50, "Confirmar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

    def update(self):
        """Atualiza a lógica da tela e o cursor piscante."""
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
