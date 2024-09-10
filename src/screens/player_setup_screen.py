import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM, RED

class PlayerSetupScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(None, 36)

        # Lista temporária de jogadores para a partida
        self.invited_players = []

        # Botão Voltar
        button_width = 200
        button_height = 50
        button_x = (self.screen.get_width() - button_width) / 2
        button_y = self.screen.get_height() - 150
        self.back_button = Button(button_x, button_y, button_width, button_height, "Voltar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

        # Caixa de entrada para nome do jogador
        self.input_box = pygame.Rect(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2, 200, 36)
        self.active = False
        self.color_inactive = BLUE_GRAY
        self.color_active = WHITE
        self.color = self.color_inactive
        self.text = ''

        # Botão "Adicionar Jogador"
        self.add_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 60, 200, 50, "Adicionar Jogador", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

        # Botão "Pronto"
        self.ready_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 130, 200, 50, "Pronto", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

        # Botão "Iniciar Jogo" (exibido depois de clicar em "Pronto")
        self.start_game_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 130, 200, 50, "Iniciar Jogo", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

        # Controla se os jogadores estão prontos
        self.players_ready = False

        # Mensagem de feedback
        self.feedback_message = ""

    def draw(self):
        # Desenha o fundo com gradiente
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)

        # Desenha o texto de instrução
        self.game.draw_text('Digite o nome do jogador:', self.screen.get_width() / 2, self.screen.get_height() / 2 - 50, font_size=36, color=WHITE)

        # Renderiza o texto inserido na caixa de entrada
        txt_surface = self.font.render(self.text, True, WHITE)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.color, self.input_box, border_radius=15, width=2)

        # Desenha botões
        self.add_button.draw(self.screen)

        if not self.players_ready:
            self.ready_button.draw(self.screen)
        else:
            self.start_game_button.draw(self.screen)

        self.back_button.draw(self.screen)

        # Exibe mensagem de feedback, se houver
        if self.feedback_message:
            self.game.draw_text(self.feedback_message, self.screen.get_width() / 2, self.screen.get_height() / 2 + 180, font_size=24, color=RED)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
                self.color = self.color_active if self.active else self.color_inactive
            else:
                self.active = False
                self.color = self.color_inactive

            if not self.players_ready:
                if self.add_button.is_clicked(event):
                    if self.text:
                        self.invited_players.append(self.text)  # Adiciona à lista temporária
                        self.feedback_message = f"Jogador '{self.text}' adicionado!"
                        self.text = ''  # Limpa o texto após adicionar o jogador
                    else:
                        self.feedback_message = "Nome do jogador não pode estar vazio."

                if self.ready_button.is_clicked(event):
                    if len(self.invited_players) < 2:
                        self.feedback_message = "Adicione pelo menos 2 jogadores para iniciar o jogo."
                    else:
                        self.players_ready = True  # Define que os jogadores estão prontos

            if self.start_game_button.is_clicked(event) and self.players_ready:
                self.game.start_round()  # Chama o método para iniciar o jogo

            if self.back_button.is_clicked(event):
                self.game.screen_manager.show_choose_theme()  # Volta para a tela de escolha de tema

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text:
                        self.invited_players.append(self.text)  # Adiciona à lista temporária
                        self.feedback_message = f"Jogador '{self.text}' adicionado!"
                        self.text = ''
                    else:
                        self.feedback_message = "Nome do jogador não pode estar vazio."
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        pass  # Método update vazio para evitar erro

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
