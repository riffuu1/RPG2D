import pygame
from player import Player
from enemies import Enemy
from map import Map

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
backround = pygame.image.load('assets/Background/House.png')
background = pygame.transform.scale(backround, (Width, Height))


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

#======================
# La Map de base
#=====================
current_map = Map(800, 600, background, "map1")


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
    screen.blit(background, (0, 0))



    player.update(keys,current_map.get_surface(), current_map.objects)
    player.limit_movements(Width, Height)



    player.draw()
    player.show_pv()



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
