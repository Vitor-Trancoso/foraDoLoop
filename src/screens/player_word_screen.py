import pygame
import random
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM

class PlayerWordScreen:
    def __init__(self, game, players):
        self.game = game
        self.screen = game.screen
        self.font = self.game.font
        self.players = players  # Jogadores ativos

        # Verifica se há jogadores antes de escolher o impostor
        if not self.players:
            # Exibe mensagem de erro e volta para a tela de edição de grupo
            self.game.show_group_edit_screen()
            return

        self.current_player_index = 0  # Índice do jogador atual que verá a tela
        self.impostor = random.choice(self.players)  # Escolhe o impostor aleatoriamente
        self.secret_word = random.choice(self.game.categories[self.game.selected_category])  # Palavra secreta da categoria
        self.show_next_player_screen = False  # Controla quando mostrar a próxima tela

        # Botão "Próximo" para passar para o próximo jogador
        self.next_button = Button(self.screen.get_width() / 2 - 50, self.screen.get_height() / 2 + 100, 100, 50, "Próximo", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)

        current_player = self.players[self.current_player_index]  # Jogador atual

        # Verifica se o jogador atual é o impostor
        if current_player == self.impostor:
            message = f"{current_player}, você é o impostor!"
        else:
            message = f"{current_player}, a palavra secreta é: {self.secret_word}"

        self.game.draw_text(message, self.screen.get_width() / 2, self.screen.get_height() / 2 - 50, font_size=36)

        # Botão para avançar
        self.next_button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_button.is_clicked(event):
                self.show_next_player()

    def show_next_player(self):
        """Mostra a tela para o próximo jogador."""
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            # Todos os jogadores já viram sua palavra ou se são impostores
            self.game.start_round()  # Inicia a rodada de perguntas
        else:
            self.show_next_player_screen = True  # Passa para o próximo jogador

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
