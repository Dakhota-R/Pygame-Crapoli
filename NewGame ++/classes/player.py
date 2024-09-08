import pygame
import constants.constants as c

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, player_animations):
        self.width = 50
        self.height = 50

        self.image = player_animations[0]

        self.rect = self.image.get_rect()

        self.screen = screen
        self.x = (c.SCREEN_WIDTH / 4) - self.width / 2
        self.y = (c.SCREEN_HEIGHT / 4) - self.height
        self.rect.x = self.x
        self.rect.y = self.y

        self.row = 0
        self.column = 0
        
        self.is_moving = False
        
        self.target_pos = (0,0)

        self.collide_box = self.rect.inflate(2,2)

    def changeTile(self, tile_list, row_increment, column_increment):
        target_column = self.column + column_increment
        target_row = self.row + row_increment
        for tile in tile_list:
            #print(target_column)
            if tile.column == target_column and tile.row == target_row and tile.tile_index == 1 and tile.is_walkable == True:
                self.column = tile.column
                self.row = tile.row               
                target_rect = tile.rect
                return target_rect
                
    def animateMove(self):
        if self.is_moving:
            player_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
            new_pos = pygame.math.Vector2.move_towards(player_pos, self.target_pos, c.PLAYER_SPEED)
            self.rect.x = new_pos.x
            self.rect.y = new_pos.y
            if self.rect.x == self.target_pos[0] and self.rect.y == self.target_pos[1]:
                pass
                
    def getTargetPos(self, target_rect):
        self.target_pos = target_rect.x, target_rect.y - 40          

    def move(self, camera_pos, tile_list, wall_list, dx, dy):
        self.collide_box.center = self.rect.center
        camera_pos_x = camera_pos[0]
        camera_pos_y = camera_pos[1]
        
        target_rect = 0

        if dx == 1:
            target_rect = self.changeTile(tile_list, 0, 1)
            if target_rect:
                self.getTargetPos(target_rect)
            dx = 0
        elif dy == 1:
            target_rect = self.changeTile(tile_list, 1, 0)
            if target_rect:
                self.getTargetPos(target_rect)
            dy = 0
        elif dx == -1:
            target_rect = self.changeTile(tile_list, 0, -1)
            if target_rect:
                self.getTargetPos(target_rect)
            dx = 0
        elif dy == -1:
            target_rect = self.changeTile(tile_list, -1, 0)
            if target_rect:
                self.getTargetPos(target_rect)
            dx = 0

        camera_pos_x = -self.rect.x + ((c.SCREEN_WIDTH / 2) - self.width)
        camera_pos_y = -self.rect.y + ((c.SCREEN_HEIGHT / 2) - self.height)
            
        if target_rect:
            self.getTargetPos(target_rect)

        return [camera_pos_x, camera_pos_y], dx, dy

    def update(self):
        self.animateMove()

    def draw(self, world):
        self.update()
        world.blit(self.image, self.rect)