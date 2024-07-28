import tensorflow as tf

# Configure TensorFlow memory growth
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

import numpy as np
import pygame
import os
import sys
import cv2

# Ensure the game directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from ai.model import FlappyBirdAI
from game.flappy_bird import Bird, Pipe, WIDTH, HEIGHT, BLACK, WHITE

def collect_data():
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 30

    bird = Bird()
    pipes = [Pipe(WIDTH + 100)]
    states = []
    actions = []

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.jump()
            action = 1
        else:
            action = 0

        state = pygame.surfarray.array3d(SCREEN)
        state = np.dot(state[..., :3], [0.299, 0.587, 0.114])  # Convert to grayscale
        state = cv2.resize(state, (160, 120))  # Resize to 160x120
        states.append(state)
        actions.append(action)

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

    pygame.quit()
    states = np.array(states)
    actions = np.array(actions)
    print(f"Collected {states.shape[0]} states")
    return states, actions

def train_ai(model_path='ai/flappy_bird_model.h5'):
    states, actions = collect_data()
    actions = np.eye(2)[actions]  # Convert to one-hot encoding
    states = states.reshape(-1, 120, 160, 1)

    ai = FlappyBirdAI()
    ai.train(states, actions)
    ai.save_model(model_path)
    print(f"Model saved at {model_path}")

if __name__ == "__main__":
    train_ai()
