import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRAVITY = 1.5
JUMP_HEIGHT = 10
PIPE_WIDTH = 50
PIPE_GAP = 150
BIRD_SIZE_IN_GAME = 40

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE_IN_GAME, BIRD_SIZE_IN_GAME))

background_img = pygame.image.load("background.png")
pipe_img = pygame.image.load("pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, HEIGHT - PIPE_GAP))

# Bird class
class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = -JUMP_HEIGHT

    def update(self, space_pressed):
        if space_pressed:
            self.velocity = -JUMP_HEIGHT * 1.2
        else:
            self.velocity += GRAVITY
        self.y += self.velocity

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.passed = False

    def update(self):
        self.x -= 5

# Create objects
bird = Bird()
pipes = [Pipe(WIDTH + i * 300) for i in range(2)]

score_font = pygame.font.Font(None, 24)
score_color = (0, 0, 0)
score = 0

game_over_font = pygame.font.Font(None, 48)
game_over_color = (255, 0, 0)
game_over_text = game_over_font.render("Game Over", True, game_over_color)
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

total_score_font = pygame.font.Font(None, 36)
total_score_color = (0, 0, 0)
total_score_text = total_score_font.render("Your total score is:", True, total_score_color)
total_score_rect = total_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

play_again_font = pygame.font.Font(None, 24)
play_again_color = (0, 0, 255)
play_again_text = play_again_font.render("Press 'R' to play again", True, play_again_color)
play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

clock = pygame.time.Clock()
# Game loop
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird.flap()
            elif event.key == pygame.K_r and game_over:
                # Reset the game state
                bird = Bird()
                pipes = [Pipe(WIDTH + i * 300) for i in range(2)]
                score = 0
                game_over = False

    space_pressed = pygame.key.get_pressed()[pygame.K_SPACE]

    if not game_over:
        # Update
        bird.update(space_pressed)
        for pipe in pipes:
            pipe.update()

            if not pipe.passed and bird.x > pipe.x + PIPE_WIDTH:
                pipe.passed = True
                score += 1
                # print(f"Score: {score}")

        # Check collisions
        if bird.y > HEIGHT or bird.y < 0:
            game_over = True

        for pipe in pipes:
            if (
                bird.x < pipe.x + PIPE_WIDTH
                and bird.x + BIRD_SIZE_IN_GAME > pipe.x
                and (bird.y < pipe.height or bird.y + BIRD_SIZE_IN_GAME > pipe.height + PIPE_GAP)
            ):
                game_over = True

        # Add new pipes
        if pipes[-1].x < WIDTH - 300:
            pipes.append(Pipe(WIDTH))

        # Remove off-screen pipes
        if pipes[0].x < -PIPE_WIDTH:
            pipes.pop(0)

    # Draw
    screen.blit(background_img, (0, 0))

    if not game_over:
        # Draw bird
        screen.blit(bird_img, (bird.x, bird.y))
        for pipe in pipes:
            screen.blit(pipe_img, (pipe.x, pipe.height + PIPE_GAP))
            upper_pipe_height = pipe.height - HEIGHT + PIPE_GAP
            screen.blit(pipe_img, (pipe.x, upper_pipe_height))

        # Draw score
        score_text = score_font.render(f"Score: {score}", True, score_color)
        screen.blit(score_text, (10, 10))
    else:
        # Draw game over screen
        screen.blit(game_over_text, game_over_rect)
        screen.blit(total_score_text, total_score_rect)
        total_score_value_text = total_score_font.render(str(score), True, total_score_color)
        total_score_value_rect = total_score_value_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.8))
        screen.blit(total_score_value_text, total_score_value_rect)
        screen.blit(play_again_text, play_again_rect)

    pygame.display.flip()
    clock.tick(30)
