import pygame
import random
import math
from constants import WIDTH, HEIGHT, METEOR_SIZE

class Meteor:
    def __init__(self, image):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, *METEOR_SIZE)
        angle = random.uniform(0, 2 * math.pi)
        self.vel = pygame.math.Vector2(
            math.cos(angle) * 2,
            math.sin(angle) * 2
        )
        self.image = image

    def update(self):
        self.rect.x = (self.rect.x + self.vel.x) % (WIDTH + METEOR_SIZE[0])
        self.rect.y = (self.rect.y + self.vel.y) % (HEIGHT + METEOR_SIZE[1])

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)