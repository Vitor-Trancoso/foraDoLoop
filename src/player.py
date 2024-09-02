import json

class Player:
    def __init__(self, name, password="", access_code="", score=0):
        self.name = name
        self.password = password
        self.access_code = access_code
        self.score = score
        self.is_out_of_the_loop = False
        self.secret_word = None

class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, name, password="", access_code="", score=0):
        """Adiciona um novo jogador à lista de jogadores."""
        player = Player(name, password, access_code, score)
        self.players.append(player)
        self.save_players()  # Salva jogadores após adicionar

    def validate_login(self, access_code):
        """Valida se o código de acesso fornecido corresponde a algum jogador registrado."""
        for player in self.players:
            if player.access_code == access_code:
                return True
        return False

    def remove_player(self, name):
        """Remove um jogador pelo nome."""
        self.players = [player for player in self.players if player.name != name]
        self.save_players()

    def update_player_name(self, old_name, new_name):
        """Atualiza o nome de um jogador."""
        for player in self.players:
            if player.name == old_name:
                player.name = new_name
                self.save_players()
                return True
        return False

    def get_all_players(self):
        """Retorna a lista de todos os jogadores."""
        return self.players

    def save_players(self, filename='players.json'):
        """Salva a lista de jogadores em um arquivo JSON."""
        players_data = [{
            'name': player.name,
            'password': player.password,
            'access_code': player.access_code,
            'score': player.score
        } for player in self.players]
        with open(filename, 'w') as f:
            json.dump(players_data, f)

    def load_players(self, filename='players.json'):
        """Carrega a lista de jogadores de um arquivo JSON."""
        try:
            with open(filename, 'r') as f:
                players_data = json.load(f)
                self.players = [Player(data['name'], data['password'], data['access_code'], data['score']) for data in players_data]
        except FileNotFoundError:
            self.players = []
