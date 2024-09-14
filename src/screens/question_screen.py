# question_screen.py
import pygame
import random
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM

class QuestionScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.players = self.game.player_manager.active_players[:]  # Usando jogadores ativos
        self.question_order = self.players[:]  # Garante que todos perguntem e respondam
        self.current_pair = None
        self.asked_pairs = []  # Mantém o controle de quem já perguntou e respondeu

        # Botão "Próximo" para avançar para a próxima pergunta
        self.next_button = Button(self.screen.get_width() / 2 - 50, self.screen.get_height() / 2 + 100, 100, 50, "Próximo", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

        self.next_pair()  # Sorteia a primeira dupla de jogadores

    def next_pair(self):
        # Se não houver jogadores suficientes ou todos já perguntaram e responderam
        if len(self.question_order) < 2:
            self.game.show_voting_screen()
            return

        # Sorteia o próximo par de jogadores que ainda não perguntaram e responderam
        while True:
            player1, player2 = random.sample(self.question_order, 2)

            # Verifica se esse par já foi usado (evita repetição)
            if (player1, player2) not in self.asked_pairs and (player2, player1) not in self.asked_pairs:
                break

        # Armazena o par atual que já fez uma pergunta
        self.asked_pairs.append((player1, player2))

        # Remove os jogadores da ordem para garantir que todos participem
        self.question_order.remove(player1)
        self.question_order.remove(player2)

        # Define o par atual
        self.current_pair = (player1, player2)

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)

        if self.current_pair:
            question_text = f"{self.current_pair[0].name} pergunta para {self.current_pair[1].name}"
            self.game.draw_text(question_text, self.screen.get_width() / 2, self.screen.get_height() / 2 - 50, font_size=36)

        self.next_button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_button.is_clicked(event):
                if len(self.question_order) >= 2:
                    self.next_pair()  # Avança para a próxima dupla de jogadores
                else:
                    self.game.show_voting_screen()  # Quando todos já perguntaram e responderam, avança para a votação

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
