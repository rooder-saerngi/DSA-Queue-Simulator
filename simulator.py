import pygame
import sys
import threading
import time

# ---------------- START GENERATOR ----------------
import Traffic_Generator as tg

threading.Thread(target=tg.lights_changer, daemon=True).start()
threading.Thread(target=tg.generator, daemon=True).start()
threading.Thread(target=tg.traversal, daemon=True).start()

# ---------------- PYGAME SETUP ----------------
pygame.init()
WIDTH, HEIGHT = 1368, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulator")
clock = pygame.time.Clock()
bg = pygame.image.load("Road.png").convert()

# ---------------- CONSTANTS ----------------
CAR_W, CAR_H = 50, 30
SPEED = 4
INTERSECTION = (684, 384)
LANE_SPACING = 60

# ---------------- LANES ----------------
lane_pos = {
    "AL3": (684, 0), "AL2": (646, 0), "AL1": (646, 760),
    "BL3": (0, 350), "BL2": (0, 384), "BL1": (1360, 384),
    "CL3": (1420, 418), "CL2": (1420, 384), "CL1": (684, -20),
    "DL3": (646, 820), "DL2": (684, 820), "DL1": (-20, 384),

    # Added proper exit lanes to avoid twitching
    "AL_exit": (684, -120),
    "BL_exit": (1500, 384),
    "CL_exit": (1420, 100),
    "DL_exit": (646, 900),
}

lane_dir = {
    "AL3": (0, 1), "AL2": (0, 1),
    "BL3": (1, 0), "BL2": (1, 0),
    "CL3": (-1, 0), "CL2": (-1, 0),
    "DL3": (0, -1), "DL2": (0, -1),
}

# Map lanes to intersection sides
lane_to_intersection = {
    "AL2": "A", "AL3": "A",
    "BL2": "B", "BL3": "B",
    "CL2": "C", "CL3": "C",
    "DL2": "D", "DL3": "D"
}

# ---------------- STATE ----------------
lanes = {k: [] for k in lane_pos}   # VISUAL lanes
moving = []                         # moving cars
intersection_busy = {"A": False, "B": False, "C": False, "D": False}

# ---------------- HELPERS ----------------
def spawn_car(lane):
    idx = len(lanes[lane])
    bx, by = lane_pos[lane]
    dx, dy = lane_dir.get(lane, (0, 0))
    x = bx + dx * idx * LANE_SPACING
    y = by + dy * idx * LANE_SPACING
    lanes[lane].append({"x": x, "y": y})


def start_move():
    if tg.moves.is_empty():
        return

    move = tg.moves.dequeue()
    src, dst = move.split("->")

    direction = lane_to_intersection.get(src)
    if direction and intersection_busy[direction]:
        # Intersection lane blocked
        tg.moves.enqueue(move)  # requeue for next check
        return

    if not lanes[src]:
        spawn_car(src)

    car = lanes[src].pop(0)
    if direction:
        intersection_busy[direction] = True

    moving.append({
        "x": car["x"],
        "y": car["y"],
        "phase": 0,
        "dst": dst,
        "direction": direction
    })


def update_moving():
    for car in moving[:]:
        if car["phase"] == 0:  # Move to intersection
            tx, ty = INTERSECTION
        else:  # Move to destination lane
            tx, ty = lane_pos[car["dst"]]

        dx = tx - car["x"]
        dy = ty - car["y"]

        # Move without overshooting
        if abs(dx) > SPEED:
            car["x"] += SPEED if dx > 0 else -SPEED
        else:
            car["x"] = tx

        if abs(dy) > SPEED:
            car["y"] += SPEED if dy > 0 else -SPEED
        else:
            car["y"] = ty

        # Phase handling
        if car["x"] == tx and car["y"] == ty:
            if car["phase"] == 0:
                car["phase"] = 1
            else:
                moving.remove(car)
                lanes[car["dst"]].append(car)
                if car["direction"]:
                    intersection_busy[car["direction"]] = False


# ---------------- DRAW ----------------
def draw():
    screen.fill((25, 25, 25))
    screen.blit(bg, (0, 0))

    for lane, cars in lanes.items():
        for c in cars:
            pygame.draw.rect(screen, (0, 200, 0), (c["x"], c["y"], CAR_W, CAR_H))


    for c in moving:
        pygame.draw.rect(screen, (200, 0, 0), (c["x"], c["y"], CAR_W, CAR_H))

    pygame.display.flip()


# ---------------- MAIN LOOP ----------------
MOVE_TIMER = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    MOVE_TIMER += clock.get_time()
    if MOVE_TIMER > 800:   # one move every 0.8s
        start_move()
        MOVE_TIMER = 0

    update_moving()
    draw()
    clock.tick(60)
