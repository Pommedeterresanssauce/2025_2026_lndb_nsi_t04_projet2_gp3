import pygame

class Player : 
    def __init__(self) :
        self.hand = []
        
        # --- IMAGES ---
        self.card1_image = None
        self.card2_image = None
        self.card1_dimension = [140, 192]
        self.card2_dimension = [140, 192]
        self.card1_pos = [800, 890]
        self.card2_pos = [970, 890]
        
        
    def draw(self, screen) :
        mouse_pos = pygame.mouse.get_pos()
        card1_rect = self.card1_image.get_rect(topleft = self.card1_pos)
        card2_rect = self.card2_image.get_rect(topleft = self.card2_pos)
        
        if card1_rect.collidepoint(mouse_pos) :
            if self.card1_pos[1] > 860 :
                # self.card1_pos = [self.card1_pos[0] - 2, self.card1_pos[1] - 2]
                self.card1_pos[1] -= 2
        else :
            self.card1_pos = [800, 890]
        
        if card2_rect.collidepoint(mouse_pos) :
            if self.card2_pos[1] > 860 :
                # self.card2_pos = [self.card2_pos[0] + 2, self.card2_pos[1] - 2]  
                self.card2_pos[1] -= 2
        else :
            self.card2_pos = [970, 890]
        
        screen.blit(self.card1_image, self.card1_pos)
        screen.blit(self.card2_image, self.card2_pos)


    def update(self) :
        pass