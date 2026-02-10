import pygame
from player import Player
from enemies import Enemy

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
enemy_1 = Enemy(screen,"ghost", image_path,34,56,100)

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

    for color in obstacle_color:
        if player.detect_collision_color(backround, color, Width, Height):
            player.rect.topleft = old_pos  # Remettre à l'ancienne position si il y a une collision
            break

    player.update(keys)
    player.limit_movements(Width, Height)

    player.draw()
    player.show_pv()

    enemy_1.draw()
    enemy_1.move(player)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
