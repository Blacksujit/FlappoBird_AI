import pygame
import random
import cv2
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bird class
class Bird:
    def __init__(self):
        self.bird = pygame.Rect(WIDTH // 3, HEIGHT // 2, 30, 30)
        self.gravity = 0.5
        self.jump_strength = 8
        self.velocity = 0

    def jump(self):
        self.velocity = -self.jump_strength

    def move(self):
        self.velocity += self.gravity
        self.bird.y += int(self.velocity)

    def draw(self):
        pygame.draw.rect(SCREEN, WHITE, self.bird)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.gap = 150
        self.top = pygame.Rect(x, 0, 60, random.randint(50, HEIGHT // 2))
        self.bottom = pygame.Rect(x, self.top.height + self.gap, 60, HEIGHT)

    def move(self):
        self.top.x -= 5
        self.bottom.x -= 5

    def draw(self):
        pygame.draw.rect(SCREEN, WHITE, self.top)
        pygame.draw.rect(SCREEN, WHITE, self.bottom)

# Main game function
def flappy_bird():
    bird = Bird()
    pipes = [Pipe(WIDTH + 100)]
    score = 0
    running = True

    # OpenCV setup
    cap = cv2.VideoCapture(0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Detect if any key is pressed (simple motion detection)
        if np.mean(gray) < 100:
            bird.jump()

        bird.move()

        if pipes[-1].top.x < WIDTH // 2:
            pipes.append(Pipe(WIDTH + 100))

        for pipe in pipes:
            pipe.move()
            if pipe.top.x < -60:
                pipes.remove(pipe)
                score += 1

            if bird.bird.colliderect(pipe.top) or bird.bird.colliderect(pipe.bottom):
                running = False

        if bird.bird.y > HEIGHT or bird.bird.y < 0:
            running = False

        SCREEN.fill(BLACK)
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.flip()
        CLOCK.tick(FPS)

    cap.release()
    pygame.quit()

# Run the game manually
if __name__ == "__main__":
    flappy_bird()
