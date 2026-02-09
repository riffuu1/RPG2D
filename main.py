import pygame
from player import Player

pygame.init()


# ======================
# La fenêtre
#=======================
Width, Height = 640, 480
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


    player.draw()
    player.show_pv()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
