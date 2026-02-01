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


    def update(self) :
        pass