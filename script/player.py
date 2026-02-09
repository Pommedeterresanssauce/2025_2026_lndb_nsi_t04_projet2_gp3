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
        self.actions = ['Check', 'Bet', 'Call', 'Raise', 'Fold']

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
        pygame.draw.rect(screen, (46, 82, 58), (1150, 657, 250, 410))
        pygame.draw.rect(screen, (104, 157, 113), (1155, 662, 240, 400))
        text_surface = self.font.render('ACTIONS', True, (255, 255, 255))
        screen.blit(text_surface, (1167, 666))
        

    def draw_action_buttons(self, screen, possible_actions) :
            mouse_pos = pygame.mouse.get_pos()

            for button in self.action_buttons :
                is_available = button['name'] in possible_actions
                hovering = button['rect'].collidepoint(mouse_pos) and is_available # Le hover n'est actif que si l'action est possible
                button['hovered'] = hovering

                # --- SIZE ANIMATION ---
                target_size = self.button_hover_size if hovering else self.button_base_size
                button['size'] += (target_size - button['size']) * 0.15

                # --- COLOR ANIMATION ---
                if not is_available :
                    target_color = (100, 100, 100) # Gris si indisponible
                elif hovering:
                    target_color = self.button_hover_color
                else :
                    target_color = self.button_color
                    
                new_color = []
                for i in range(3) :
                    value = button['current_color'][i] + (target_color[i] - button['current_color'][i]) * 0.15
                    new_color.append(int(value))
                button['current_color'] = new_color

                # Update rect size
                center = button['rect'].center
                button['rect'].size = button['size']
                button['rect'].center = center

                # --- DRAW SHADOW ---
                shadow_rect = button['rect'].copy()
                shadow_rect.y += 4
                shadow_color = (10, 60, 30) if is_available else (50, 50, 50)
                pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=14)

                # --- DRAW BUTTON ---
                pygame.draw.rect(screen, button['current_color'], button['rect'], border_radius=14) 

                # --- DRAW TEXT ---
                text_color = (240, 255, 245) if is_available else (180, 180, 180) # Texte légèrement plus sombre si désactivé
                text_surface = self.font.render(button['name'], True, text_color)
                text_rect = text_surface.get_rect(center=button['rect'].center)
                screen.blit(text_surface, text_rect)


    def action_check(self, table) :
        table.player_turn_done = True
        print('CHECK')


    def action_call(self, table) :
        table.player_turn_done = True
        print('CALL')


    def action_bet(self, table) :
        table.player_turn_done = True
        print('BET')


    def action_raise(self, table) :
        table.player_turn_done = True
        print('RAISE')


    def action_fold(self, table) :
        table.player_turn_done = True
        table.players.remove(self)
        table.active_player_indice -= 1
        print('FOLD')
    
    
    def handle_action_input(self, possible_actions, table) :
            # mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = table.mouse_clicked

            if mouse_pressed :
                for button in self.action_buttons :
                    if button['hovered'] and button['name'] in possible_actions:
                        action_name = button['callback']
                        action_method = getattr(self, f'action_{action_name}', None)
                        if action_method :
                            action_method(table)


    def update(self, screen, possible_actions, table) :
        self.draw_menu_rect(screen)
        self.draw_action_buttons(screen, possible_actions)
        self.handle_action_input(possible_actions, table)