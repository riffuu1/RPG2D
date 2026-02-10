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
backround = pygame.image.load('assetes/Background/House.png')
background = pygame.transform.scale(backround, (Width, Height))


#=================
# Le joueur
#=================
dossier_perso = "./assetes/Joueur"
player = Player(screen, dossier_perso)


#====================
# L'ennemi
#====================
image_path = "./assetes/Ennemies/ghost.png"
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
    screen.blit(background, (0, 0))

    player.update(keys)
    player.limit_movements(Width, Height)

    player.draw()
    player.show_pv()

    enemy_1.draw()
    enemy_1.move(player)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
