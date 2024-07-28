import tensorflow as tf

# Configure TensorFlow memory growth
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

import pygame
import numpy as np
import cv2
import os
import sys

# Ensure the game directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from ai.model import FlappyBirdAI
from game.flappy_bird import Bird, Pipe, WIDTH, HEIGHT, BLACK, WHITE

def play_ai():
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 30

    bird = Bird()
    pipes = [Pipe(WIDTH + 100)]
    ai = FlappyBirdAI()
    ai.load_model('ai/flappy_bird_model.h5')

    running = True
    cap = cv2.VideoCapture(0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        state = cv2.resize(gray, (160, 120))

        state = state.reshape(120, 160, 1) / 255.0  # Normalize the state
        state = np.expand_dims(state, axis=0)  # Add batch dimension

        action = np.argmax(ai.predict(state))

        if action == 1:
            bird.jump()

        bird.move()

        if pipes[-1].top.x < WIDTH // 2:
            pipes.append(Pipe(WIDTH + 100))

        for pipe in pipes:
            pipe.move()
            if pipe.top.x < -60:
                pipes.remove(pipe)

            if bird.bird.colliderect(pipe.top) or bird.bird.colliderect(pipe.bottom):
                running = False

        if bird.bird.y > HEIGHT or bird.bird.y < 0:
            running = False

        SCREEN.fill(BLACK)
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        pygame.display.flip()
        CLOCK.tick(FPS)

    cap.release()
    pygame.quit()

if __name__ == "__main__":
    play_ai()
