# admin.py

class Admin:
    def __init__(self, admin_code="1234"):
        self.admin_code = admin_code

    def is_admin(self, code):
        """Verifica se o código fornecido corresponde ao código do administrador."""
        return code == self.admin_code

    def remove_player(self, player_manager, player_name):
        """Remove um jogador da lista de jogadores pelo nome."""
        player_manager.players = [player for player in player_manager.players if player.name != player_name]

    def edit_player(self, player_manager, player_name, new_name=None, new_password=None):
        """Edita o nome ou senha de um jogador."""
        for player in player_manager.players:
            if player.name == player_name:
                if new_name:
                    player.name = new_name
                if new_password:
                    player.password = new_password
