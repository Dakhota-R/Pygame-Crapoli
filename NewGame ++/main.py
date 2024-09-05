import pygame
import time
import sys
import psutil
import math



# init pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player_animations = [pygame.transform.scale(pygame.image.load("New Piskel.png").convert_alpha(), (50,50))]
ground_tiles = [pygame.transform.scale(pygame.image.load(f"GroundTiles\grass_{i}.png"), (50,50)) for i in range(4)]
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

        self.collide_box = self.rect.inflate(2,2)

    def move(self, camera_pos, level, wall_list, dx, dy):
        self.collide_box.center = self.rect.center
        camera_pos_x = camera_pos[0]
        camera_pos_y = camera_pos[1]

        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx
        for wall in wall_list:
            if wall.rect.colliderect(self.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
        
        self.rect.y += dy
        for wall in wall_list:
            if wall.rect.colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom


        camera_pos_x = -self.rect.x + ((SCREEN_WIDTH / 2) - self.width)
        camera_pos_y = -self.rect.y + ((SCREEN_HEIGHT / 2) - self.height)
            

        
        return [camera_pos_x, camera_pos_y]


    def draw(self, world):
        world.blit(self.image, self.collide_box)
        world.blit(self.image, self.rect)

class Ground(pygame.sprite.Sprite):
    def __init__(self, tile_index, x_pos, y_pos):
        self.tile_index = tile_index

        self.ground_image = ground_tiles[tile_index]

        self.rect = self.ground_image.get_rect()


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
    [3,3,3,3,3,3,3,3,3,3],
    [3,0,1,0,0,0,0,0,1,3],
    [3,0,0,1,0,0,0,0,1,3],
    [3,0,0,0,1,0,0,0,1,3],
    [3,0,0,0,0,1,0,0,1,3],
    [3,0,0,0,0,0,1,0,1,3],
    [3,0,0,0,0,0,0,1,1,3],
    [3,0,0,0,2,0,0,1,0,3],
    [3,0,0,0,0,0,0,1,0,3],
    [3,0,0,0,0,0,0,1,0,3],
    [3,0,0,0,0,0,0,1,0,3],
    [3,0,3,0,3,0,0,1,0,3],
    [3,0,0,0,0,0,0,1,0,3],
    [3,0,0,0,0,0,0,1,0,3],
    [3,3,3,3,3,3,3,3,3,3],
]
#===================================

#===================================
# Wall Placement
# get coords of wall tiles
# create instance of wall at tile location
#===================================

#===================================
# Main function
def Main(screen, clock):
    game_started = False
    world = pygame.Surface((len(level[0]) * 50, len(level) * 50))

    player = Player(screen)
    camera_pos = ()

    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False
    
    ground_group = []
    wall_group = []
    for row_index, row in enumerate(level):
        y = row_index * 50
        for tile_index, tile in enumerate(row):
            x = tile_index * 50
            if tile != 3:
                ground = Ground(tile, x, y)
                ground_group.append(ground)
            elif tile == 3:
                wall = Wall(world, x, y)
                wall_group.append(wall)

    while True:
        clock.tick(60)
        world.fill('black')
        screen.fill('black')

        dx = 0
        dy = 0
        if moving_right:
            dx = 5
        if moving_left:
            dx = -5
        if moving_down:
            dy = 5
        if moving_up:
            dy = -5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w:
                    moving_up = True
                if event.key == pygame.K_s:
                    moving_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_s:
                    moving_down = False

        # draw world tiles
        for tile in ground_group:
            tile.draw(world)
            if tile.tile_index == 2:
                # set player starting pos
                if not game_started:
                    player.rect.x, player.rect.y = (tile.x, tile.y)
                    camera_pos = (player.x - 50, player.y - 100)
                    game_started = True

        for wall in wall_group:
            wall.draw()


        camera_pos = player.move(camera_pos, level, wall_group, dx, dy)

        player.draw(world)

        screen.blit(world, camera_pos)

        inventory.draw(screen)
        for item in items_group:
            item.draw(screen)

        pygame.display.flip()
    

while __name__ == '__main__':
    Main(screen, clock)
