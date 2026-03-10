import pygame
from Item import Item

class Object():
    def __init__(self, image, x, y):
        self.rect = image.get_rect(topleft=(x, y))
        self.image = image
        self.active = True

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

    def interact(self):
        pass

class PickableObject(Object):
    def __init__(self, x, y, image, item):
        # Le super sert a prendre les paramètre de la classe parents (self.rect = image.get_rect(topleft=(x, y)), self.image = image, self.active = True
        super().__init__(image,x,y)
        self.item = item

    def interact(self, player, e_pressed):
        if self.active and self.rect.colliderect(player.feet) and e_pressed:
            player.add_item(self.item)
            self.active = False