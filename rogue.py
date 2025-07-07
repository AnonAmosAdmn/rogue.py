import pygame
import random
import sys
import math
import base64
from io import BytesIO
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.font.init()

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
GRID_SIZE = 32
FPS = 60

MINIMAP_WIDTH = 300
MINIMAP_HEIGHT = 300
MINIMAP_CELL_SIZE = 5
MINIMAP_POSITION = (SCREEN_WIDTH - MINIMAP_WIDTH - 10, 10)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
PURPLE = (150, 50, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
DARKER_GRAY = (20, 20, 20)
STONE = (120, 120, 120)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Diablo-Style Dungeon Crawler")
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont('Arial', 16)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 32)

def load_base64_image(base64_string, size=(GRID_SIZE, GRID_SIZE)):
    """Load an image from a base64 string and resize it."""
    image_data = base64.b64decode(base64_string)
    image = pygame.image.load(BytesIO(image_data))
    return pygame.transform.scale(image, size)

# Placeholder Base64 images (replace these with your actual Base64 strings)
PLAYER_IMAGE = "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"
GOBLIN_IMAGE = "PLACEHOLDER_GOBLIN_BASE64_STRING"
ORC_IMAGE = "PLACEHOLDER_ORC_BASE64_STRING"
SKELETON_IMAGE = "PLACEHOLDER_SKELETON_BASE64_STRING"
ZOMBIE_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAAUUlEQVR4nGNkSGGgKWCirfGjFoxaMGoBAwMDAwsuif+z/yNzGVMZyVMz9INo6FvAOFpcD38LcOZkZPB/Dk4pRkJpZOgH0dC3YDQnj1owBCwAAJ6ICW7RhODzAAAAAElFTkSuQmCC"
TROLL_IMAGE = "PLACEHOLDER_TROLL_BASE64_STRING"
GHOST_IMAGE = "PLACEHOLDER_GHOST_BASE64_STRING"
HEALTH_POTION_IMAGE = "PLACEHOLDER_HEALTH_POTION_BASE64_STRING"
WEAPON_IMAGE = "PLACEHOLDER_WEAPON_BASE64_STRING"
ARMOR_IMAGE = "PLACEHOLDER_ARMOR_BASE64_STRING"
EXIT_IMAGE = "PLACEHOLDER_EXIT_BASE64_STRING"

class Tile:
    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.type = tile_type  # 0=wall, 1=floor, 2=door
        self.explored = False  # Has this tile ever been seen?
        self.visible = False   # Is this tile currently visible?

class Room:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = (x + w // 2, y + h // 2)
        
    def intersects(self, other):
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)

class Entity:
    def __init__(self, x, y, char, color, name, hp=1, attack=0, defense=0, exp=0):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.alive = True
        self.sprite = None
        
        # Load appropriate sprite based on name
        self.load_sprite()
    
    def load_sprite(self):
        """Load the appropriate sprite based on entity type."""
        try:
            if self.name == "Player":
                self.sprite = load_base64_image(PLAYER_IMAGE)
            elif self.name == "goblin":
                self.sprite = load_base64_image(GOBLIN_IMAGE)
            elif self.name == "orc":
                self.sprite = load_base64_image(ORC_IMAGE)
            elif self.name == "skeleton":
                self.sprite = load_base64_image(SKELETON_IMAGE)
            elif self.name == "zombie":
                self.sprite = load_base64_image(ZOMBIE_IMAGE)
            elif self.name == "troll":
                self.sprite = load_base64_image(TROLL_IMAGE)
            elif self.name == "ghost":
                self.sprite = load_base64_image(GHOST_IMAGE)
            elif self.name == "Health Potion":
                self.sprite = load_base64_image(HEALTH_POTION_IMAGE)
            elif self.name == "Weapon":
                self.sprite = load_base64_image(WEAPON_IMAGE)
            elif self.name == "Armor":
                self.sprite = load_base64_image(ARMOR_IMAGE)
        except:
            # Fallback to colored circle if sprite loading fails
            self.sprite = pygame.Surface((GRID_SIZE, GRID_SIZE))
            self.sprite.fill(BLACK)
            pygame.draw.circle(self.sprite, self.color, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2 - 2)
    
    def draw(self, surface, x, y, size):
        if self.sprite is not None:
            surface.blit(self.sprite, (x, y))
        else:
            # Fallback to character if no sprite
            text = font_medium.render(self.char, True, self.color)
            surface.blit(text, (x, y))

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "@", GREEN, "Player", 30, 8, 5)
        self.level = 1
        self.exp = 0
        self.next_level = 100
        self.vision_radius = 8
        self.crit_chance = 0.1  # 10% chance for critical hit
        self.crit_multiplier = 1.5  # 50% extra damage on crit
    
    def level_up(self):
        self.level += 1
        self.max_hp += 10 + self.level  # More HP at higher levels
        self.hp = self.max_hp
        self.attack += 3 + self.level // 2  # Better attack scaling
        self.defense += 2 + self.level // 3  # Better defense scaling
        self.next_level = self.level * 100
        self.crit_chance = min(0.3, self.crit_chance + 0.02)  # Increase crit chance slightly each level
        return f"Level up! You are now level {self.level}!"

