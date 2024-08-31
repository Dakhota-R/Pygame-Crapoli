import pygame
import time
import sys



# init pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player_animations = [pygame.transform.scale(pygame.image.load("New Piskel.png").convert_alpha(), (50,50))]
ground_tiles = [pygame.transform.scale(pygame.image.load(f"GroundTiles\grass_{i}.png"), (50,50)) for i in range(2)]
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

    def move(self, camera_pos):
        camera_pos_x = camera_pos[0]
        camera_pos_y = camera_pos[1]

        keys = pygame.key.get_pressed()
        right = keys[pygame.K_d]
        left = keys[pygame.K_a]
        up = keys[pygame.K_w]
        down = keys[pygame.K_s]

        move = pygame.math.Vector2(right - left, down - up)
        if move.length_squared() > 0:
            move.scale_to_length(5)
            camera_pos_x -= round(move.x)
            camera_pos_y -= round(move.y)
            self.rect.move_ip(round(move.x), round(move.y))
        
        return [camera_pos_x, camera_pos_y]
    

    def collisions(self):
        if self.rect.x + self.width >= enemy.rect.x and self.rect.x <= enemy.rect.x + enemy.width:
            if self.rect.y + self.height >= enemy.rect.y and self.rect.y <= enemy.rect.y + enemy.height:
                pass

    def draw(self, world):
        self.collisions()
        world.blit(self.image, self.rect)


# ground object just a warmup for me, delete  when ready
class Ground(pygame.sprite.Sprite):
    def __init__(self, tile_index, x_pos, y_pos):
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


inventory = Inventory(screen)
enemy = Enemy(screen)
tree = Tree(screen)


items_group = []
items = [0,0,0]
for index, item in enumerate(items):
    item = InventoryItems(screen, index * 50, SCREEN_HEIGHT - 40)
    items_group.append(item)


level = [
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
]

ground_group = []

for row_index, row in enumerate(level):
    x = row_index * 50
    for tile_index, tile in enumerate(row):
        y = tile_index * 50
        ground = Ground(tile, x, y)
        ground_group.append(ground)


def Main(screen, clock):
    world = pygame.Surface((800, 600))

    player = Player(screen)
    camera_pos = (200,200)

    while True:
        clock.tick(60)
        world.fill('black')
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        for tile in ground_group:
            tile.draw(world)

        camera_pos = player.move(camera_pos)

        player.draw(world)
        enemy.draw()
        tree.draw()
        inventory.draw(world)

        for item in items_group:
            item.draw(world)

        screen.blit(world, camera_pos)

        pygame.display.flip()
    

while __name__ == '__main__':
    Main(screen, clock)
