import pygame
import os

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
        self.hitbox = pygame.Rect(self.rect.x + 40, self.rect.y + 70, 48, 50)
        self.actif = True
        self.attack_cooldown = 1000
        self.last_attack_time = 0

    def draw(self,screen):
        if self.actif:
            self.screen.blit(self.image, self.rect)

#=====================
# With the help of Chat GPT
#======================
    def move(self, player):
        if not self.actif:
            return  # ← Ne fait rien si l'ennemi est mort

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distance = math.hypot(dx, dy)
        if distance == 0:
            return

        if distance <= 200:  # évite division par zéro
            dx /= distance
            dy /= distance

            future_hitbox = self.hitbox.copy()
            future_hitbox.x += dx * self.vitesse
            future_hitbox.y += dy * self.vitesse

            if not future_hitbox.colliderect(player.hitbox):
                self.rect.x += dx * self.vitesse
                self.rect.y += dy * self.vitesse

                self.hitbox.x = self.rect.x + 40
                self.hitbox.y = self.rect.y + 70

            else:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time >= self.attack_cooldown:
                    player.pv -= 10
                    self.last_attack_time = current_time




