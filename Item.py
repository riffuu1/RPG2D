import pygame

class Item():
    def __init__(self,name, image_path=None):
        self.name = name
        self.image_path = image_path

    def use(self,player):
        print(f"Item {self.name} used")

