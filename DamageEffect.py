import pygame

class DamageEffect:
    def __init__(self, x, y, image, duration=200):
        self.image = image
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_finished(self):
        return pygame.time.get_ticks() - self.start_time > self.duration