import pygame
from Item import Item, Potion, Weapon
from DamageEffect import DamageEffect
from enemies import Enemy
from collision_player import *

class Player:
    def __init__(self, screen, player_folder, hp=100):
        self.screen = screen
        self.start_x = 200
        self.start_y = 150
        self.hp = hp
        self.max_hp = hp
        self.inventory = []
        self.equipped_weapon = None
        self.attack_cooldown = 300  # ms
        self.last_attack_time = 0
        self.effects = []
        self.damage_image = None  # to assign from main.py

        self.x = self.start_x
        self.y = self.start_y
        self.speed = 2
        self.rect = pygame.Rect(self.x, self.y, 128, 128)
        self.hitbox = pygame.Rect(self.rect.x + 40, self.rect.y + 70, 48, 50)
        self.feet = pygame.Rect(self.x + 54, self.y + 118, 20, 10)

        self.frame_index = 0
        self.frame_speed = 0.05
        self.last_direction = "front"

        # Animations
        self.animations = {
            "idle_left": self.load_animation(player_folder, ["left.png"]),
            "idle_right": self.load_animation(player_folder, ["right.png"]),
            "idle_front": self.load_animation(player_folder, ["front.png"]),
            "idle_back": self.load_animation(player_folder, ["back.png"]),
            "walk_left": self.load_animation(player_folder, ["Walk_left_1.png","left.png","Walk_left_2.png","left.png"]),
            "walk_right": self.load_animation(player_folder, ["Walk_right_1.png","right.png","Walk_right_2.png","right.png"]),
            "walk_up": self.load_animation(player_folder, ["Walk_up_1.png","Walk_up_2.png"]),
            "walk_down": self.load_animation(player_folder, ["Walk_down_1.png","Walk_down_2.png"]),
        }
        self.current_animation = self.animations["idle_front"]

    # ---------------- Animations ----------------
    def load_animation(self, folder, image_names, size=(128,128)):
        frames = []
        for name in image_names:
            path = f"{folder}/{name}"
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, size)
            frames.append(image)
        return frames

    def get_frame(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.current_animation):
            self.frame_index = 0
        return self.current_animation[int(self.frame_index)]

    # ---------------- Collisions ----------------
    def feet_collision(self, surface, objects, enemies):
        px, py = self.feet.center
        # Color collision
        if check_collision_with_color(surface, px, py):
            return True
        # Object collision
        for obj in objects:
            if self.feet.colliderect(obj.rect):
                return True
        # Enemy collision
        for enemy in enemies:
            if isinstance(enemy, Enemy) and enemy.active and self.hitbox.colliderect(enemy.hitbox):
                return True
        return False

    # ---------------- Movement & Attacks ----------------
    def update(self, keys, map_surface, map_objects, enemies):
        old_x, old_y = self.rect.x, self.rect.y
        in_movement = False

        # --- Vertical movement ---
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.current_animation = self.animations["walk_up"]
            self.last_direction = "back"
            in_movement = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            self.current_animation = self.animations["walk_down"]
            self.last_direction = "front"
            in_movement = True

        self.hitbox.y = self.rect.y + 70
        self.feet.y = self.rect.y + 118

        # Collision Y → rollback
        if self.feet_collision(map_surface, map_objects, enemies):
            self.rect.y = old_y
            self.hitbox.y = old_y + 70
            self.feet.y = old_y + 118

        # --- Horizontal movement ---
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.current_animation = self.animations["walk_left"]
            self.last_direction = "left"
            in_movement = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.current_animation = self.animations["walk_right"]
            self.last_direction = "right"
            in_movement = True

        self.hitbox.x = self.rect.x + 40
        self.feet.x = self.rect.x + 54

        # Collision X → rollback
        if self.feet_collision(map_surface, map_objects, enemies):
            self.rect.x = old_x
            self.hitbox.x = old_x + 40
            self.feet.x = old_x + 54

        if not in_movement:
            self.current_animation = self.animations[f"idle_{self.last_direction}"]

        # --- Attack ---
        if keys[pygame.K_x]:
            self.attack(enemies)

    # ---------------- HP ----------------
    def show_hp(self):
        font = pygame.font.Font(None, 36)
        hp_text = font.render(f"HP: {self.hp}", True, (255, 255, 255))
        bar_x, bar_y = 20, 20
        bar_width, bar_height = 200, 20
        pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        hp_width = int((self.hp / self.max_hp) * bar_width)
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, hp_width, bar_height))
        self.screen.blit(hp_text, (bar_x, bar_y))

    # ---------------- Inventory ----------------
    def add_item(self, item: Item):
        if item not in self.inventory:
            self.inventory.append(item)
            print(f"{item.name} added to inventory")

    def remove_item(self, item: Item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{item.name} removed from inventory")

    def equip_item(self, item: Item):
        if isinstance(item, Weapon):
            if self.equipped_weapon == item:
                self.equipped_weapon = None
                print(f"{item.name} unequipped")
            else:
                self.equipped_weapon = item
                print(f"{item.name} equipped")

    def use_item(self, item: Item):
        item.use(self)
        if isinstance(item, Potion):
            self.remove_item(item)

    # ---------------- Attack ----------------
    def attack(self, enemies):
        if not self.equipped_weapon or not self.damage_image:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time < self.attack_cooldown:
            return
        self.last_attack_time = current_time

        attack_range = 50
        attack_rect = self.hitbox.copy()
        if self.last_direction == "front":
            attack_rect.y += attack_range
            effect_x, effect_y, angle = attack_rect.centerx, attack_rect.top, -90
        elif self.last_direction == "back":
            attack_rect.y -= attack_range
            effect_x, effect_y, angle = attack_rect.centerx, attack_rect.bottom, 90
        elif self.last_direction == "left":
            attack_rect.x -= attack_range
            effect_x, effect_y, angle = attack_rect.right, attack_rect.centery, 180
        elif self.last_direction == "right":
            attack_rect.x += attack_range
            effect_x, effect_y, angle = attack_rect.left, attack_rect.centery, 0

        # Apply Damage
        for enemy in enemies:
            if enemy.active and attack_rect.colliderect(enemy.hitbox):
                enemy.hp -= self.equipped_weapon.damage
                print(f"{enemy.name} takes {self.equipped_weapon.damage} damage")
                if enemy.hp <= 0:
                    enemy.active = False

        # Visual Effect
        rotated_image = pygame.transform.rotate(self.damage_image, angle)
        effect = DamageEffect(effect_x - rotated_image.get_width()//2,
                              effect_y - rotated_image.get_height()//2,
                              rotated_image)
        self.effects.append(effect)

    # ---------------- Draw ----------------
    def draw(self):
        self.screen.blit(self.get_frame(), self.rect)
        for effect in self.effects:
            effect.draw(self.screen)
        self.effects = [e for e in self.effects if not e.is_finished()]