class Game:
    def __init__(self):
        self.map_width = 50
        self.map_height = 50
        self.tiles = [[Tile(x, y, 0) for x in range(self.map_width)] for y in range(self.map_height)]
        self.player = Player(0, 0)  # Initialize player with dummy position
        self.entities = []
        self.items = []
        self.exit_pos = (0, 0)
        self.message = ""
        self.message_time = 0
        self.camera_x = 0
        self.camera_y = 0
        self.game_state = "playing"
        self.dungeon_level = 1
        self.combat_log = []
        self.max_log_entries = 10
        self.generate_dungeon()
    
    def generate_dungeon(self):
        # Reset map to all walls
        self.tiles = [[Tile(x, y, 0) for x in range(self.map_width)] for y in range(self.map_height)]
        self.entities = []
        self.items = []
        self.combat_log = []
        
        # Generate rooms - larger and more at deeper levels
        rooms = []
        max_rooms = 10 + self.dungeon_level  # More rooms at deeper levels
        min_room_size = 5 + self.dungeon_level // 2  # Larger rooms at deeper levels
        max_room_size = 10 + self.dungeon_level // 2
        
        # Ensure room sizes don't exceed map bounds
        min_room_size = min(min_room_size, 15)
        max_room_size = min(max_room_size, 20)
        
        player_placed = False
        
        for _ in range(max_rooms):
            # Random room size and position
            w = random.randint(min_room_size, max_room_size)
            h = random.randint(min_room_size, max_room_size)
            x = random.randint(1, self.map_width - w - 1)
            y = random.randint(1, self.map_height - h - 1)
            
            new_room = Room(x, y, w, h)
            
            # Check for intersections with other rooms
            failed = False
            for other_room in rooms:
                if new_room.intersects(other_room):
                    failed = True
                    break
            
            if not failed:
                # Carve out the room
                self.carve_room(new_room)
                
                # Center coordinates of new room
                (new_x, new_y) = new_room.center
                
                # Place player in first room if not already placed
                if not player_placed:
                    self.player.x, self.player.y = new_x, new_y
                    player_placed = True
                else:
                    # Connect to previous room with a tunnel
                    prev_center = rooms[-1].center
                    
                    # Flip a coin (random number 0 or 1)
                    if random.randint(0, 1) == 1:
                        # First move horizontally, then vertically
                        self.carve_h_tunnel(prev_center[0], new_x, prev_center[1])
                        self.carve_v_tunnel(prev_center[1], new_y, new_x)
                    else:
                        # First move vertically, then horizontally
                        self.carve_v_tunnel(prev_center[1], new_y, prev_center[0])
                        self.carve_h_tunnel(prev_center[0], new_x, new_y)
                
                # Place entities
                self.place_entities(new_room)
                
                # Append the new room to the list
                rooms.append(new_room)
        
        # If no rooms were generated (shouldn't happen), place player at (1,1)
        if not player_placed:
            self.player.x, self.player.y = 1, 1
            self.tiles[1][1].type = 1  # Ensure it's a floor tile
        
        # Place exit in last room if rooms exist
        if rooms:
            last_room = rooms[-1]
            self.exit_pos = last_room.center
            self.tiles[self.exit_pos[1]][self.exit_pos[0]].type = 2  # 2 = exit
        
        # Update FOV after generation
        self.update_fov()
    
    def carve_room(self, room):
        # Set all tiles in the room to floor
        for y in range(room.y + 1, room.y + room.h):
            for x in range(room.x + 1, room.x + room.w):
                self.tiles[y][x].type = 1  # Floor
    
    def carve_h_tunnel(self, x1, x2, y):
        # Horizontal tunnel
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[y][x].type = 1  # Floor
    
    def carve_v_tunnel(self, y1, y2, x):
        # Vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[y][x].type = 1  # Floor
    
    def place_entities(self, room):
        # Place enemies - more enemies and stronger as dungeon level increases
        num_enemies = random.randint(0, 2 + self.dungeon_level // 2)  # More enemies at deeper levels
        
        enemy_types = ["goblin", "orc", "skeleton", "zombie", "troll", "ghost"]
        enemy_chars = ["g", "o", "s", "z", "T", "G"]
        enemy_colors = [GREEN, GREEN, WHITE, WHITE, (0, 150, 0), (150, 150, 255)]
        
        for _ in range(num_enemies):
            # Choose random position in room
            x = random.randint(room.x + 1, room.x + room.w - 1)
            y = random.randint(room.y + 1, room.y + room.h - 1)
            
            # Only place if it's a floor and not occupied by player, exit, or other entities
            if (self.tiles[y][x].type == 1 and 
                not any(e.x == x and e.y == y for e in self.entities) and
                (x, y) != (self.player.x, self.player.y) and
                (x, y) != self.exit_pos):
                enemy_type = random.randint(0, len(enemy_types)-1)
                
                # Base stats + scaling with dungeon level
                hp = random.randint(8, 15) + (self.dungeon_level - 1) * 3
                attack = random.randint(2, 5) + (self.dungeon_level - 1)
                defense = random.randint(0, 2) + (self.dungeon_level - 1) // 2
                exp = random.randint(10, 25) + (self.dungeon_level - 1) * 5
                
                # Special abilities for certain enemies
                special = {}
                if enemy_types[enemy_type] == "troll":
                    hp *= 1.5  # Trolls have more HP
                    special["regeneration"] = True
                elif enemy_types[enemy_type] == "ghost":
                    defense += 2  # Ghosts are harder to hit
                    special["dodge_chance"] = 0.2  # 20% chance to dodge attacks
                
                enemy = Entity(x, y, enemy_chars[enemy_type], enemy_colors[enemy_type], 
                            enemy_types[enemy_type], hp, attack, defense, exp)
                if special:
                    enemy.special = special
                self.entities.append(enemy)
        
        # Place items - better items at deeper levels
        if random.random() < 0.4:  # 40% chance for item
            # Try to find a valid position (up to 10 attempts)
            attempts = 0
            placed = False
            while attempts < 10 and not placed:
                x = random.randint(room.x + 1, room.x + room.w - 1)
                y = random.randint(room.y + 1, room.y + room.h - 1)
                
                # Check if position is valid (floor, not occupied, not player start, not exit)
                if (self.tiles[y][x].type == 1 and 
                    not any(e.x == x and e.y == y for e in self.entities) and
                    not any(i.x == x and i.y == y for i in self.items) and
                    (x, y) != (self.player.x, self.player.y) and
                    (x, y) != self.exit_pos):
                    
                    item_type = random.choice(["health", "weapon", "armor"])
                    
                    if item_type == "health":
                        item = Entity(x, y, "H", RED, "Health Potion")
                        item.effect = "heal"
                        item.amount = random.randint(10, 25) + (self.dungeon_level - 1) * 5
                    elif item_type == "weapon":
                        item = Entity(x, y, "W", BLUE, "Weapon")
                        item.effect = "attack"
                        item.amount = random.randint(1, 3) + (self.dungeon_level - 1)
                    else:  # armor
                        item = Entity(x, y, "A", BLUE, "Armor")
                        item.effect = "defense"
                        item.amount = random.randint(1, 2) + (self.dungeon_level - 1)
                    
                    self.items.append(item)
                    placed = True
                    
                attempts += 1
    
    def update_fov(self):
        # Reset current visibility (but keep explored state)
        for y in range(self.map_height):
            for x in range(self.map_width):
                self.tiles[y][x].visible = False
        
        # Calculate new visibility
        for y in range(max(0, self.player.y - self.player.vision_radius), 
                    min(self.map_height, self.player.y + self.player.vision_radius + 1)):
            for x in range(max(0, self.player.x - self.player.vision_radius), 
                        min(self.map_width, self.player.x + self.player.vision_radius + 1)):
                dx = x - self.player.x
                dy = y - self.player.y
                distance_squared = dx*dx + dy*dy
                
                if distance_squared <= self.player.vision_radius ** 2:
                    # Simple line of sight check
                    visible = True
                    steps = max(abs(dx), abs(dy))
                    
                    if steps > 0:
                        step_x = dx / steps
                        step_y = dy / steps
                        
                        for i in range(1, steps):
                            check_x = int(self.player.x + i * step_x)
                            check_y = int(self.player.y + i * step_y)
                            
                            if (0 <= check_x < self.map_width and 
                                0 <= check_y < self.map_height):
                                if self.tiles[check_y][check_x].type == 0:  # Wall
                                    visible = False
                                    break
                    
                    if visible:
                        self.tiles[y][x].visible = True
                        self.tiles[y][x].explored = True
    
    def update_camera(self):
        # Center camera on player
        self.camera_x = self.player.x * GRID_SIZE - SCREEN_WIDTH // 2
        self.camera_y = self.player.y * GRID_SIZE - SCREEN_HEIGHT // 2
        
        # Clamp camera to map bounds
        max_x = self.map_width * GRID_SIZE - SCREEN_WIDTH
        max_y = self.map_height * GRID_SIZE - SCREEN_HEIGHT
        self.camera_x = max(0, min(self.camera_x, max_x))
        self.camera_y = max(0, min(self.camera_y, max_y))
    
    def move_player(self, dx, dy):
        new_x, new_y = self.player.x + dx, self.player.y + dy
        
        # Check bounds
        if new_x < 0 or new_y < 0 or new_x >= self.map_width or new_y >= self.map_height:
            self.add_message("You can't go that way!")
            return
        
        # Check walls
        if self.tiles[new_y][new_x].type == 0:
            self.add_message("You can't walk through walls!")
            return
        
        # Check exit
        if (new_x, new_y) == self.exit_pos:
            self.dungeon_level += 1
            self.add_message(f"Descending to dungeon level {self.dungeon_level}...")
            self.generate_dungeon()
            self.update_fov()
            return
        
        # Check entities
        for entity in self.entities[:]:
            if (entity.x, entity.y) == (new_x, new_y):
                self.fight(entity)
                return
        
        # Check items
        for item in self.items[:]:
            if (item.x, item.y) == (new_x, new_y):
                self.pick_up_item(item)
                self.player.x, self.player.y = new_x, new_y
                self.update_fov()
                return
        
        # Move player
        self.player.x, self.player.y = new_x, new_y
        self.update_fov()
    
    def fight(self, enemy):
        # Player attacks enemy
        player_damage = self.calculate_damage(self.player, enemy)
        
        # Check for enemy dodge
        if hasattr(enemy, 'special') and 'dodge_chance' in enemy.special:
            if random.random() < enemy.special['dodge_chance']:
                self.add_message(f"{enemy.name} dodged your attack!")
                self.add_to_log(f"{enemy.name} dodged your attack!")
            else:
                enemy.hp -= player_damage
                self.add_message(f"You hit {enemy.name} for {player_damage} damage!")
                self.add_to_log(f"You hit {enemy.name} for {player_damage} damage!")
        else:
            enemy.hp -= player_damage
            self.add_message(f"You hit {enemy.name} for {player_damage} damage!")
            self.add_to_log(f"You hit {enemy.name} for {player_damage} damage!")
        
        if enemy.hp <= 0:
            enemy.alive = False
            self.entities.remove(enemy)
            self.player.exp += enemy.exp
            self.add_message(f"You defeated {enemy.name}! Gained {enemy.exp} XP.")
            self.add_to_log(f"You defeated {enemy.name}! Gained {enemy.exp} XP.")
            
            # Check level up
            if self.player.exp >= self.player.next_level:
                level_up_msg = self.player.level_up()
                self.add_message(level_up_msg)
                self.add_to_log(level_up_msg)
            
            # Move to enemy's position after defeating it
            self.player.x, self.player.y = enemy.x, enemy.y
            self.update_fov()
        else:
            # Enemy attacks player if alive
            if enemy.alive:
                enemy_damage = self.calculate_damage(enemy, self.player)
                self.player.hp -= enemy_damage
                self.add_message(f"{enemy.name} hits you for {enemy_damage} damage!")
                self.add_to_log(f"{enemy.name} hits you for {enemy_damage} damage!")
                
                # Check for enemy regeneration
                if hasattr(enemy, 'special') and 'regeneration' in enemy.special:
                    regen_amount = random.randint(1, 3)
                    enemy.hp = min(enemy.max_hp, enemy.hp + regen_amount)
                    self.add_message(f"{enemy.name} regenerates {regen_amount} HP!")
                    self.add_to_log(f"{enemy.name} regenerates {regen_amount} HP!")
                
                if self.player.hp <= 0:
                    self.game_state = "game_over"
                    self.add_message("You have been defeated! Game Over.")
                    self.add_to_log("You have been defeated! Game Over.")
    
    def calculate_damage(self, attacker, defender):
        # Base damage calculation
        base_damage = max(1, attacker.attack - defender.defense // 2)
        
        # Check for critical hit (player only)
        if attacker == self.player:
            if random.random() < self.player.crit_chance:
                base_damage = int(base_damage * self.player.crit_multiplier)
                self.add_message("Critical hit!")
                self.add_to_log("Critical hit!")
        
        # Add some randomness to damage
        damage = max(1, base_damage + random.randint(-1, 2))
        return damage
    
    def pick_up_item(self, item):
        self.items.remove(item)
        
        if hasattr(item, 'effect'):
            if item.effect == "heal":
                heal_amount = min(item.amount, self.player.max_hp - self.player.hp)
                self.player.hp += heal_amount
                self.add_message(f"You used {item.name} and healed {heal_amount} HP!")
                self.add_to_log(f"You used {item.name} and healed {heal_amount} HP!")
            elif item.effect == "attack":
                self.player.attack += item.amount
                self.add_message(f"You equipped {item.name}! Attack + {item.amount}.")
                self.add_to_log(f"You equipped {item.name}! Attack + {item.amount}.")
            elif item.effect == "defense":
                self.player.defense += item.amount
                self.player.max_hp += item.amount * 2
                self.player.hp += item.amount * 2
                self.add_message(f"You equipped {item.name}! Defense + {item.amount} and max HP + {item.amount * 2}.")
                self.add_to_log(f"You equipped {item.name}! Defense + {item.amount} and max HP + {item.amount * 2}.")
    
    def add_message(self, msg):
        self.message = msg
        self.message_time = pygame.time.get_ticks()
    
    def add_to_log(self, entry):
        # Split multi-line entries and add them in order
        for line in entry.split('\n'):
            self.combat_log.append(line)
        # Trim log if it gets too long
        if len(self.combat_log) > self.max_log_entries:
            self.combat_log = self.combat_log[-self.max_log_entries:]
    
    
    def draw(self):
        # Clear screen
        screen.fill(BLACK)
        
        # Calculate visible area
        start_x = max(0, self.camera_x // GRID_SIZE)
        start_y = max(0, self.camera_y // GRID_SIZE)
        end_x = min(self.map_width, (self.camera_x + SCREEN_WIDTH) // GRID_SIZE + 1)
        end_y = min(self.map_height, (self.camera_y + SCREEN_HEIGHT) // GRID_SIZE + 1)
        
        # Draw map
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                screen_x = x * GRID_SIZE - self.camera_x
                screen_y = y * GRID_SIZE - self.camera_y
                tile = self.tiles[y][x]
                
                if tile.visible:
                    # Currently visible tiles - draw normally
                    if tile.type == 0:  # Wall
                        pygame.draw.rect(screen, STONE, (screen_x, screen_y, GRID_SIZE, GRID_SIZE))
                    elif tile.type == 1:  # Floor
                        pygame.draw.rect(screen, DARK_GRAY, (screen_x, screen_y, GRID_SIZE, GRID_SIZE))
                    elif tile.type == 2:  # Exit
                        # Draw exit with image if available
                        try:
                            exit_img = load_base64_image(EXIT_IMAGE)
                            screen.blit(exit_img, (screen_x, screen_y))
                        except:
                            pygame.draw.rect(screen, YELLOW, (screen_x, screen_y, GRID_SIZE, GRID_SIZE))
                            exit_text = font_medium.render("E", True, BLACK)
                            screen.blit(exit_text, (screen_x, screen_y))
                elif tile.explored:
                    # Previously explored but not currently visible - draw darkened
                    if tile.type == 0:  # Wall
                        pygame.draw.rect(screen, (40, 40, 40), (screen_x, screen_y, GRID_SIZE, GRID_SIZE))
                    elif tile.type == 1:  # Floor
                        pygame.draw.rect(screen, (20, 20, 20), (screen_x, screen_y, GRID_SIZE, GRID_SIZE))
                    elif tile.type == 2:  # Exit
                        pygame.draw.rect(screen, (100, 100, 0), (screen_x, screen_y, GRID_SIZE, GRID_SIZE))
                        exit_text = font_medium.render("E", True, BLACK)
                        screen.blit(exit_text, (screen_x, screen_y))
                elif tile.explored:
                    # Previously explored but not currently visible
                    if tile.type == 0:  # Wall
                        pygame.draw.rect(screen, DARKER_GRAY, (screen_x, screen_y, GRID_SIZE, GRID_SIZE))
                    elif tile.type == 1:  # Floor
                        pygame.draw.rect(screen, BLACK, (screen_x, screen_y, GRID_SIZE, GRID_SIZE))
                        pygame.draw.rect(screen, (10, 10, 10), (screen_x, screen_y, GRID_SIZE, GRID_SIZE), 1)

        # Draw entities and items (only if visible)
        for entity in self.entities:
            if self.tiles[entity.y][entity.x].visible:
                screen_x = entity.x * GRID_SIZE - self.camera_x
                screen_y = entity.y * GRID_SIZE - self.camera_y
                entity.draw(screen, screen_x, screen_y, GRID_SIZE)
        
        for item in self.items:
            if self.tiles[item.y][item.x].visible:
                screen_x = item.x * GRID_SIZE - self.camera_x
                screen_y = item.y * GRID_SIZE - self.camera_y
                item.draw(screen, screen_x, screen_y, GRID_SIZE)
        
        # Draw player
        screen_x = self.player.x * GRID_SIZE - self.camera_x
        screen_y = self.player.y * GRID_SIZE - self.camera_y
        self.player.draw(screen, screen_x, screen_y, GRID_SIZE)
        
        # Draw UI
        self.draw_ui()
        
        # Draw message
        if pygame.time.get_ticks() - self.message_time < 3000:  # Show message for 3 seconds
            msg_surface = font_medium.render(self.message, True, WHITE)
            screen.blit(msg_surface, (10, SCREEN_HEIGHT - 40))
        
        # Draw game over screen
        if self.game_state == "game_over":
            self.draw_game_over()
            
        # Draw minimap
        if self.game_state == "playing":
            self.draw_minimap()
            
        pygame.display.flip()
    
    def draw_ui(self):
        # Draw semi-transparent UI panel
        ui_panel = pygame.Surface((SCREEN_WIDTH, 120), pygame.SRCALPHA)
        ui_panel.fill((0, 0, 0, 180))
        screen.blit(ui_panel, (0, SCREEN_HEIGHT - 120))
        
        # Draw health bar
        health_ratio = self.player.hp / self.player.max_hp
        bar_width = 200
        pygame.draw.rect(screen, DARK_GRAY, (20, SCREEN_HEIGHT - 100, bar_width, 20))
        pygame.draw.rect(screen, GREEN if health_ratio > 0.6 else YELLOW if health_ratio > 0.3 else RED, 
                        (20, SCREEN_HEIGHT - 100, bar_width * health_ratio, 20))
        health_text = font_small.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
        screen.blit(health_text, (25, SCREEN_HEIGHT - 100))
        
        # Draw stats
        stats = [
            f"Level: {self.player.level}",
            f"XP: {self.player.exp}/{self.player.next_level}",
            f"Attack: {self.player.attack}",
            f"Defense: {self.player.defense}",
            f"Dungeon: {self.dungeon_level}",
            f"Crit: {int(self.player.crit_chance*100)}%"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = font_small.render(stat, True, WHITE)
            screen.blit(stat_text, (250 + (i % 2) * 150, SCREEN_HEIGHT - 100 + (i // 2) * 20))
        
        # Draw combat log (now positioned at top left)
        log_panel = pygame.Surface((300, 230), pygame.SRCALPHA)
        log_panel.fill((0, 0, 0, 150))
        screen.blit(log_panel, (10, 10))  # Positioned at top left with 10px padding

        log_title = font_small.render("Combat Log:", True, WHITE)
        screen.blit(log_title, (20, 15))  # Slightly indented from panel edge

        # Display most recent entries in chronological order (oldest at top)
        y_offset = 35  # Start below title
        lines_to_show = min(10, len(self.combat_log))  # Show up to 10 lines
        start_index = max(0, len(self.combat_log) - lines_to_show)  # Start index for last 10 entries

        for i in range(start_index, len(self.combat_log)):
            log_entry = font_small.render(self.combat_log[i], True, WHITE)
            screen.blit(log_entry, (20, y_offset))  # Indented from panel edge
            y_offset += 20
        
        # Draw controls
        controls = font_small.render("WASD: Move     Q: Quit     R: Restart", True, WHITE)
        screen.blit(controls, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 30))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        restart_text = font_medium.render("Press R to restart or Q to quit", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
    
    def draw_minimap(self):
        # Create minimap surface
        minimap = pygame.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT), pygame.SRCALPHA)
        minimap.fill((0, 0, 0, 150))  # Semi-transparent black background
        
        # Calculate visible area on minimap
        start_x = max(0, self.player.x - MINIMAP_WIDTH // (2 * MINIMAP_CELL_SIZE))
        start_y = max(0, self.player.y - MINIMAP_HEIGHT // (2 * MINIMAP_CELL_SIZE))
        end_x = min(self.map_width, start_x + MINIMAP_WIDTH // MINIMAP_CELL_SIZE)
        end_y = min(self.map_height, start_y + MINIMAP_HEIGHT // MINIMAP_CELL_SIZE)
        
        # Draw explored tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.tiles[y][x].explored:
                    # Calculate position on minimap
                    map_x = (x - start_x) * MINIMAP_CELL_SIZE
                    map_y = (y - start_y) * MINIMAP_CELL_SIZE
                    
                    # Choose color based on tile type
                    if self.tiles[y][x].type == 0:  # Wall
                        color = STONE
                    elif self.tiles[y][x].type == 1:  # Floor
                        color = DARK_GRAY
                    elif self.tiles[y][x].type == 2:  # Exit
                        color = YELLOW
                    
                    # Darken if not currently visible
                    if not self.tiles[y][x].visible:
                        color = tuple(c // 2 for c in color)
                    
                    pygame.draw.rect(minimap, color, 
                                    (map_x, map_y, MINIMAP_CELL_SIZE, MINIMAP_CELL_SIZE))
        
        # Draw player position
        player_map_x = (self.player.x - start_x) * MINIMAP_CELL_SIZE
        player_map_y = (self.player.y - start_y) * MINIMAP_CELL_SIZE
        pygame.draw.rect(minimap, GREEN, 
                        (player_map_x, player_map_y, MINIMAP_CELL_SIZE, MINIMAP_CELL_SIZE))
        
        # Draw a border around the minimap
        pygame.draw.rect(minimap, WHITE, (0, 0, MINIMAP_WIDTH, MINIMAP_HEIGHT), 1)
        
        # Blit the minimap to the screen
        screen.blit(minimap, MINIMAP_POSITION)
    
    def run(self):
        running = True
        self.update_fov()

        # Key repeat delay
        move_delay = 100  # in milliseconds
        last_move_time = 0

        while running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if self.game_state == "playing":
                        if event.key == K_q:
                            running = False
                    elif self.game_state == "game_over":
                        if event.key == K_r:
                            # Preserve player stats
                            current_player = self.player
                            # Reinitialize game
                            self.__init__()
                            # Restore the player
                            self.player = current_player
                            # Regenerate dungeon
                            self.generate_dungeon()
                            self.update_fov()
                        elif event.key == K_q:
                            running = False

            # Key hold movement (continuous movement)
            if self.game_state == "playing":
                keys = pygame.key.get_pressed()
                if current_time - last_move_time >= move_delay:
                    dx, dy = 0, 0
                    if keys[K_w] or keys[K_UP]:
                        dy = -1
                    elif keys[K_s] or keys[K_DOWN]:
                        dy = 1
                    elif keys[K_a] or keys[K_LEFT]:
                        dx = -1
                    elif keys[K_d] or keys[K_RIGHT]:
                        dx = 1
                    if dx != 0 or dy != 0:
                        self.move_player(dx, dy)
                        last_move_time = current_time

            if self.game_state == "playing":
                self.update_camera()
                self.draw()

            clock.tick(FPS)

        pygame.quit()
        sys.exit()


# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()