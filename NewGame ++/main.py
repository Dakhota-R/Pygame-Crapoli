import pygame
import time
import sys
import psutil
import math
import random



#RRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
#WASD TO MOVE

#+++++++++++++++++++++++++++
# animate moving from tile to tile
# figure it out future self





tile_offset_1 = 40
tile_offset_2 = 20

# init pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player_animations = [pygame.transform.scale(pygame.image.load("assets\greenpawnguy.png").convert_alpha(), (80,80))]
ground_tiles = [pygame.transform.scale(pygame.image.load(f"assets\iso_tiles_{i}.png"), (80,80)) for i in range(4)]
tree = pygame.transform.scale(pygame.image.load("tree.png"), (50,50))

camera_pos = [0, 0]

class Inventory(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT / 5

        self.screen = screen

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(35,40,45))
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - self.height

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
        
class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.width = 50
        self.height = 50

        self.image = player_animations[0]

        self.rect = self.image.get_rect()

        self.screen = screen
        self.x = (SCREEN_WIDTH / 4) - self.width / 2
        self.y = (SCREEN_HEIGHT / 4) - self.height
        self.rect.x = self.x
        self.rect.y = self.y

        self.row = 0
        self.column = 0

        self.collide_box = self.rect.inflate(2,2)

    def changeTile(self, tile_list, row_increment, column_increment):
        target_column = self.column + column_increment
        target_row = self.row + row_increment
        for tile in tile_list:
            print(target_column)
            if tile.column == target_column and tile.row == target_row and tile.tile_index == 1:
                self.column = tile.column
                self.row = tile.row               
                target_rect = tile.rect
                return target_rect
                #self.rect.x = tile.rect.x
                #self.rect.y = tile.rect.y - 40
                
    def animateMove(self, target_rect):
        self.rect.x = target_rect.x
        self.rect.y = target_rect.y - 40

    def move(self, camera_pos, tile_list, wall_list, dx, dy):
        self.collide_box.center = self.rect.center
        camera_pos_x = camera_pos[0]
        camera_pos_y = camera_pos[1]
        
        target_rect = 0

        if dx == 1:
            target_rect = self.changeTile(tile_list, 0, 1)
            if target_rect:
                self.animateMove(target_rect)
            dx = 0
        elif dy == 1:
            target_rect = self.changeTile(tile_list, 1, 0)
            if target_rect:
                self.animateMove(target_rect)
            dy = 0
        elif dx == -1:
            target_rect = self.changeTile(tile_list, 0, -1)
            if target_rect:
                self.animateMove(target_rect)
            dx = 0
        elif dy == -1:
            target_rect = self.changeTile(tile_list, -1, 0)
            if target_rect:
                self.animateMove(target_rect)
            dx = 0


        camera_pos_x = -self.rect.x + ((SCREEN_WIDTH / 2) - self.width)
        camera_pos_y = -self.rect.y + ((SCREEN_HEIGHT / 2) - self.height)
            
        if target_rect:
            self.animateMove(target_rect)

        
        return [camera_pos_x, camera_pos_y], dx, dy


    def draw(self, world):
        world.blit(self.image, self.rect)

class Ground(pygame.sprite.Sprite):
    def __init__(self, tile_index, x_pos, y_pos):
        self.tile_index = tile_index

        self.ground_image = ground_tiles[tile_index]

        self.rect = self.ground_image.get_rect()

        self.width = self.ground_image.get_width()
        self.height = self.ground_image.get_height()

        self.x = x_pos
        self.y = y_pos
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, world):
        world.blit(self.ground_image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.width = 40
        self.height = 40

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(79,33,2))

        self.rect = self.image.get_rect()
        
        self.screen = screen
        
        self.x = 300
        self.y = 300
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Tree(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.image = tree
        self.rect = self.image.get_rect()
        self.screen = screen
        self.x = 300
        self.y = 300
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        self.screen.blit(self.image, self.rect)
        
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




inventory = Inventory(screen)
enemy = Enemy(screen)
tree = Tree(screen)


items_group = []
items = [0,0,0]
for index, item in enumerate(items):
    item = InventoryItems(screen, index * 50, SCREEN_HEIGHT - 40)
    items_group.append(item)




#===================================
# Level Placement
level = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 2, 3, 0, 0, 0, 0, 0, 0]
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
    world = pygame.Surface((len(level[0]) * 500, len(level) * 500))

    player = Player(screen)
    camera_pos = ()

    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False
    
    
    ground_group = []
    wall_group = []
    for row_index, row in enumerate(level):
        for tile_index, tile in enumerate(row):
            if tile != 3:
                ground = Ground(tile, 600  + (row_index + 1) * tile_offset_1 - (tile_index + 1) * tile_offset_1, 
                                    100 + (row_index + 1) * tile_offset_2 + (tile_index + 1) * tile_offset_2)
                ground.row = row_index
                ground.column = tile_index
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
                if event.key == pygame.K_d:
                    dy = 1
                if event.key == pygame.K_a:
                    dy = -1
                if event.key == pygame.K_w:
                    dx = -1

        # draw world tiles
        for tile in ground_group:
            tile.draw(world)
            if tile.tile_index == 2:
                # set player starting pos
                if not game_started:
                    player.rect.x, player.rect.y = tile.x, tile.y - 40
                    player.row = tile.row
                    player.column = tile.column
                    camera_pos = (player.x - 50, player.y - 100)
                    game_started = True

        for wall in wall_group:
            wall.draw()


        camera_pos, dx, dy = player.move(camera_pos, ground_group, wall_group, dx, dy)

        player.draw(world)

        screen.blit(world, camera_pos)

        inventory.draw(screen)
        for item in items_group:
            item.draw(screen)

        pygame.display.flip()
    

while __name__ == '__main__':
    Main(screen, clock)
