class RemovePlayer:
    def __init__(self, invited_players):
        self.invited_players = invited_players

    def remove_player(self, player_name):
        """Remove um jogador da lista de convidados temporários."""
        if player_name in self.invited_players:
            self.invited_players.remove(player_name)
        else:
            print("Jogador não encontrado na lista.")
