import pygame

class Map:
    def __init__(self, width, height,bg_image,bg_name):
        self.width = width
        self.height = height
        self.bg_image = bg_image
        self.bg_name = bg_name

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))