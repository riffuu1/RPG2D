import pygame
from player import Player
from enemies import Enemy
from map import *


pygame.init()


# ======================
# La fenêtre
#=======================
Width, Height = 960,540
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Aurore et le trésore de l'aurore")

#=====================
# Background
#======================
background_house = pygame.image.load('assets/Background/House.png')
background_house = pygame.transform.scale(background_house, (Width, Height))
background_house_outside = pygame.image.load('assets/Background/map_1.png')
background_house_outside = pygame.transform.scale(background_house_outside, (Width, Height))
background_map_2 = pygame.image.load('assets/Background/map_2.png')
background_map_2 = pygame.transform.scale(background_map_2, (Width, Height))
background_chest_1 = pygame.image.load('assets/Background/map_chest_1.png')
background_chest_1 = pygame.transform.scale(background_chest_1, (Width, Height))


#=====================
# Collision
#=====================
obstacle_color = [(0,0,0)]

#=================
# Le joueur
#=================
dossier_perso = "./assets/Joueur"
player = Player(screen, dossier_perso)


#====================
# L'ennemi
#====================
image_path = "assets/Ennemies/ghost.png"
enemy_1 = Enemy(screen,"ghost", image_path,34,56,100)
#======================
# La Map de base
#=====================
map4 = Map(800,600,background_house,"map_4",[])
map1 = Map(800,600,background_house_outside,"map_1",[])
map2 = Map(800,600,background_map_2,"map_2",[])
map3 = Map(800,600,background_chest_1,"map_3",[])
maps = [map1,map2,map3,map4]

current_map = map4


#======================
# Boucle Principale
#======================



clock = pygame.time.Clock()
running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    old_pos = player.rect.topleft



    player.update(keys,current_map.get_surface(), current_map.objects)
    print(player.rect.topleft)
    player.limit_movements(Width, Height)
    current_map = Map.switch_map(current_map,player,map1,map2,map3,map4)


    current_map.draw(screen)
    player.draw()
    player.show_pv()






    pygame.display.flip()
    clock.tick(60)

pygame.quit()
