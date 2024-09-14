# ui.py
import pygame

BLACK = (0, 0, 0)

def draw_rounded_rect(surface, rect, color, corner_radius, border_width=0, border_color=None):
    x, y, width, height = rect
    if border_width > 0 and border_color:
        outer_rect = pygame.Rect(x - border_width, y - border_width, width + 2 * border_width, height + 2 * border_width)
        draw_rounded_rect(surface, outer_rect, border_color, corner_radius + border_width)

    pygame.draw.rect(surface, color, (x + corner_radius, y, width - 2 * corner_radius, height))
    pygame.draw.rect(surface, color, (x, y + corner_radius, width, height - 2 * corner_radius))
    pygame.draw.circle(surface, color, (x + corner_radius, y + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (x + width - corner_radius, y + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (x + corner_radius, y + height - corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (x + width - corner_radius, y + height - corner_radius), corner_radius)

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, corner_radius=15, border_width=0, border_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.corner_radius = corner_radius
        self.border_width = border_width
        self.border_color = border_color

    def draw(self, screen):
        draw_rounded_rect(screen, self.rect, self.current_color, self.corner_radius, self.border_width, self.border_color)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        # Reduza o tamanho da fonte, se necessário, ou aumente a largura do botão
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Verifique se o texto cabe dentro do botão, se não ajustar a fonte ou a largura do botão
        if text_rect.width > self.rect.width - 10:  # Subtrair para garantir espaço de preenchimento
            self.font = pygame.font.Font(None, 30)  # Reduzir o tamanho da fonte
        
        screen.blit(text_surf, text_rect)

    def check_for_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
