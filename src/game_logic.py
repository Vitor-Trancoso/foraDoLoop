# src/game_logic.py

import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class GameLogic:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font

    def start_round(self):
        if not self.game.selected_category:
            self.game.start_game()
            return
        
        players = self.game.player_manager.players
        if len(players) < 2:
            self.game.draw_text('Adicione pelo menos 2 jogadores para começar a rodada.', self.screen.get_width()/2, self.screen.get_height()/2, font_size=24, color=RED)
            pygame.display.update()
            pygame.time.wait(2000)
            self.game.player_setup()
            return
        
        impostor_index = random.randint(0, len(players) - 1)
        self.game.secret_word = random.choice(self.game.categories[self.game.selected_category])
        
        for i, player in enumerate(players):
            if i == impostor_index:
                player.is_out_of_the_loop = True
                player.secret_word = "Você é o Impostor!"
                self.game.impostor = player
            else:
                player.secret_word = self.game.secret_word
        
        self.show_player_words(players)

    def show_player_words(self, players):
        for player in players:
            self.show_player_word(player)
        self.ask_question()

    def show_player_word(self, player):
        waiting = True
        while waiting:
            self.screen.fill(WHITE)
            self.game.draw_text(f'{player.name}, pressione Enter para ver sua palavra!', self.screen.get_width()/2, self.screen.get_height()/2 - 100, font_size=28)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
        
        self.screen.fill(WHITE)
        self.game.draw_text(f'{player.secret_word}', self.screen.get_width()/2, self.screen.get_height()/2, font_size=36, color=GREEN)
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

    def ask_question(self):
        players = self.game.player_manager.players
        while True:
            asker = random.choice(players)
            responder = random.choice(players)
            if asker != responder and (asker, responder) not in self.game.questions_asked:
                self.game.questions_asked.add((asker, responder))
                self.game.current_question = (asker, responder)
                break
        
        self.show_question_screen()

    def show_question_screen(self):
        asker, responder = self.game.current_question
        waiting = True
        while waiting:
            self.screen.fill(WHITE)
            self.game.draw_text(f'{asker.name} pergunta para {responder.name}!', self.screen.get_width()/2, self.screen.get_height()/2 - 100, font_size=28)
            self.game.draw_text('Pressione o botão para a próxima pergunta', self.screen.get_width()/2, self.screen.get_height()/2, font_size=24)
            
            self.game.next_button.check_for_hover(pygame.mouse.get_pos())
            self.game.next_button.draw(self.screen)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    waiting = False
                if self.game.next_button.is_clicked(event):
                    if len(self.game.questions_asked) < len(self.game.player_manager.players) * 2:
                        self.ask_question()
                    else:
                        self.start_voting()
                    waiting = False

    def start_voting(self):
        self.game.votes = {player.name: 0 for player in self.game.player_manager.players}
        self.game.current_voter_index = 0
        self.show_voting_screen()

    def show_voting_screen(self):
        players = self.game.player_manager.players
        voter = players[self.game.current_voter_index]
        waiting = True
        while waiting:
            self.screen.fill(WHITE)
            self.game.draw_text(f'{voter.name}, vote em quem você acha que é o impostor:', self.screen.get_width()/2, self.screen.get_height()/2 - 100, font_size=28)
            
            y_offset = 0
            for i, player in enumerate(players):
                self.game.draw_text(f'{i+1}. {player.name}', self.screen.get_width()/2, self.screen.get_height()/2 + y_offset, font_size=24)
                y_offset += 40
            
            self.game.next_button.draw(self.screen)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        choice = event.key - pygame.K_1
                        if choice < len(players):
                            chosen_player = players[choice]
                            self.game.votes[chosen_player.name] += 1
                            waiting = False
                            self.game.current_voter_index += 1
                            if self.game.current_voter_index < len(players):
                                self.show_voting_screen()
                            else:
                                self.reveal_impostor()
                                waiting = False

    def reveal_impostor(self):
        self.screen.fill(WHITE)
        self.game.draw_text(f'O impostor era: {self.game.impostor.name}', self.screen.get_width()/2, self.screen.get_height()/2 - 100, font_size=28)
        self.game.draw_text('Pressione qualquer tecla para continuar.', self.screen.get_width()/2, self.screen.get_height()/2, font_size=24)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    self.impostor_guess()
                    waiting = False

    def impostor_guess(self):
        options = self.game.categories[self.game.selected_category]
        self.screen.fill(WHITE)
        self.game.draw_text(f'{self.game.impostor.name}, tente adivinhar a palavra secreta:', self.screen.get_width()/2, self.screen.get_height()/2 - 100, font_size=28)
        
        y_offset = 0
        for i, word in enumerate(options):
            self.game.draw_text(f'{i+1}. {word}', self.screen.get_width()/2, self.screen.get_height()/2 + y_offset, font_size=24)
            y_offset += 40
        
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        choice = event.key - pygame.K_1
                        if choice < len(options):
                            guessed_word = options[choice]
                            self.reveal_final_result(guessed_word)
                            waiting = False

    def reveal_final_result(self, guessed_word):
        self.screen.fill(WHITE)
        if guessed_word == self.game.secret_word:
            self.game.draw_text(f'Correto! A palavra era {self.game.secret_word}', self.screen.get_width()/2, self.screen.get_height()/2 - 100, font_size=28, color=GREEN)
        else:
            self.game.draw_text(f'Errado! A palavra era {self.game.secret_word}', self.screen.get_width()/2, self.screen.get_height()/2 - 100, font_size=28, color=RED)
        
        self.game.draw_text('Fim do Jogo. Pressione qualquer tecla para sair.', self.screen.get_width()/2, self.screen.get_height()/2, font_size=24)
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    self.game.running = False
                    waiting = False
