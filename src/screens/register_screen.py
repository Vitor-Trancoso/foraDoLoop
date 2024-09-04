# src/screens/register_screen.py

import pygame
from ..ui import Button
from ..constants import WHITE, GRADIENT_TOP, GRADIENT_BOTTOM, MINT_GREEN, SKY_BLUE, BLUE_GRAY, BLACK

class RegisterScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.show_code_button = False
        self.access_code = ''

        # Definindo as caixas de input e botões
        self.nickname_box = pygame.Rect(self.screen.get_width() / 2 - 150, self.screen.get_height() / 2 - 80, 300, 40)
        self.password_box = pygame.Rect(self.screen.get_width() / 2 - 150, self.screen.get_height() / 2 + 10, 300, 40)
        self.register_button = Button(self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 + 80, 200, 50, "Registrar-se", self.font, BLUE_GRAY, BLACK, corner_radius=25)
        self.ok_button = Button(self.screen.get_width() / 2 - 75, self.screen.get_height() / 2 + 180, 150, 40, "Ok", self.font, MINT_GREEN, SKY_BLUE, corner_radius=15)

        # Alterando a posição do botão "Voltar" para um pouco mais acima
        self.back_button = Button(self.screen.get_width() / 2 - 75, self.screen.get_height() / 2 + 180, 150, 40, "Voltar", self.font, BLUE_GRAY, BLACK, corner_radius=15)

        # Estados de input e cursores
        self.active_nickname = False
        self.active_password = False
        self.nickname = ''
        self.password = ''
        self.cursor_visible_nickname = True
        self.cursor_visible_password = True
        self.cursor_timer_nickname = pygame.time.get_ticks()
        self.cursor_timer_password = pygame.time.get_ticks()
        self.cursor_interval = 500

    def draw(self):
        # Desenha o background com gradiente
        self.draw_gradient_background(GRADIENT_TOP, GRADIENT_BOTTOM)
        self.draw_text('Digite seu nickname:', self.screen.get_width() / 2, self.screen.get_height() / 2 - 100, font_size=36, color=WHITE)
        self.draw_text('Digite sua senha:', self.screen.get_width() / 2, self.screen.get_height() / 2 - 11, font_size=36, color=WHITE)

        # Desenha o input do nickname
        nickname_surf = self.font.render(self.nickname, True, WHITE)
        self.screen.blit(nickname_surf, (self.nickname_box.x + 5, self.nickname_box.y + 5))
        pygame.draw.rect(self.screen, WHITE if self.active_nickname else BLUE_GRAY, self.nickname_box, border_radius=15, width=2)

        # Desenha o cursor piscante na caixa de nickname
        if self.active_nickname and self.cursor_visible_nickname:
            cursor_pos = self.nickname_box.x + 5 + nickname_surf.get_width()
            pygame.draw.line(self.screen, WHITE, (cursor_pos, self.nickname_box.y + 5), (cursor_pos, self.nickname_box.y + 35), 2)

        # Desenha o input da senha
        password_surf = self.font.render('*' * len(self.password), True, WHITE)
        self.screen.blit(password_surf, (self.password_box.x + 5, self.password_box.y + 5))
        pygame.draw.rect(self.screen, WHITE if self.active_password else BLUE_GRAY, self.password_box, border_radius=15, width=2)

        # Desenha o cursor piscante na caixa de senha
        if self.active_password and self.cursor_visible_password:
            cursor_pos = self.password_box.x + 5 + password_surf.get_width()
            pygame.draw.line(self.screen, WHITE, (cursor_pos, self.password_box.y + 5), (cursor_pos, self.password_box.y + 35), 2)

        # Desenha botões
        self.register_button.draw(self.screen)
        if self.show_code_button:
            self.draw_text(f'Registrado! Seu código é: {self.access_code}', self.screen.get_width() / 2, self.screen.get_height() / 2 + 150, font_size=24, color=MINT_GREEN)
            self.ok_button.draw(self.screen)
        else:
            self.back_button.draw(self.screen)

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

            if self.register_button.is_clicked(event):
                if self.nickname and self.password:
                    self.access_code = self.game.player_manager.register_player(self.nickname, self.password)
                    self.show_code_button = True

            if not self.show_code_button and self.back_button.is_clicked(event):
                self.game.screen_manager.show_login_screen()

            if self.show_code_button and self.ok_button.is_clicked(event):
                self.show_code_button = False
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
        current_time = pygame.time.get_ticks()
        # Alternar a visibilidade do cursor para nickname
        if current_time - self.cursor_timer_nickname > self.cursor_interval:
            self.cursor_timer_nickname = current_time
            self.cursor_visible_nickname = not self.cursor_visible_nickname
        
        # Alternar a visibilidade do cursor para senha
        if current_time - self.cursor_timer_password > self.cursor_interval:
            self.cursor_timer_password = current_time
            self.cursor_visible_password = not self.cursor_visible_password

    def draw_gradient_background(self, color_top, color_bottom):
        for y in range(self.screen.get_height()):
            ratio = y / self.screen.get_height()
            color = (
                int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio),
                int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio),
                int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))

    def draw_text(self, text, x, y, font_size=36, color=WHITE):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
