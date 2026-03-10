import pygame
from player import Player
from enemies import Enemy
from map import *
from Objects import *
from inventory_menu import inventory_menu
from Item import Item, Potion, Key

pygame.init()

# ======================
# Fenêtre
# ======================
Width, Height = 960,540
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Aurore et le trésor de l'aurore")

# ======================
# Background
# ======================
background_house = pygame.image.load('assets/Background/House.png')
background_house = pygame.transform.scale(background_house, (Width, Height))
background_house_outside = pygame.image.load('assets/Background/map_1.png')
background_house_outside = pygame.transform.scale(background_house_outside, (Width, Height))
background_map_2 = pygame.image.load('assets/Background/map_2.png')
background_map_2 = pygame.transform.scale(background_map_2, (Width, Height))
background_chest_1 = pygame.image.load('assets/Background/map_chest_1.png')
background_chest_1 = pygame.transform.scale(background_chest_1, (Width, Height))

# ======================
# Objets décoratifs
# ======================
bed = pygame.image.load('assets/Background/Objects_deco/bed.png')
bed = pygame.transform.scale(bed, (250,250))
shelve = pygame.image.load('assets/Background/Objects_deco/librairie.png')
shelve = pygame.transform.scale(shelve, (250,250))

obj1 = Object(bed,720,50)
obj2 = Object(shelve,0,50)

# ======================
# Joueur
# ======================
folder_player = "./assets/Joueur"
player = Player(screen, folder_player)

# ======================
# Ennemi
# ======================
image_path = "assets/Ennemies/ghost.png"
enemy_1 = Enemy(screen,"ghost", image_path,600,200,100)
enemies = [enemy_1]

# ======================
# Objets ramassables
# ======================
# Exemple : une potion sur la map

potion_image = pygame.image.load("assets/Background/Items/heal potion.png")
potion_image = pygame.transform.scale(potion_image, (50,50))
potion_item = Potion("Potion", potion_image)
pickable_potion = PickableObject(400, 300, potion_image, potion_item)

# ======================
# Maps
# ======================
map4 = Map(800,600,background_house,"map_4",[obj1,obj2],[pickable_potion],[])
map1 = Map(800,600,background_house_outside,"map_1",[],[],[])
map2 = Map(800,600,background_map_2,"map_2",[],[],[enemy_1])
map3 = Map(800,600,background_chest_1,"map_3",[],[],[])
maps = [map1,map2,map3,map4]

current_map = map4

# ======================
# Boucle principale
# ======================
clock = pygame.time.Clock()
running = True

e_pressed = False

while running:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    # Détection appui unique sur E
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                e_pressed = True
            if event.key == pygame.K_i:
                inventory_menu(screen, pygame.font.Font(None,36), player)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                e_pressed = False

    # Mise à jour joueur
    player.update(keys, current_map.get_surface(), current_map.objects, current_map.enemies)

    # Switch de map si besoin
    current_map = Map.switch_map(current_map, player, map1, map2, map3, map4)

    # Interactions avec objets ramassables


    # Dessin de la map
    current_map.draw(screen)

    # Interactions with pickable objects
    for obj in current_map.pickable_objects:
        obj.interact(player, e_pressed)

        # Enemy's moves
    for enemy in current_map.enemies:
        enemy.move(player)

    # draw player and pv
    player.draw()
    player.show_pv()

    # Screen refresh
    pygame.display.flip()
    clock.tick(60)

pygame.quit()