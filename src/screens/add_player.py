class AddPlayer:
    def __init__(self, invited_players):
        self.invited_players = invited_players

    def add_player(self, player_name):
        """Adiciona um jogador à lista temporária de convidados."""
        if player_name and player_name.strip():  # Certifica-se de que o nome não está vazio
            new_player_name = player_name.strip()
            self.invited_players.append(new_player_name)  # Adiciona o jogador à lista
        else:
            print("Nome do jogador não pode estar vazio.")
