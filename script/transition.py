import pygame

class CircleTransition :
    def __init__(self, radius, speed, action_to_do) :
        self.display_surface = pygame.display.get_surface()
        self.beginning_radius = radius
        self.radius = radius
        self.speed = speed
        self.action_to_do = action_to_do
        self.state = 'appearing'
       
    
    def draw(self) :
        w, h = self.display_surface.get_size()
        
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        mask.fill((0, 0, 0))
        
        pygame.draw.circle(mask, (0, 0, 0, 0), (w // 2, h // 2), int(self.radius))
        self.display_surface.blit(mask, (0, 0))


    def update(self, dt, table) :
        if self.state == 'appearing' :
            self.radius -= self.speed * dt
            if self.radius <= 0 :
                self.state = 'disappearing'
                self.action_to_do()
    
        else :
            self.radius += self.speed * dt
            if self.radius >= self.beginning_radius :
                table.actual_transition = None
                table.transition_in_progress = False
                
        self.draw()