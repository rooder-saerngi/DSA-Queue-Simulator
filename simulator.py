import pygame
import sys
import random
import Traffic_Generator as T
import threading

threading.Thread(target=T.Lights_Changer,daemon= True).start()
threading.Thread(target=T.generator,daemon= True).start()
threading.Thread(target=T.traversal,daemon= True).start()
pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Traffic Simulator")
pygame.mouse.set_visible(False)

bg = pygame.image.load("Road.png")

# Randomly select a car image
car_choice = ["Car_1.png", "Car_2.png"]
choice = random.choice(car_choice)

# Load the selected image
car_raw = pygame.image.load(choice)

# Resize the image
car = pygame.transform.scale(car_raw, (200, 200))

clock = pygame.time.Clock()
FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw everything
    screen.blit(bg, (0, 0))
    screen.blit(car, (640, 640))

    pygame.display.update()
    clock.tick(FPS)
