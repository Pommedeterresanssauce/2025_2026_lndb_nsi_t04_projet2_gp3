import pygame

class Player : 
    def __init__(self) :
        self.hand = []
        
        # --- UI ---
        self.ui_card_color = {
            'p' : 'pique',
            'c' : 'coeur',
            't' : 'trefle',
            'k' : 'carreau'
        }
        self.ui_card_name = {
            '01' : 'As',
            '02' : '2',
            '03' : '3',
            '04' : '4',
            '05' : '5',
            '06' : '6',
            '07' : '7',
            '08' : '8',
            '09' : '9',
            '10' : '10',
            '11' : 'Valet',
            '12' : 'Dame',
            '13' : 'Roi'
        }
        self.font = pygame.font.Font('graphics/ui/font.ttf', 40)
        
        # --- BUTTON ACTION ---
        self.actions = ['Check', 'Call', 'Bet', 'Raise', 'Fold']

        self.button_base_size = pygame.Vector2(180, 55)
        self.button_hover_size = pygame.Vector2(195, 62)
        self.button_color = (40, 170, 90)
        self.button_hover_color = (60, 200, 120)

        self.action_buttons = []

        start_x = 1185
        start_y = 720
        space_between_button = 65

        for i, action in enumerate(self.actions) :
            rect = pygame.Rect(start_x, start_y + i * space_between_button, self.button_base_size.x, self.button_base_size.y)

            self.action_buttons.append({
                'name' : action,
                'rect' : rect,
                'size' : self.button_base_size.copy(),
                'current_color' : self.button_color,
                'hovered' : False,
                'callback' : action.lower()
            })
        
        # --- IMAGES ---
        self.card1_image = None
        self.card2_image = None
        self.card1_pos = [800, 890]
        self.card2_pos = [970, 890]
        
        
    def draw_card_info(self, card_code, screen) :
        name_code = card_code[0] + card_code[1]
        color_code = card_code[2]
        card = str(self.ui_card_name[name_code] + ' de ' + self.ui_card_color[color_code])
        text_surface = self.font.render(card, True, (255, 255, 255))
        screen.blit(text_surface, (230, 80))
        
        
    def draw(self, screen) :
        mouse_pos = pygame.mouse.get_pos()
        card1_rect = self.card1_image.get_rect(topleft = self.card1_pos)
        card2_rect = self.card2_image.get_rect(topleft = self.card2_pos)
        
        if card1_rect.collidepoint(mouse_pos) :
            if self.card1_pos[1] > 860 :
                self.card1_pos[1] -= 2
            self.draw_card_info(self.hand[0], screen)
        else :
            self.card1_pos = [800, 890]
        
        if card2_rect.collidepoint(mouse_pos) :
            if self.card2_pos[1] > 860 :
                self.card2_pos[1] -= 2
            self.draw_card_info(self.hand[1], screen)
        else :
            self.card2_pos = [970, 890]
        
        screen.blit(self.card1_image, self.card1_pos)
        screen.blit(self.card2_image, self.card2_pos)


    def draw_menu_rect(self, screen) :
        pygame.draw.rect(screen, (46, 82, 58), (1150, 657, 250, 430))
        pygame.draw.rect(screen, (104, 157, 113), (1155, 662, 240, 420))
        text_surface = self.font.render('ACTIONS', True, (255, 255, 255))
        screen.blit(text_surface, (1167, 666))
        

    def draw_action_buttons(self, screen) :
        mouse_pos = pygame.mouse.get_pos()

        for button in self.action_buttons :
            hovering = button["rect"].collidepoint(mouse_pos)
            button["hovered"] = hovering

            # --- SIZE ANIMATION ---
            if hovering :
                target_size = self.button_hover_size
            else :
                target_size = self.button_base_size
            button["size"] += (target_size - button["size"]) * 0.15

            # --- COLOR ANIMATION ---
            if hovering :
                target_color = self.button_hover_color
            else :
                target_color = self.button_color
            new_color = []
            for i in range(3) :
                value = button["current_color"][i] + (target_color[i] - button["current_color"][i]) * 0.15
                new_color.append(int(value))
            button["current_color"] = new_color

            # Update rect size
            center = button["rect"].center
            button["rect"].size = button["size"]
            button["rect"].center = center

            # --- DRAW SHADOW ---
            shadow_rect = button["rect"].copy()
            shadow_rect.y += 4
            pygame.draw.rect(screen, (10, 60, 30), shadow_rect, border_radius=14)

            # --- DRAW BUTTON ---
            pygame.draw.rect(screen, button["current_color"], button["rect"], border_radius=14)

            # --- DRAW TEXT ---
            text_surface = self.font.render(button["name"], True, (240, 255, 245))
            text_rect = text_surface.get_rect(center=button["rect"].center)
            screen.blit(text_surface, text_rect)


    def action_check(self):
        print("CHECK")


    def action_call(self):
        print("CALL")


    def action_bet(self):
        print("BET")


    def action_raise(self):
        print("RAISE")


    def action_fold(self):
        print("FOLD")
    
    
    def handle_action_input(self) :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if mouse_pressed :
            for button in self.action_buttons :
                if button["hovered"] :
                    action_name = button["callback"]
                    action_method = getattr(self, f"action_{action_name}", None)
                    if action_method :
                        action_method()


    def update(self, screen) :
        self.draw_menu_rect(screen)
        self.draw_action_buttons(screen)
        self.handle_action_input()