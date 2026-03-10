import pygame

class Item():
    def __init__(self,name, image):
        self.name = name
        self.image = image

    def use(self,player):
        print(f"Item {self.name} used")

class Potion(Item):
    def use(self, player):
        player.pv = min(player.max_pv, player.pv + 20)
        print("Vous récupérez 20 PV")


class Key(Item):
    def __init__(self, name, key_id, image_path=None):
        super().__init__(name, image_path)
        self.key_id = key_id