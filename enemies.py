import pygame
import os
from player import Player
import math

class Enemy:
    def __init__(self,screen,name,image_path,x,y,pv):
        self.screen = screen
        self.name = name
        self.pv = pv
        self.vitesse = 1.5
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image,(128,128))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.actif = True

    def draw(self):
        if self.actif:
            self.screen.blit(self.image, self.rect)

#=====================
# Réaliser par Chat GPT
#======================
    def move(self,player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        distance = math.hypot(dx, dy)

        if distance <= 200:  # évite division par zéro
            dx /= distance
            dy /= distance

            self.rect.x += dx * self.vitesse
            self.rect.y += dy * self.vitesse




