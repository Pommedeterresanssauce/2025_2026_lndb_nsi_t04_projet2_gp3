import pygame

class CircleTransition :
    def __init__(self, radius, speed, action_to_execute) :
        self.display_surface = pygame.display.get_surface()
        self.beginning_radius = radius
        self.radius = radius
        self.speed = speed
        self.action_to_execute = action_to_execute
        self.state = 'appearing'
       
    
    def draw(self) :
        w, h = self.display_surface.get_size()
        
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        mask.fill((0, 0, 0))
        
        pygame.draw.circle(mask, (0, 0, 0, 0), (w // 2, h // 2), int(self.radius))
        self.display_surface.blit(mask, (0, 0))


    def update(self, dt, level) :
        if self.state == 'appearing' :
            self.radius -= self.speed * dt
            if self.radius <= 0 :
                self.state = 'disappearing'
                self.action_to_execute()
                level.sprite_pause = False
    
        else :
            self.radius += self.speed * dt
            if self.radius >= self.beginning_radius :
                level.current_effects.remove(self)
                level.transition_in_progress = False
                
        self.draw()