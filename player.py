import pygame
import os
from collision_player import *
from Item import Item
from enemies import *


class Player:
    def __init__(self,screen, dossier_perso,pv=100):
        self.screen = screen

        self.start_x = 200
        self.start_y = 150
        self.pv = pv
        self.max_pv = pv
        self.inventory = []

        self.x = self.start_x
        self.y = self.start_y

        self.vitesse = 2
        self.rect = pygame.Rect(self.x, self.y, 128,128)

        # With the help of chat Gpt to make it more professional:
        # the +40 is to make the hitbox in the center horizontally
        # the +70 go near to the feet
        # and the 48 and 50 => 48*50 => the size of the body
        self.hitbox = pygame.Rect(self.rect.x + 40,self.rect.y + 70,48,50)


        self.frame_index = 0
        self.frame_speed = 0.05
        self.derniere_direction = "front"
        self.feet = pygame.Rect(self.x + 54, self.y + 118, 20, 10)

        self.animations = {
            "idle_left" : self.charger_animation(dossier_perso, ["left.png"]),
            "idle_right": self.charger_animation(dossier_perso, ["right.png"]),
            "idle_front": self.charger_animation(dossier_perso, ["front.png"]),
            "idle_back": self.charger_animation(dossier_perso, ["back.png"]),

            "walk_left": self.charger_animation(dossier_perso, ["Walk_left_1.png","left.png","Walk_left_2.png","left.png"]),
            "walk_right": self.charger_animation(dossier_perso,["Walk_right_1.png","right.png","Walk_right_2.png","right.png "]),
            "walk_up": self.charger_animation(dossier_perso,["Walk_up_1.png","Walk_up_2.png"]),
            "walk_down":self.charger_animation(dossier_perso,["Walk_down_1.png","Walk_down_2.png"]),
        }

        self.current_animation = self.animations["idle_front"]

    def charger_animation(self, dossier, noms_images, taille=(128,128)):
        frames = []
        for nom in noms_images:
            chemin= os.path.join(dossier, nom)
            image = pygame.image.load(chemin).convert_alpha()
            image = pygame.transform.scale(image, taille)
            frames.append(image)
        return frames

    def limit_movements(self,Width,Height):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Width:
            self.rect.right = Width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Height:
            self.rect.bottom = Height



    def get_frame(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.current_animation):
            self.frame_index = 0
        return self.current_animation[int(self.frame_index)]

    def collision_pieds(self, surface, objects, enemies):
        px, py = self.feet.center

        # Collision par couleur sur la map
        if check_collision_with_color(surface, px, py):
            return True

        # Collision avec les objets
        for obj in objects:
            if self.feet.colliderect(obj.rect):
                return True

        for enemy in enemies:
            if isinstance(enemy, Enemy) and enemy.actif and self.hitbox.colliderect(enemy.hitbox):
                return True

        return False


        #Déplacement
    def update(self,keys, map_surface, map_objects,enemies):

        old_x = self.rect.x
        old_y = self.rect.y
        en_mouvement = False

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.vitesse
            self.current_animation = self.animations["walk_up"]
            self.derniere_direction = "back"
            en_mouvement = True

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.vitesse
            self.current_animation = self.animations["walk_down"]
            self.derniere_direction = "front"
            en_mouvement = True

        self.hitbox.x = self.rect.x+40
        self.hitbox.y = self.rect.y+70

        # update feet
        self.feet.x = self.rect.x + 54
        self.feet.y = self.rect.y + 118

        # collision sur Y → rollback seulement Y
        if self.collision_pieds(map_surface, map_objects,enemies):
            self.rect.y = old_y
            self.hitbox.y = old_y + 70
            self.feet.y = old_y + 118

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.vitesse
            self.current_animation = self.animations["walk_left"]
            self.derniere_direction = "left"
            en_mouvement = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.vitesse
            self.current_animation = self.animations["walk_right"]
            self.derniere_direction = "right"
            en_mouvement = True

        # update feet
        self.feet.x = self.rect.x + 54
        self.feet.y = self.rect.y + 118

        self.hitbox.x = self.rect.x + 40
        self.hitbox.y = self.rect.y + 70

        # collision sur X → rollback seulement X
        if self.collision_pieds(map_surface, map_objects,enemies):
            self.rect.x = old_x
            self.hitbox.x = old_x + 40
            self.feet.x = old_x + 54

        if not en_mouvement:
            self.current_animation = self.animations[f"idle_{self.derniere_direction}"]


    def show_pv(self,):
        font =pygame.font.Font(None,36)
        pv_text = font.render(f"PV: {self.pv}", True, (255,255,255))

        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = 20

        pygame.draw.rect(self.screen, (255,0,0),(bar_x,bar_y,bar_width,bar_height))
        pv_width = int((self.pv / self.max_pv) * bar_width)
        pygame.draw.rect(self.screen,(0,255,0), (bar_x,bar_y,pv_width,bar_height))

        self.screen.blit(pv_text, (bar_x,bar_y))

    def add_item(self,item : Item):
        self.inventory.append(item)

    def remove_item(self,item : Item):
        self.inventory.remove(item)


    def has_item(self,item_class):
        return any(isinstance(i, item_class) for i in self.inventory)


    def draw(self):
        self.screen.blit(self.get_frame(), self.rect)
