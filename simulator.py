import pygame
import sys
import random
import Traffic_Generator as tg
from Traffic_Generator import moves
import threading
pygame.init()

threading.Thread(target=tg.lights_changer,daemon= True).start()
threading.Thread(target=tg.generator,daemon= True).start()
threading.Thread(target=tg.traversal,daemon= True).start()


WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Traffic Simulator")
pygame.mouse.set_visible(False)
bg = pygame.image.load("Road.png")

# Randomly select a car image
car_choice = ["Car_1.png", "Car_2.png"]
car_choice2 = ["Car_2.png", "Car_1.png"]
choice = random.choice(car_choice)
choice2 = random.choice(car_choice2)


# Load the selected image
car_raw = pygame.image.load(choice)
car_raw2 = pygame.image.load(choice2)

# Resize the image
car = pygame.transform.scale(car_raw, (100,100))
car2 =pygame.transform.scale(car_raw2, (100,100))

LANE_POS = {
    # Road A
    "AL1": (640, 720),  # Bottom center (incoming)
    "AL2": (620, 0),  # Top center (priority lane)
    "AL3": (695, 0),  # Top right (free left)

    # Road B
    "BL1": (1280, 360),  # Right center (incoming)
    "BL2": (0, 327),  # Left center (normal lane)
    "BL3": (0, 280),  # Left top (free left)

    # Road C
    "CL1": (640, 0),  # Top center (incoming)
    "CL2": (1200, 327),  # Right center (normal lane)
    "CL3": (1200, 385),  # Right bottom (free left)

    # Road D
    "DL1": (0, 360),  # Left center (incoming)
    "DL2": (620, 650),  # Bottom center (normal lane)
    "DL3": (560, 650),  # Bottom left (free left)
}
Lane_movements = {
    "AL2->BL1": (50, 0),      # Move right
    "AL3->CL1": (0, 50),      # Move down
    "BL2->CL1": (0, 50),      # Move down
    "BL3->AL1": (50, 0),      # Move right
    "CL2->DL1": (-50, 0),     # Move left
    "CL3->BL1": (0, -50),     # Move up
    "DL2->AL1": (0, -50),     # Move up
    "DL3->CL1": (50, 0),      # Move right
}

class Moving_car:
    def __init__(self,car_id,start_lane,end_lane,car_image,start_x,start_y):
        self.car_id = car_id
        self.start_lane =start_lane
        self.end_lane = end_lane
        self.car_image = car_image

        #starting position for the cars
        self.x, self.y = start_x, start_y

        #end positions for the cars
        self.target_x, self.target_y = LANE_POS[end_lane]

        move_key = f"{start_lane}->{end_lane}"
        if move_key in Lane_movements:
            self.dx , self.dy = Lane_movements[move_key]
        else :
            self.dx , self.dy = 0,0

        self.speed =5

        def Update(self):
            if abs(self.x - self.target_x) > self.speed :
                self.x += self.dx
            if abs(self.y - self.target_y) > self.speed :
                self.y+= self.dy

            if abs(self.x - self.target_x) <= self.speed and abs(self.y -self.target_y) <= self.speed :
                return True
            else :
                return False
        def draw(self,screen):
            screen.blit(self.car_image,(self.x,self.y))

        def calculate_position(Lane_name,position_in_queue):
            """Calculate position for a car based on its position in the queue"""

clock = pygame.time.Clock()
FPS = 60


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw everything
    screen.blit(bg, (0, 0))

    pygame.display.update()
    clock.tick(FPS)
    screen.blit(car, (640, 640))

    pygame.display.update()
    clock.tick(FPS)
)
