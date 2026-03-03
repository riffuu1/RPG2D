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
            enemy.draw(screen)

    @staticmethod
    def switch_map(current_map,player,map1,map2,map3,House):
        # Sortie à gauche
        if player.rect.x ==0:
            if current_map == map1:
                player.rect.x = map2.width - player.rect.width
                return map2


        # Sortie à droite
        elif player.rect.x == 800:
            if current_map == map2:
                player.rect.x = 0
                return map1

        #Sortie en haut
        elif player.rect.y ==0:
            if current_map == map2:
                player.rect.y = 410
                return map3

        #Sortie en bas
        elif player.rect.y  == 412:
            if current_map == House:
                player.rect.y = 300
                return map1
            if current_map == map3:
                player.rect.y = 0
                return map2
        return current_map

    def get_surface(self):
        return self.bg_image