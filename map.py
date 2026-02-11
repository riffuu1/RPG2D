import pygame

class Map:
    def __init__(self, width, height,bg_image, bg_name, objects=None,enemies=None):
        self.width = width
        self.height = height
        self.bg_image = bg_image
        self.bg_name = bg_name
        self.objects = objects if objects else []
        self.enemies = enemies if enemies else []

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        for obj in self.objects:
            if hasattr(obj, "active") and not obj.active:
                continue
            obj.draw(screen)
        for enemy in self.enemies:
            if hasattr(enemy, "active") and not enemy.active:
                continue

    def get_surface(self):
        return self.bg_image