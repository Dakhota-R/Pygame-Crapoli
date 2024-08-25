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



class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.width = 50
        self.height = 50

        self.image = player_animations[0]

        self.rect = self.image.get_rect()

        self.screen = screen

        self.x = 200
        self.y = 200
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self):
        keys = pygame.key.get_pressed()
        right = keys[pygame.K_d]
        left = keys[pygame.K_a]
        up = keys[pygame.K_w]
        down = keys[pygame.K_s]

        move = pygame.math.Vector2(right - left, down - up)
        if move.length_squared() > 0:
            move.scale_to_length(5)
            self.rect.move_ip(round(move.x), round(move.y))

    def collisions(self):
        if self.rect.x + self.width >= enemy.rect.x and self.rect.x <= enemy.rect.x + enemy.width:
            if self.rect.y + self.height >= enemy.rect.y and self.rect.y <= enemy.rect.y + enemy.height:
                pass

    def draw(self):
        self.collisions()
        self.screen.blit(self.image, self.rect)
        self.update()


# ground object just a warmup for me, delete  when ready
class Ground(pygame.sprite.Sprite):
    def __init__(self, screen, tile_index, x_pos, y_pos):
        self.ground_image = ground_tiles[tile_index]

        self.rect = self.ground_image.get_rect()

        self.screen = screen

        self.x = x_pos
        self.y = y_pos
        self.rect.x = self.x
        self.rect.y = self.y


    def draw(self, player_x, player_y):
        self.screen.blit(self.ground_image, self.rect)

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


player = Player(screen)
enemy = Enemy(screen)
tree = Tree(screen)

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
        ground = Ground(screen, tile, x, y)
        ground_group.append(ground)

main = True
while main:
    clock.tick(60)
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False
        

    for tile in ground_group:
        tile.draw(player.x, player.y)
    player.move()
    player.draw()
    enemy.draw()
    tree.draw()

    pygame.display.flip()
    

pygame.quit()