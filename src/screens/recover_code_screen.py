import pygame
from ..ui import Button
from ..constants import WHITE, BLUE_GRAY, DARK_BLUE_GRAY, GRADIENT_TOP, GRADIENT_BOTTOM

class RecoverCodeScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = self.game.font

        self.nickname_box = pygame.Rect(self.screen.get_width() / 2 - 150, self.screen.get_height() / 2 - 80, 300, 40)
        self.password_box = pygame.Rect(self.screen.get_width() / 2 - 150, self.screen.get_height() / 2, 300, 40)

        self.recover_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 80, 200, 50, "Recuperar Código", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=25)

        # Botão "Ok" (inicialmente escondido)
        self.ok_button = Button(self.screen.get_width() / 2 - 75, self.screen.get_height() / 2 + 160, 150, 40, "Ok", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

        # Alterando a visibilidade do botão "Voltar" (vai mostrar quando o código for gerado)
        self.back_button = Button(self.screen.get_width() / 2 - 75, self.screen.get_height() / 2 + 160, 150, 40, "Voltar", self.font, BLUE_GRAY, DARK_BLUE_GRAY, corner_radius=15)

        # Estado do campo de entrada
        self.active_nickname = False
        self.active_password = False
        self.nickname = ''
        self.password = ''

        # Estado para exibir o código recuperado
        self.show_code = False
        self.recovered_code = ""

        # Configurações do cursor piscante
        self.cursor_visible_nickname = True
        self.cursor_visible_password = True
        self.cursor_timer_nickname = pygame.time.get_ticks()
        self.cursor_timer_password = pygame.time.get_ticks()
        self.cursor_interval = 500  # Intervalo para alternar o cursor piscante

    def draw(self):
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)
        self.game.draw_text('Digite seu nickname:', self.screen.get_width() / 2, self.screen.get_height() / 2 - 100, font_size=36, color=WHITE)
        self.game.draw_text('Digite sua senha:', self.screen.get_width() / 2, self.screen.get_height() / 2 - 20, font_size=36, color=WHITE)

        # Desenha o input de nickname
        nickname_surf = self.font.render(self.nickname, True, WHITE)
        self.screen.blit(nickname_surf, (self.nickname_box.x + 5, self.nickname_box.y + 5))
        pygame.draw.rect(self.screen, WHITE if self.active_nickname else BLUE_GRAY, self.nickname_box, border_radius=15, width=2)

        # Desenha o cursor piscante para nickname
        if self.active_nickname and self.cursor_visible_nickname:
            cursor_pos = self.nickname_box.x + 5 + nickname_surf.get_width()
            pygame.draw.line(self.screen, WHITE, (cursor_pos, self.nickname_box.y + 5), (cursor_pos, self.nickname_box.y + 35), 2)

        # Desenha o input de senha
        password_surf = self.font.render('*' * len(self.password), True, WHITE)
        self.screen.blit(password_surf, (self.password_box.x + 5, self.password_box.y + 5))
        pygame.draw.rect(self.screen, WHITE if self.active_password else BLUE_GRAY, self.password_box, border_radius=15, width=2)

        # Desenha o cursor piscante para senha
        if self.active_password and self.cursor_visible_password:
            cursor_pos = self.password_box.x + 5 + password_surf.get_width()
            pygame.draw.line(self.screen, WHITE, (cursor_pos, self.password_box.y + 5), (cursor_pos, self.password_box.y + 35), 2)

        if self.show_code:
            # Se o código foi recuperado, mostrar ele na tela
            self.game.draw_text(f"Novo código: {self.recovered_code}", self.screen.get_width() / 2, self.screen.get_height() / 2 + 50, font_size=28, color=WHITE)
            self.ok_button.draw(self.screen)  # Mostrar botão "Ok"
        else:
            self.recover_button.draw(self.screen)  # Mostrar botão "Recuperar Código"

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.nickname_box.collidepoint(event.pos):
                self.active_nickname = True
                self.active_password = False
            elif self.password_box.collidepoint(event.pos):
                self.active_password = True
                self.active_nickname = False
            else:
                self.active_nickname = False
                self.active_password = False

            if not self.show_code and self.recover_button.is_clicked(event):
                self.recover_code()

            if self.show_code and self.ok_button.is_clicked(event):
                self.game.screen_manager.show_login_screen()

        elif event.type == pygame.KEYDOWN:
            if self.active_nickname:
                if event.key == pygame.K_RETURN:
                    self.active_nickname = False
                elif event.key == pygame.K_BACKSPACE:
                    self.nickname = self.nickname[:-1]
                else:
                    self.nickname += event.unicode
            elif self.active_password:
                if event.key == pygame.K_RETURN:
                    self.active_password = False
                elif event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode

    def update(self):
        # Atualiza o estado do cursor piscante
        current_time = pygame.time.get_ticks()

        # Alterna o estado de visibilidade do cursor para nickname
        if current_time - self.cursor_timer_nickname > self.cursor_interval:
            self.cursor_visible_nickname = not self.cursor_visible_nickname
            self.cursor_timer_nickname = current_time

        # Alterna o estado de visibilidade do cursor para senha
        if current_time - self.cursor_timer_password > self.cursor_interval:
            self.cursor_visible_password = not self.cursor_visible_password
            self.cursor_timer_password = current_time

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

    def recover_code(self):
        """Lógica para recuperação do código."""
        player = self.game.player_manager.get_player_by_name(self.nickname)
        if player and player.password == self.password:
            self.recovered_code = self.game.player_manager.generate_new_code(player)
            self.game.player_manager.save_players()
            self.show_code = True
        else:
            print("Nickname ou senha incorretos!")