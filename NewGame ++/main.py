import pygame
import time
import sys
import psutil
import math
import random

import constants.constants as c
import classes.player as p
import classes.ground as g

#RRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
#WASD TO MOVE

#+++++++++++++++++++++++++++
# animate moving from tile to tile
# figure it out future self

# init pygame
pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
clock = pygame.time.Clock()

cauldron_sprite = [pygame.transform.scale(pygame.image.load("assets\cauldron_transparent.png"), (160,160))]
player_animations = [pygame.transform.scale(pygame.image.load("assets\greenpawnguy.png").convert_alpha(), (80,80))]
ground_tiles = [pygame.transform.scale(pygame.image.load(f"assets\iso_tiles_{i}.png"), (80,80)) for i in range(5)]


class Inventory(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.width = c.SCREEN_WIDTH
        self.height = c.SCREEN_HEIGHT / 5

        self.screen = screen

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(35,40,45))
        self.rect = self.image.get_rect()
        self.rect.y = c.SCREEN_HEIGHT - self.height

    def draw(self, world):
        world.blit(self.image, self.rect)

class InventoryItems(pygame.sprite.Sprite):
    def __init__(self, screen, pos_x, pos_y):
        self.width = 40
        self.height = 40

        self.screen = screen

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(100,100,20))
        self.rect = self.image.get_rect()

        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, world):
        world.blit(self.image, self.rect)
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, world, tile_x, tile_y):
        self.world = world
        self.image = ground_tiles[3]
        self.rect = self.image.get_rect()

        self.rect.x = tile_x
        self.rect.y = tile_y

        self.width = self.rect.width
        self.height = self.rect.height

    def draw(self):
        self.world.blit(self.image, self.rect)

class fourTileItem(pygame.sprite.Sprite):
    def __init__(self, screen, item_sprite_list):
        self.screen = screen
        
        self.image = item_sprite_list[0]
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0
        
        self.spawned = False
        
        self.row = 0
        self.column = 0 
        
    def draw(self, tile_list): 
        for tile in tile_list:
            if tile.row == self.row - 1 and tile.column == self.column:
                tile.is_walkable = False
            if tile.row == self.row and tile.column == self.column - 1:
                tile.is_walkable = False
            if tile.row == self.row - 1 and tile.column == self.column - 1:
                tile.is_walkable = False
        #print(self.row, self.column)
        self.screen.blit(self.image, self.rect)

inventory = Inventory(screen)

items_group = []
items = [0,0,0]
for index, item in enumerate(items):
    item = InventoryItems(screen, index * 50, c.SCREEN_HEIGHT - 40)
    items_group.append(item)

#===================================
# Level Placement
level = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 3, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1]
         ]
#===================================

#===================================
# random level
for i in range(10):
    row = []
    for j in range(10):
        tile = random.randint(0, 3)
        row.append(tile)
    #level.append(row)

#===================================
# Wall Placement
# get coords of wall tiles
# create instance of wall at tile location
#===================================

#===================================
# Main function
def Main(screen, clock):
    game_started = False
    cauldron_spawned = False
    world = pygame.Surface((len(level[0]) * 500, len(level) * 500))
    
    cauldron = fourTileItem(world, cauldron_sprite)

    player = p.Player(screen, player_animations)

    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False

    camera_pos = [0, 0]
    
    
    ground_group = []
    wall_group = []
    for row_index, row in enumerate(level):
        for tile_index, tile in enumerate(row):
            if tile == 2 or 3:
                ground = g.Ground(tile, 600  + (row_index + 1) * c.tile_offset_1 - (tile_index + 1) * c.tile_offset_1, 
                                    100 + (row_index + 1) * c.tile_offset_2 + (tile_index + 1) * c.tile_offset_2, ground_tiles)
                ground.row = row_index
                ground.column = tile_index
                if tile == 3:
                    ground.is_walkable = False
                ground_group.append(ground)
            elif tile == 3:
                pass
                #wall = Wall(world, tile, y)
                #wall_group.append(wall)

    while True:
        clock.tick(60)
        world.fill('black')
        screen.fill('black')

        dx = 0
        dy = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    dx = 1
                    player.is_moving = True
                if event.key == pygame.K_d:
                    dy = 1
                    player.is_moving = True
                if event.key == pygame.K_a:
                    dy = -1
                    player.is_moving = True
                if event.key == pygame.K_w:
                    dx = -1
                    player.is_moving = True

        # draw world tiles
        for tile in ground_group:
            tile.draw(world)
            if tile.tile_index == 2:
                # set player starting pos
                if not game_started:
                    player.rect.x, player.rect.y = tile.x, tile.y - 40
                    player.row = tile.row
                    player.column = tile.column
                    camera_pos = [player.x - 50, player.y - 100]
                    game_started = True
            # set cauldron pos
            if tile.tile_index == 3:
                if not cauldron_spawned:
                    cauldron.rect.x, cauldron.rect.y = tile.x - 30, tile.y - 130
                    cauldron.row = tile.row
                    cauldron.column = tile.column
                    cauldron_spawned = True
            
        # draw walls
        for wall in wall_group:
            wall.draw()
            
        cauldron.draw(ground_group)

        camera_pos, dx, dy = player.move(camera_pos, ground_group, wall_group, dx, dy)

        player.draw(world)

        screen.blit(world, camera_pos)

        inventory.draw(screen)
        for item in items_group:
            item.draw(screen)

        pygame.display.flip()
    
while __name__ == '__main__':
    Main(screen, clock)
