import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, tile_index, x_pos, y_pos, ground_tiles):
        self.tile_index = tile_index

        self.ground_image = ground_tiles[tile_index]

        self.rect = self.ground_image.get_rect()

        self.width = self.ground_image.get_width()
        self.height = self.ground_image.get_height()

        self.x = x_pos
        self.y = y_pos
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.is_walkable = True

    def draw(self, world):
        world.blit(self.ground_image, self.rect)