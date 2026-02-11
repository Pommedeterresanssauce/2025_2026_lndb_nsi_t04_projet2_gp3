import pygame

class Player : 
    def __init__(self) :
        self.type = 'player'
        self.hand = []
        self.chip_number = 2000
        self.placing_a_bet = False
        
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
        self.chip_font = pygame.font.Font('graphics/ui/font.ttf', 65)
    
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
            
        # --- BET SLIDER ---
        self.bet_min = 0
        self.bet_max = 0
        self.bet_value = 0

        self.slider_rect = pygame.Rect(1180, 850, 200, 10)
        self.slider_handle_rect = pygame.Rect(1180, 842, 14, 26)

        self.slider_hitbox_rect = pygame.Rect( # ZONE DE CLIC LARGE (HITBOX)
            self.slider_rect.x,
            self.slider_rect.y - 20,
            self.slider_rect.width,
            self.slider_rect.height + 40
        )

        self.dragging_slider = False

        self.validate_button_rect = pygame.Rect(1175, 900, 200, 50)
        
        # --- IMAGES ---
        self.card1_image = None
        self.card2_image = None
        self.card1_pos = [800, 890]
        self.card2_pos = [970, 890]
        
        self.stack_1_image = pygame.image.load('graphics/table_de_jeu/coin_stack/1.png').convert_alpha()
        self.stack_1_image = pygame.transform.scale_by(self.stack_1_image, 4)
        self.stack_2_image = pygame.image.load('graphics/table_de_jeu/coin_stack/10.png').convert_alpha()
        self.stack_2_image = pygame.transform.scale_by(self.stack_2_image, 4)
        self.stack_3_image = pygame.image.load('graphics/table_de_jeu/coin_stack/20.png').convert_alpha()
        self.stack_3_image = pygame.transform.scale_by(self.stack_3_image, 4)
        self.stack_4_image = pygame.image.load('graphics/table_de_jeu/coin_stack/100.png').convert_alpha()
        self.stack_4_image = pygame.transform.scale_by(self.stack_4_image, 4)
        
        
    def draw_card_info(self, card_code, screen) :
        name_code = card_code[0] + card_code[1]
        color_code = card_code[2]
        card = str(self.ui_card_name[name_code] + ' de ' + self.ui_card_color[color_code])
        text_surface = self.font.render(card, True, (255, 255, 255))
        screen.blit(text_surface, (100, 950))
        
    
    def draw_stacks(self, screen) :
        screen.blit(self.stack_1_image, (1450, 920))
        screen.blit(self.stack_2_image, (1560, 920))
        screen.blit(self.stack_3_image, (1670, 920))
        screen.blit(self.stack_4_image, (1780, 920))
        
        text_surface = self.font.render('CHIP STACK :', True, (255, 255, 255))
        chip_number_text_surface = self.chip_font.render(str(self.chip_number), True, (255, 255, 255))
        screen.blit(text_surface, (1500, 780))
        screen.blit(chip_number_text_surface, (1560, 830))
        
        
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
        
        self.draw_stacks(screen)


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


    def all_in(self, table) :
        table.pot += self.chip_number
        self.chip_number = 0
        table.player_turn_done = True
        table.round_players.remove(self)


    def action_check(self, table) :
        table.player_turn_done = True


    def action_call(self, table) :
        if self not in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.append(self)
        if self.chip_number >= table.max_bet :
            table.player_turn_done = True
            table.pot += table.max_bet
            self.chip_number -= table.max_bet
            if self.chip_number == 0 :
                table.round_players.remove(self)
        else :
            self.all_in(table)


    def action_bet(self, table) :
        if self not in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.append(self)
        if self.chip_number >= table.max_bet :
            self.placing_a_bet = True
        else :
            self.all_in(table)


    def action_raise(self, table) :
        if self not in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.append(self)
        if self.chip_number > table.max_bet :
            self.placing_a_bet = True
        else :
            self.all_in(table)


    def action_fold(self, table) :
        if self in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.remove(self)
        table.player_turn_done = True
        table.round_players.remove(self)
        table.active_player_indice -= 1
    
    
    def place_a_bet(self, screen, table) :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pressed_once = table.mouse_clicked

        # Initialisation une seule fois
        if self.bet_value == 0 :
            self.bet_min = table.max_bet + 1
            self.bet_max = self.chip_number
            self.bet_value = self.bet_min

        # --- PANEL ---
        pygame.draw.rect(screen, (46, 82, 58), (1150, 657, 250, 410))
        pygame.draw.rect(screen, (104, 157, 113), (1155, 662, 240, 400))

        title = self.font.render('YOUR BET', True, (255, 255, 255))
        screen.blit(title, (1160, 670))

        # --- SLIDER BAR ---
        pygame.draw.rect(screen, (30, 60, 40), self.slider_rect, border_radius=5)

        ratio = (self.bet_value - self.bet_min) / (self.bet_max - self.bet_min)
        self.slider_handle_rect.centerx = self.slider_rect.left + int(ratio * self.slider_rect.width)

        pygame.draw.rect(screen, (200, 230, 210), self.slider_handle_rect, border_radius=6)

        # --- DRAG START ---
        if mouse_pressed and self.slider_hitbox_rect.collidepoint(mouse_pos) :
            self.dragging_slider = True

        # --- DRAG STOP ---
        if not mouse_pressed :
            self.dragging_slider = False

        # --- DRAGGING ---
        if self.dragging_slider :
            x = max(self.slider_rect.left, min(mouse_pos[0], self.slider_rect.right))
            ratio = (x - self.slider_rect.left) / self.slider_rect.width
            self.bet_value = int(self.bet_min + ratio * (self.bet_max - self.bet_min))

        # --- BET VALUE ---
        bet_text = self.font.render(f'Bet: {self.bet_value}', True, (255, 255, 255))
        screen.blit(bet_text, (1155, 800))

        # --- VALIDATE BUTTON ---
        hovering = self.validate_button_rect.collidepoint(mouse_pos)
        color = (60, 200, 120) if hovering else (40, 170, 90)

        pygame.draw.rect(screen, color, self.validate_button_rect, border_radius=14)

        text = self.font.render('VALIDER', True, (240, 255, 245))
        text_rect = text.get_rect(center=self.validate_button_rect.center)
        screen.blit(text, text_rect)

        # --- VALIDATION ---
        if mouse_pressed_once and hovering :
            self.chip_number -= self.bet_value
            table.pot += self.bet_value
            table.max_bet = self.bet_value

            table.player_turn_done = True
            self.placing_a_bet = False
            self.bet_value = 0
            if self.chip_number == 0 :
                table.round_players.remove(self)

    
    def handle_action_input(self, possible_actions, table) :
            # mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = table.mouse_clicked

            if mouse_pressed :
                for button in self.action_buttons :
                    if button['hovered'] and button['name'] in possible_actions :
                        action_name = button['callback']
                        action_method = getattr(self, f'action_{action_name}', None)
                        if action_method :
                            action_method(table)


    def update(self, screen, possible_actions, table) :
        if not self.placing_a_bet :
            self.draw_menu_rect(screen)
            self.draw_action_buttons(screen, possible_actions)
            self.handle_action_input(possible_actions, table)
        else :
            self.place_a_bet(screen, table)