import pygame
from .player import PlayerManager
from .ui import Button
from .screen_manager import ScreenManager
from .admin import Admin

# Definir cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

class Game:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Out of the Loop")
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.categories = {
            "Comidas": ["Pizza", "Hambúrguer", "Sushi", "Salada", "Sorvete"],
            "Filmes": ["Inception", "Titanic", "Avatar", "The Matrix", "Gladiator"],
            "Animais": ["Elefante", "Tigre", "Golfinho", "Canguru", "Pinguim"]
        }
        self.selected_category = None
        self.player_manager = PlayerManager()  # Carrega os jogadores no início
        self.current_player = None
        self.questions_asked = set()
        self.current_question = None
        self.votes = {}
        self.secret_word = None
        self.impostor = None
        self.admin = Admin()  # Instância para verificar funções de administrador
        self.screen_manager = ScreenManager(self)  # Instância única do ScreenManager

    def draw_text(self, text, x, y, font_size=36, color=BLACK):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        self.player_manager.load_players()  # Certifique-se de carregar jogadores ao iniciar
        self.screen_manager.show_login_screen()  # Mostra a tela inicial
    
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
                self.screen_manager.handle_event(event)  # Gerencia eventos

            self.screen_manager.update()  # Atualiza a lógica
            self.screen.fill((0, 0, 0))  # Limpa a tela
            self.screen_manager.draw()  # Desenha na tela
        
            pygame.display.flip()  # Atualiza a tela

        pygame.quit()

    def show_main_menu(self):
        self.screen_manager.show_main_menu()

    def show_admin_login(self):
        self.screen_manager.show_admin_login()

    def show_group_edit_screen(self):
        self.screen_manager.show_group_edit_screen()  # Mostra a tela de edição de grupo

    def register_screen(self):
        self.screen_manager.show_register_screen()

    def start_game(self):
        self.screen_manager.show_choose_theme()

    def player_setup(self):
        self.screen_manager.show_player_setup()

    def start_round(self):
        self.player_manager.reset_active_players()  # Reseta a lista de jogadores ativos antes de começar uma nova rodada
        self.screen_manager.show_question_screen()

    def show_player_words(self, players):
        self.screen_manager.show_player_words(players)

    def ask_question(self):
        self.screen_manager.ask_question()

    def show_voting_screen(self):
        self.screen_manager.show_voting_screen()

    def reveal_impostor(self):
        self.screen_manager.reveal_impostor()

    def impostor_guess(self):
        self.screen_manager.impostor_guess()

    def reveal_final_result(self, guessed_word):
        self.screen_manager.reveal_final_result(guessed_word)

    def show_instructions(self):
        self.screen_manager.show_instructions()

    def show_settings(self):
        self.screen_manager.show_settings()

    def show_credits(self):
        self.screen_manager.show_credits()

    def exit_game(self):
        self.save_players()
        self.running = False

    def save_players(self):
        self.player_manager.save_players()

    def load_players(self):
        self.player_manager.load_players()
