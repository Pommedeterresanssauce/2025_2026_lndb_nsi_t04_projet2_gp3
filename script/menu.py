import pygame
from table import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.is_open = True

        # --- FOND ---
        self.background_rect = screen.get_rect()
        self.background_color = (25, 120, 50)  # vert table de poker

        # --- TITLE --- 
        self.title_font = pygame.font.Font("graphics/ui/font.ttf", 64)
        self.title_text = "POKER 2"
        self.title_color = (215, 180, 90)      # doré
        self.title_bg_color = (150, 30, 30)    # rouge casino

        self.title_surface = self.title_font.render(self.title_text, True, self.title_color)
        self.title_rect = self.title_surface.get_rect()

        padding_x = 30
        padding_y = 15

        self.title_bg_rect = pygame.Rect(
            0,
            0,
            self.title_rect.width + padding_x * 2,
            self.title_rect.height + padding_y * 2
        )

        self.title_bg_rect.midtop = (self.screen.get_width() // 2, 20)
        self.title_rect.center = self.title_bg_rect.center
        self.title_border_radius = 14

        # --- BUTTON ---
        self.button_base_size = pygame.Vector2(260, 80)
        self.button_hover_size = pygame.Vector2(280, 90)
        self.button_size = self.button_base_size.copy()

        self.button_color = (40, 170, 90)
        self.button_hover_color = (60, 200, 120)
        self.button_current_color = self.button_color

        self.button_rect = pygame.Rect(0, 0, *self.button_size)
        self.button_rect.center = self.screen.get_rect().center

        self.border_radius = 18

        # self.font = pygame.font.SysFont(None, 36)
        self.font = pygame.font.Font("graphics/ui/font.ttf", 36)


    def handle_input(self) :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        hovering = self.button_rect.collidepoint(mouse_pos)

        # Size animation
        if hovering :
            target_size = self.button_hover_size
        else :
            target_size = self.button_base_size
        self.button_size += (target_size - self.button_size) * 0.15

        # Color animation
        target_color = self.button_hover_color if hovering else self.button_color
        new_color = []
        for i in range(3) :
            value = self.button_current_color[i] + (target_color[i] - self.button_current_color[i]) * 0.15
            new_color.append(int(value))
        self.button_current_color = new_color

        # Center the button after resize
        self.button_rect.size = self.button_size
        self.button_rect.center = self.screen.get_rect().center

        if hovering and mouse_pressed:
            self.is_open = False


    def draw(self) :
        # Fond
        pygame.draw.rect(self.screen, self.background_color, self.background_rect)

        # --- TITLE ---
        pygame.draw.rect(
            self.screen,
            self.title_bg_color,
            self.title_bg_rect,
            border_radius=self.title_border_radius
        )
        self.screen.blit(self.title_surface, self.title_rect)

        # --- BUTTON SHADOW ---
        shadow_rect = self.button_rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (10, 60, 30), shadow_rect, border_radius=self.border_radius)

        # --- BUTTON ---
        pygame.draw.rect(
            self.screen,
            self.button_current_color,
            self.button_rect,
            border_radius=self.border_radius
        )

        # button text
        text_surface = self.font.render("JOUER", True, (240, 255, 245))
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)


    def update(self) :
        self.handle_input()
        self.draw()
