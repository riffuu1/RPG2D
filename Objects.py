import pygame

class Object():
    def __init__(self, x, y, image):
        self.rect = image.get_rect(topleft=(x, y))
        self.image = image
        self.active = True

    def draw(self):
        if self.active:
            self.image.blit(self.image, (self.x, self.y))

    def interact(self):
        pass

class Pickableobject(Object):
    def __init__(self, x, y, image, item_name):
        # Le super sert a prendre les paramètre de la classe parents (self.rect = image.get_rect(topleft=(x, y)), self.image = image, self.active = True
        super().__init__(self,x,y,image)
        self.item_name = item_name

    def interact(self,player,keys):
        if self.rect.colliderect(player.feet):
            if keys[pygame.K_e]:
                player.add_item(self.item_name)
                self.active = False