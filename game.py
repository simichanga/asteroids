import os
import pygame
from constants import WIDTH, HEIGHT, FPS, COLORS, ASSET_DIR, SPACESHIP_SIZE, METEOR_SIZE, BULLET_VEL
from spaceship import Spaceship
from meteor import Meteor

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # Window setup
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Space Fight')
        self.clock = pygame.time.Clock()

        # Background and border
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_DIR, 'space.png')),
            (WIDTH, HEIGHT)
        )
        self.border = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

        # Sounds and fonts
        self.bullet_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, 'laser.wav'))
        self.hit_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, 'explosion.wav'))
        self.health_font = pygame.font.SysFont('arial', 40)
        self.winner_font = pygame.font.SysFont('arial', 100)

        # Load ship images
        def load_ship(name, rot):
            img = pygame.transform.rotate(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(ASSET_DIR, name)
                    ), SPACESHIP_SIZE
                ), rot
            )
            return img

        # Create spaceships
        self.yellow = Spaceship(
            100, 300,
            load_ship('spaceship_yellow.png', 90),
            {
                'left': pygame.K_a, 'right': pygame.K_d,
                'up': pygame.K_w, 'down': pygame.K_s,
                'shoot': pygame.K_SPACE
            },
            'YELLOW'
        )
        self.red = Spaceship(
            700, 300,
            load_ship('spaceship_red.png', 270),
            {
                'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                'up': pygame.K_UP, 'down': pygame.K_DOWN,
                'shoot': pygame.K_RCTRL
            },
            'RED'
        )

        # Create meteors
        meteor_img = pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join(ASSET_DIR, 'meteor.png')
                ), METEOR_SIZE
            ),
            90
        )
        self.meteors = [Meteor(meteor_img) for _ in range(3)]

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            # Event handling
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == self.yellow.controls['shoot']:
                        self.yellow.shoot(self.bullet_sound)
                    if event.key == self.red.controls['shoot']:
                        self.red.shoot(self.bullet_sound)
                if event.type == pygame.USEREVENT + 1:
                    self.yellow.health -= 1
                    self.hit_sound.play()
                if event.type == pygame.USEREVENT + 2:
                    self.red.health -= 1
                    self.hit_sound.play()
            # Movement
            self.yellow.move(keys, self.border)
            self.red.move(keys, self.border)
            # Update bullets and meteors
            self.update_game()
            # Drawing
            self.draw()
            # Check for winner
            winner = self.check_winner()
            if winner:
                self.display_winner(winner)
                running = False
        pygame.time.delay(5000)
        pygame.quit()

    def update_game(self):
        # Handle bullets collisions and movement
        for shooter, target, evt in [
            (self.yellow, self.red, pygame.USEREVENT + 2),
            (self.red, self.yellow, pygame.USEREVENT + 1)
        ]:
            for b in shooter.bullets[:]:
                b.x += BULLET_VEL if shooter.color_key == 'YELLOW' else -BULLET_VEL
                if target.rect.colliderect(b):
                    pygame.event.post(pygame.event.Event(evt))
                    shooter.bullets.remove(b)
                elif not (0 <= b.x <= WIDTH):
                    shooter.bullets.remove(b)
                else:
                    for m in self.meteors:
                        if m.rect.colliderect(b):
                            shooter.bullets.remove(b)
                            break
        # Meteors update and collisions
        for m in self.meteors:
            m.update()
            for ship, evt in [(self.yellow, pygame.USEREVENT + 1), (self.red, pygame.USEREVENT + 2)]:
                if m.rect.colliderect(ship.rect):
                    pygame.event.post(pygame.event.Event(evt))
                    m.rect.center = (WIDTH // 2, HEIGHT // 2)

    def draw(self):
        self.win.blit(self.background, (0, 0))
        pygame.draw.rect(self.win, COLORS['BLACK'], self.border)
        # Health display
        y_text = self.health_font.render(
            f"Health: {self.yellow.health}", True, COLORS['WHITE']
        )
        r_text = self.health_font.render(
            f"Health: {self.red.health}", True, COLORS['WHITE']
        )
        self.win.blit(y_text, (10, 10))
        self.win.blit(r_text, (WIDTH - r_text.get_width() - 10, 10))
        # Draw entities
        self.yellow.draw(self.win)
        self.red.draw(self.win)
        for m in self.meteors:
            m.draw(self.win)
        pygame.display.update()

    def check_winner(self):
        if self.yellow.health <= 0:
            return 'Red Wins!'
        if self.red.health <= 0:
            return 'Yellow Wins!'
        return None

    def display_winner(self, text):
        winner_surf = self.winner_font.render(text, True, COLORS['WHITE'])
        self.win.blit(
            winner_surf,
            (
                WIDTH // 2 - winner_surf.get_width() // 2,
                HEIGHT // 2 - winner_surf.get_height() // 2
            )
        )
        pygame.display.update()