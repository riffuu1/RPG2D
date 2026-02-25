import os
import sys
import pygame_menu



#----------------------
# Start game
#----------------------



#----------------------
# Menu principal
#----------------------
def create_menu(screen, FONT, BIG_FONT):
    custom_theme = pygame_menu.Theme(
        title_font=pygame_menu.font.FONT_FRANCHISE,
        title_font_size=60,
        title_font_color=(255, 255, 255),
        background_color=(20, 20, 40),
        widget_font=pygame_menu.font.FONT_FIRACODE,
        widget_font_color=(255, 255, 255),
        widget_font_size=40,
        selection_color=(0, 150, 255),
        widget_padding=25,
    )

    menu = pygame_menu.Menu(
        "Aurore Et Le Tresor d'Aurore",
        screen.get_width() * 0.7,
        screen.get_height() * 0.7,
        theme=custom_theme
    )
    menu.add.button("New Game", on_new_game)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    return menu