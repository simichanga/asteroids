import pygame
from constants import VEL, MAX_BULLETS, SPACESHIP_SIZE, COLORS
from constants import WIDTH, HEIGHT, FPS, COLORS, ASSET_DIR, SPACESHIP_SIZE, METEOR_SIZE

class Spaceship:
    def __init__(self, x, y, image, controls, color_key):
        self.rect = pygame.Rect(x, y, *SPACESHIP_SIZE[::-1])
        self.image = image
        self.controls = controls
        self.bullets = []
        self.health = 10
        self.color_key = color_key

    def move(self, keys, border_rect):
        dx = dy = 0
        if keys[self.controls['left']]: dx = -VEL
        if keys[self.controls['right']]: dx = VEL
        if keys[self.controls['up']]: dy = -VEL
        if keys[self.controls['down']]: dy = VEL

        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        # Horizontal boundaries
        if self.color_key == 'YELLOW':
            lb, rb = -15, border_rect.x - self.rect.width + 15
        else:
            lb, rb = border_rect.x + border_rect.width - 15, WIDTH - self.rect.width + 15
        if lb < new_x < rb: self.rect.x = new_x
        # Vertical boundaries
        if -10 < new_y < HEIGHT - self.rect.height + 10:
            self.rect.y = new_y

    def shoot(self, sound):
        if len(self.bullets) < MAX_BULLETS:
            offset = self.rect.width if self.color_key == 'YELLOW' else -10
            bullet = pygame.Rect(
                self.rect.x + offset,
                self.rect.y + self.rect.height // 2,
                10, 5
            )
            self.bullets.append(bullet)
            sound.play()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        for bullet in self.bullets:
            pygame.draw.rect(surface, COLORS[self.color_key], bullet)