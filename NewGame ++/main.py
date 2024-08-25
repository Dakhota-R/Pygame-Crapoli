import pygame
import time
import sys



# init pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.width = 50
        self.height = 50

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(69,69,69))

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
        self.image.fill(pygame.Color(69,69,69))
        if self.rect.x + self.width >= enemy.rect.x and self.rect.x <= enemy.rect.x + enemy.width:
            if self.rect.y + self.height >= enemy.rect.y and self.rect.y <= enemy.rect.y + enemy.height:
                self.image.fill(pygame.Color(144,0,0))

    def draw(self):
        self.collisions()
        self.screen.blit(self.image, self.rect)
        self.update()


# ground object just a warmup for me, delete  when ready
class Ground(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.ground_image = pygame.Surface((40,40))
        self.ground_image.fill(pygame.Color(40,40,40))

        self.rect = self.ground_image.get_rect()

        self.screen = screen

        self.x = 100
        self.y = 100
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
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

ground = Ground(screen)
player = Player(screen)
enemy = Enemy(screen)


main = True
while main:
    clock.tick(60)
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False
        

    
    ground.draw()
    player.move()
    player.draw()
    enemy.draw()

    pygame.display.flip()
    

pygame.quit()
