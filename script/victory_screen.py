import pygame

class VictoryScreen :
    def __init__(self, screen, winner) :
        self.screen = screen
        self.winner = winner
        self.is_open = True

        # --- FOND ---
        self.background_rect = screen.get_rect()
        self.background_color = (25, 120, 50)  # vert table de poker

        # --- TITLE --- 
        self.title_font = pygame.font.Font("graphics/ui/font.ttf", 80)
        self.subtitle_font = pygame.font.Font("graphics/ui/font.ttf", 48)
        
        if winner.type == 'player' :
            self.title_text = "VICTORY!"
            self.subtitle_text = "YOU WIN THE GAME!"
        else :
            self.title_text = "GAME OVER"
            self.subtitle_text = f"{self.get_bot_name()} WINS!"
        
        self.title_color = (215, 180, 90)      # doré
        self.title_bg_color = (150, 30, 30)    # rouge casino
        
        # Title surface
        self.title_surface = self.title_font.render(self.title_text, True, self.title_color)
        self.title_rect = self.title_surface.get_rect()
        
        # Subtitle surface
        self.subtitle_surface = self.subtitle_font.render(self.subtitle_text, True, (255, 255, 255))
        self.subtitle_rect = self.subtitle_surface.get_rect()

        # Title background
        padding_x = 40
        padding_y = 20
        self.title_bg_rect = pygame.Rect(
            0, 0, 
            max(self.title_rect.width, self.subtitle_rect.width) + padding_x * 2, 
            self.title_rect.height + self.subtitle_rect.height + padding_y * 3
        )

        self.title_bg_rect.midtop = (self.screen.get_width() // 2, 50)
        self.title_rect.midtop = (self.title_bg_rect.centerx, self.title_bg_rect.top + padding_y)
        self.subtitle_rect.midtop = (self.title_bg_rect.centerx, self.title_rect.bottom + padding_y // 2)
        self.title_border_radius = 14

        # --- IMAGE DU GAGNANT ---
        if winner.type == 'bot' :
            # Pour un bot, on utilise son image
            self.winner_image = winner.image
            self.winner_image = pygame.transform.scale(self.winner_image, (300, 300))
        else :
            # Pour le joueur, on crée une image avec du texte
            self.winner_image = self.create_player_victory_image()
        
        self.winner_image_rect = self.winner_image.get_rect()
        self.winner_image_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50)

        # --- STATISTIQUES ---
        self.stats_font = pygame.font.Font("graphics/ui/font.ttf", 36)
        self.stats_text = f"Final Chips : {winner.chip_number}"
        self.stats_surface = self.stats_font.render(self.stats_text, True, (255, 255, 255))
        self.stats_rect = self.stats_surface.get_rect()
        self.stats_rect.midtop = (self.screen.get_width() // 2, self.winner_image_rect.bottom + 30)

        # --- BOUTONS ---
        self.button_base_size = pygame.Vector2(280, 80)
        self.button_hover_size = pygame.Vector2(300, 90)
        
        self.button_color = (40, 170, 90)
        self.button_hover_color = (60, 200, 120)

        # Bouton "Rejouer"
        self.replay_button_size = self.button_base_size.copy()
        self.replay_button_color = self.button_color
        self.replay_button_rect = pygame.Rect(0, 0, *self.replay_button_size)
        self.replay_button_rect.center = (self.screen.get_width() // 2 - 160, self.screen.get_height() - 100)

        # Bouton "Quitter"
        self.quit_button_size = self.button_base_size.copy()
        self.quit_button_color = self.button_color
        self.quit_button_rect = pygame.Rect(0, 0, *self.quit_button_size)
        self.quit_button_rect.center = (self.screen.get_width() // 2 + 160, self.screen.get_height() - 100)

        self.border_radius = 18
        self.font = pygame.font.Font("graphics/ui/font.ttf", 40)


    def get_bot_name(self) :
        """Extrait le nom du bot depuis son image path ou retourne un nom par défaut."""
        if hasattr(self.winner, 'image') :
            # Essayer d'extraire le nom depuis le chemin de l'image
            # Par exemple : 'graphics/bot/eliott.jpg' -> 'Eliott'
            try :
                # Cette partie dépend de comment les bots sont nommés
                return "THE BOT"
            except :
                return "THE BOT"
        return "THE BOT"


    def create_player_victory_image(self) :
        """Crée une image de victoire pour le joueur humain."""
        # Créer une surface avec fond transparent
        image = pygame.Surface((300, 300), pygame.SRCALPHA)
        
        # Dessiner un cercle doré
        pygame.draw.circle(image, (215, 180, 90), (150, 150), 140)
        pygame.draw.circle(image, (180, 140, 50), (150, 150), 130)
        
        # Dessiner une couronne ou étoile
        star_font = pygame.font.Font("graphics/ui/font.ttf", 120)
        star_text = "★"
        star_surface = star_font.render(star_text, True, (255, 215, 0))
        star_rect = star_surface.get_rect(center=(150, 150))
        image.blit(star_surface, star_rect)
        
        return image


    def handle_input(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            mouse_pos = pygame.mouse.get_pos()
            
            if self.replay_button_rect.collidepoint(mouse_pos) :
                return 'replay'
            elif self.quit_button_rect.collidepoint(mouse_pos) :
                return 'quit'
        
        return None


    def update_buttons(self) :
        mouse_pos = pygame.mouse.get_pos()

        # Replay button
        hovering_replay = self.replay_button_rect.collidepoint(mouse_pos)
        target_size_replay = self.button_hover_size if hovering_replay else self.button_base_size
        self.replay_button_size += (target_size_replay - self.replay_button_size) * 0.15

        target_color_replay = self.button_hover_color if hovering_replay else self.button_color
        new_color_replay = []
        for i in range(3) :
            value = self.replay_button_color[i] + (target_color_replay[i] - self.replay_button_color[i]) * 0.15
            new_color_replay.append(int(value))
        self.replay_button_color = new_color_replay

        center = self.replay_button_rect.center
        self.replay_button_rect.size = self.replay_button_size
        self.replay_button_rect.center = center

        # Quit button
        hovering_quit = self.quit_button_rect.collidepoint(mouse_pos)
        target_size_quit = self.button_hover_size if hovering_quit else self.button_base_size
        self.quit_button_size += (target_size_quit - self.quit_button_size) * 0.15

        target_color_quit = self.button_hover_color if hovering_quit else self.button_color
        new_color_quit = []
        for i in range(3) :
            value = self.quit_button_color[i] + (target_color_quit[i] - self.quit_button_color[i]) * 0.15
            new_color_quit.append(int(value))
        self.quit_button_color = new_color_quit

        center = self.quit_button_rect.center
        self.quit_button_rect.size = self.quit_button_size
        self.quit_button_rect.center = center


    def draw(self) :
        # Fond
        pygame.draw.rect(self.screen, self.background_color, self.background_rect)

        # --- TITLE BACKGROUND ---
        pygame.draw.rect(
            self.screen,
            self.title_bg_color,
            self.title_bg_rect,
            border_radius=self.title_border_radius
        )
        
        # --- TITLE ---
        self.screen.blit(self.title_surface, self.title_rect)
        
        # --- SUBTITLE ---
        self.screen.blit(self.subtitle_surface, self.subtitle_rect)

        # --- WINNER IMAGE ---
        self.screen.blit(self.winner_image, self.winner_image_rect)

        # --- STATS ---
        self.screen.blit(self.stats_surface, self.stats_rect)

        # --- REPLAY BUTTON ---
        # Shadow
        shadow_rect = self.replay_button_rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (10, 60, 30), shadow_rect, border_radius=self.border_radius)
        # Button
        pygame.draw.rect(
            self.screen,
            self.replay_button_color,
            self.replay_button_rect,
            border_radius=self.border_radius
        )
        # Text
        text_surface = self.font.render("REJOUER", True, (240, 255, 245))
        text_rect = text_surface.get_rect(center=self.replay_button_rect.center)
        self.screen.blit(text_surface, text_rect)

        # --- QUIT BUTTON ---
        # Shadow
        shadow_rect = self.quit_button_rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (10, 60, 30), shadow_rect, border_radius=self.border_radius)
        # Button
        pygame.draw.rect(
            self.screen,
            self.quit_button_color,
            self.quit_button_rect,
            border_radius=self.border_radius
        )
        # Text
        text_surface = self.font.render("QUITTER", True, (240, 255, 245))
        text_rect = text_surface.get_rect(center=self.quit_button_rect.center)
        self.screen.blit(text_surface, text_rect)


    def update(self) :
        self.update_buttons()
        self.draw()