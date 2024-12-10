'''EECE2140 Final Project Brick Breaker'''
import pygame
import sys

#need to type pip3 install pygame in terminal in order to run pygame
'''Decided to break each component of the game into classes for example paddle, brick, ball, and game, etc
this allowed us to add to the game easily and build on this in the future'''

# Initialize pygame
pygame.init()

# Constants
BOARD_WIDTH, BOARD_HEIGHT = 500, 500
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BRICK_WIDTH, BRICK_HEIGHT = 50, 10
BRICK_COLS = 8
BRICK_ROWS = 3
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

class Ball:
    '''Ball has all of the attributes including, movement, the drawing, and how it handles collisions with the paddle and bricks.'''
    def __init__(self):
        self.x = 250
        self.y = 150
        self.speed_x = 4
        self.speed_y = 5

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, PURPLE, (self.x, self.y, BALL_SIZE, BALL_SIZE))

    def handle_collision(self, paddle, bricks):
        if self.x <= 0 or self.x + BALL_SIZE >= BOARD_WIDTH:
            self.speed_x *= -1
        if self.y <= 0:
            self.speed_y *= -1

        if paddle.rect.colliderect((self.x, self.y, BALL_SIZE, BALL_SIZE)):
            self.speed_y *= -1

        for i, (brick, hit_points) in enumerate(bricks):
            if brick.colliderect((self.x, self.y, BALL_SIZE, BALL_SIZE)):
                self.speed_y *= -1
                '''Hp is calculated by the number of hitpoints, 4 hp and 2 hp bricks offer no pts, this is to balance the game. As 5 hp bricks will offer 5 pts, 
                but also 3 pts and 1 pt as it will turn to yellow and blue.'''
                if hit_points == 5:
                    score = 5
                elif hit_points == 3:
                    score = 3
                elif hit_points == 1:
                    score = 1
                else:
                    score = 0
                hit_points -= 1
                if hit_points == 0:
                    bricks.pop(i)
                else:
                    bricks[i] = (brick, hit_points)
                return score
        return 0

class Paddle:
    '''Paddle has all of the attributes including, movement, the drawing, and how it handles collisions with the ball.'''
    def __init__(self):
        self.x = (BOARD_WIDTH - PADDLE_WIDTH) // 2
        self.speed = 5

    @property
    def rect(self):
        return pygame.Rect(self.x, BOARD_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + PADDLE_WIDTH < BOARD_WIDTH:
            self.x += self.speed
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x + PADDLE_WIDTH < BOARD_WIDTH:
            self.x += self.speed

    def move_with_mouse(self):
        mouse_x, _ = pygame.mouse.get_pos() 
        self.x = mouse_x - PADDLE_WIDTH // 2
        if self.x < 0:
            self.x = 0
        elif self.x + PADDLE_WIDTH > BOARD_WIDTH:
            self.x = BOARD_WIDTH - PADDLE_WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Brick:
    '''Brick with attributes of hp and collisions'''
    def __init__(self, x, y, hit_points):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.hit_points = hit_points

    def draw(self, screen):
        '''Color is determined by number of hp.'''
        if self.hit_points == 5:
            color = RED
        elif self.hit_points == 4:
            color = ORANGE
        elif self.hit_points == 3:
            color = YELLOW
        elif self.hit_points == 2:
            color = GREEN
        else:
            color = BLUE
        pygame.draw.rect(screen, color, self.rect)

class Game:
    '''Game class with attribues  of screen, main menu,'''
    def __init__(self):
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.ball = Ball()
        self.paddle = Paddle()
        self.bricks = []
        self.in_game = False
        self.game_over = False
        self.paused = False
        self.message = "Click to Start"
        self.difficulty_selected = False
        self.lives = 3
        self.score = 0
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = 10 + 20 + col * 55
                y = 20 + row * 20
                if row == 0:
                    hit_points = 5
                elif row == 1:
                    hit_points = 3
                else:
                    hit_points = 1
                self.bricks.append((pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT), hit_points))

    def select_difficulty(self):
        '''main menu'''
        self.screen.fill(WHITE)
        easy_text = self.font.render("Press 1 for Easy (3 lives)", True, BLUE)
        medium_text = self.font.render("Press 2 for Medium (2 lives)", True, BLUE)
        hard_text = self.font.render("Press 3 for Hard (1 life)", True, BLUE)
        self.screen.blit(easy_text, (100, 150))
        self.screen.blit(medium_text, (100, 200))
        self.screen.blit(hard_text, (100, 250))
        pygame.display.flip()

        while not self.difficulty_selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.lives = 3
                        self.difficulty_selected = True
                    elif event.key == pygame.K_2:
                        self.lives = 2
                        self.difficulty_selected = True
                    elif event.key == pygame.K_3:
                        self.lives = 1
                        self.difficulty_selected = True
            self.clock.tick(FPS)

    def draw_game(self):
        self.screen.fill(WHITE)
        self.ball.draw(self.screen)
        self.paddle.draw(self.screen)
        for brick, hit_points in self.bricks:
            Brick(brick.x, brick.y, hit_points).draw(self.screen)
        text = self.font.render(self.message, True, BLUE)
        self.screen.blit(text, (10, BOARD_HEIGHT - 30))
        lives_text = self.font.render(f"Lives: {self.lives}", True, BLACK)
        self.screen.blit(lives_text, (BOARD_WIDTH - 100, 10))
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

    def run(self):
        self.select_difficulty()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.in_game:
                    if self.game_over:
                        self.reset_game()
                        self.difficulty_selected = False
                        self.select_difficulty()
                    self.in_game = True
                    self.message = ""
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.paused = not self.paused

            keys = pygame.key.get_pressed()
            self.paddle.move(keys)
            if pygame.mouse.get_rel()[0] != 0:
                self.paddle.move_with_mouse()

            if self.in_game and not self.paused:
                self.ball.move()
                self.score += self.ball.handle_collision(self.paddle, self.bricks)
                if self.ball.y > BOARD_HEIGHT:
                    self.lives -= 1
                    if self.lives == 0:
                        self.in_game = False
                        self.game_over = True
                        self.message = "Game Over! Click to Restart"
                    else:
                        self.ball = Ball()
                if not self.bricks:
                    self.in_game = False
                    self.game_over = True
                    self.message = "You Win! Click to Restart"

            self.draw_game()
            pygame.display.flip()
            self.clock.tick(FPS)

Game().run()