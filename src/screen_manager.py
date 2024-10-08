# screen_manager.py
import pygame
from .screens.login_screen import LoginScreen
from .screens.register_screen import RegisterScreen
from .screens.main_menu_screen import MainMenuScreen
from .screens.instructions_screen import InstructionsScreen
from .screens.settings_screen import SettingsScreen
from .screens.credits_screen import CreditsScreen
from .screens.choose_theme_screen import ChooseThemeScreen
from .screens.group_edit_screen import GroupEditScreen  # Tela de edição de grupo
from .screens.question_screen import QuestionScreen
from .screens.voting_screen import VotingScreen
from .screens.player_word_screen import PlayerWordScreen
from .screens.recover_code_screen import RecoverCodeScreen  # Adicione esta linha

class ScreenManager:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.current_screen = None

    def show_login_screen(self):
        self.current_screen = LoginScreen(self.game)

    def show_register_screen(self):
        self.current_screen = RegisterScreen(self.game)

    def show_main_menu(self):
        self.current_screen = MainMenuScreen(self.game)

    def show_instructions(self):
        self.current_screen = InstructionsScreen(self.game)

    def show_settings(self):
        self.current_screen = SettingsScreen(self.game)

    def show_credits(self):
        self.current_screen = CreditsScreen(self.game)

    def show_choose_theme_screen(self):
        self.current_screen = ChooseThemeScreen(self.game)

    def show_player_word_screen(self, players):
        self.current_screen = PlayerWordScreen(self.game, players)


    def show_group_edit_screen(self):
        self.current_screen = GroupEditScreen(self.game)

    def show_question_screen(self):
        self.current_screen = QuestionScreen(self.game)

    def show_voting_screen(self):
        self.current_screen = VotingScreen(self.game)

    def handle_event(self, event):
        if self.current_screen:
            self.current_screen.handle_event(event)

    def update(self):
        if self.current_screen:
            self.current_screen.update()

    def draw(self):
        if self.current_screen:
            self.current_screen.draw()

    def show_recover_code_screen(self):
            """Mostra a tela de recuperação de código."""
            self.current_screen = RecoverCodeScreen(self.game)

