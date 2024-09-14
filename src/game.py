import pygame
from .player import PlayerManager
from .ui import Button
from .screen_manager import ScreenManager
from .admin import Admin
from .screens.question_screen import QuestionScreen

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
        self.players = []  # Lista de jogadores adicionados
        self.categories = {
            "Comidas": ["Pizza", "Hambúrguer", "Sushi", "Salada", "Sorvete", "Lasagna", "Batata Frita", "Tacos", "Macarrão",
                        "Curry", "Panqueca", "Burrito", "Ramen", "Nhoque", "Frango Assado", "Hot Dog", "Cuscuz", "Bolo", 
                        "Sanduíche", "Croissant", "Queijo", "Arroz", "Feijão", "Camarão", "Torta", "Steak", "Brigadeiro", 
                        "Pão de Queijo", "Risoto", "Ceviche", "Yakissoba", "Churrasco", "Paella", "Tapioca", "Goulash", 
                        "Salmão", "Sopa", "Empadão", "Schnitzel", "Frango Frito", "Omelete", "Massa", "Polenta", "Pamonha",
                        "Pastel", "Moqueca", "Quiche", "Escondidinho", "Vatapá", "Polvo", "Sardinha"],
            "Filmes": ["Inception", "Titanic", "Avatar", "The Matrix", "Gladiator", "Forrest Gump", "O Poderoso Chefão",
                        "Jurassic Park", "Star Wars", "The Dark Knight", "Pulp Fiction", "Os Vingadores", "Clube da Luta",
                        "Toy Story", "De Volta para o Futuro", "O Senhor dos Anéis", "Harry Potter", "Indiana Jones", 
                        "O Exorcista", "Psicose", "Rocky", "E.T.", "O Iluminado", "Coringa", "Logan", "Pantera Negra",
                        "Mulher Maravilha", "Parasita", "A Origem", "O Rei Leão", "Braveheart", "O Grande Gatsby", 
                        "Interstellar", "Mad Max", "O Lobo de Wall Street", "Moulin Rouge", "Cisne Negro", "Django Livre", 
                        "Matrix Reloaded", "The Revenant", "The Departed", "12 Homens e uma Sentença", "Os Sete Samurais", 
                        "Cidadão Kane", "A Lista de Schindler", "O Pianista", "Ratatouille", "V de Vingança", "Jogos Vorazes", "Frozen"],
            "Animais": ["Elefante", "Tigre", "Golfinho", "Canguru", "Pinguim", "Leão", "Girafa", "Urso", "Zebra", "Cavalo",
                        "Rinoceronte", "Hipopótamo", "Cervo", "Lobo", "Raposa", "Águia", "Coruja", "Jacaré", "Cobra", 
                        "Tartaruga", "Sapo", "Panda", "Cachorro", "Gato", "Papagaio", "Leopardo", "Crocodilo",
                        "Falcão", "Bicho Preguiça", "Guaxinim", "Macaco", "Vaca", "Porco", "Ovelha", "Pato", "Galinha",
                        "Cisne", "Coelho", "Touro", "Tubarão", "Água-viva", "Caranguejo", "Baleia", "Orca", "Foca", 
                        "Urso Polar", "Flamingo", "Peixe", "Aranha"],
            "Países": ["Brasil", "Argentina", "Estados Unidos", "Canadá", "México", "Japão", "China", "Alemanha", "França", 
                        "Itália", "Espanha", "Portugal", "Reino Unido", "Austrália", "Índia", "África do Sul", "Egito", 
                        "Rússia", "Nova Zelândia", "Suécia", "Noruega", "Finlândia", "Dinamarca", "Holanda", "Bélgica", 
                        "Suíça", "Áustria", "Turquia", "Grécia", "Israel", "Arábia Saudita", "Irã", "Iraque", "Coreia do Sul", 
                        "Coreia do Norte", "Tailândia", "Filipinas", "Vietnã", "Indonésia", "Paquistão", "Afeganistão", 
                        "Malásia", "Cingapura", "Ucrânia", "Polônia", "Hungria", "Cuba", "Venezuela", "Colômbia", "Chile", "Peru"],
            "Esportes": ["Futebol", "Basquete", "Vôlei", "Tênis", "Golfe", "Rugby", "Críquete", "Beisebol", "Futebol Americano",
                        "Handebol", "Atletismo", "Natação", "Boxe", "Ciclismo", "Ginástica", "Judô", "Taekwondo", "Karatê", 
                        "Esgrima", "Hipismo", "Surfe", "Skate", "Snowboard", "Patinação no Gelo", "Esqui", "Luta Greco-Romana",
                        "Levantamento de Peso", "Badminton", "Squash", "Tênis de Mesa", "Xadrez", "Arco e Flecha", "Tiro Esportivo",
                        "Pentatlo Moderno", "Canoagem", "Remo", "Vela", "MMA", "Wrestling", "Basquete 3x3", "Hóquei no Gelo",
                        "Hóquei de Campo", "Polo Aquático", "Mountain Bike", "Triatlo", "Kickboxing", "Curling", "Lacrosse",
                        "Boliche", "Peteca"]
        }
        self.selected_category = None
        self.selected_object = None 
        self.player_manager = PlayerManager()
        self.player_manager.active_players = self.players[:]  # Carrega os jogadores no início
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
        if self.selected_category is None:
            self.screen_manager.show_choose_theme_screen()
        else:
            self.screen_manager.show_player_word_screen(self.player_manager.active_players)

    def show_player_words(self, players):
        if players:
            self.screen_manager.show_player_word_screen(players)
        else:
            print("Nenhum jogador foi adicionado.")


    def start_round(self):
        self.player_manager.reset_active_players()  # Reseta a lista de jogadores ativos antes de começar uma nova rodada
        self.screen_manager.show_question_screen()

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

    def show_choose_theme(self):
        """Função que navega para a tela de escolha de temas."""
        self.screen_manager.show_choose_theme_screen()

    def show_question_screen(self, players=None):
        """Mostra a tela de perguntas entre os jogadores."""
        if not players:
            players = self.player_manager.active_players  # Use os jogadores ativos se a lista não for fornecida

        if not players:
            print("Erro: Nenhum jogador ativo disponível.")
            return

        # Garante que há pelo menos dois jogadores
        if len(players) < 2:
            print("Erro: É necessário pelo menos dois jogadores.")
            return

        self.screen_manager.current_screen = QuestionScreen(self)
