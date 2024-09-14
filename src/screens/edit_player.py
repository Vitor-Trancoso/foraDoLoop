class EditPlayer:
    def __init__(self, invited_players):
        self.invited_players = invited_players

    def edit_player(self, old_name, new_name):
        """Edita o nome de um jogador na lista temporária de convidados."""
        if old_name in self.invited_players and new_name and new_name.strip():
            player_index = self.invited_players.index(old_name)
            self.invited_players[player_index] = new_name.strip()
        else:
            print("Nome inválido ou jogador não encontrado.")
