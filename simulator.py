import pygame
import sys
import threading
import time

# Starting traffic generator
import Traffic_Generator as tg

threading.Thread(target=tg.lights_changer, daemon=True).start()
threading.Thread(target=tg.generator, daemon=True).start()
threading.Thread(target=tg.traversal, daemon=True).start()

# Setting up pygame
pygame.init()
WIDTH, HEIGHT = 1368, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulator - Queue Based")
clock = pygame.time.Clock()

# Try to load background or use solid color
try:
    bg = pygame.image.load("Road.png").convert()
except:
    bg = None
    print("[WARNING] Road.png not found, using solid background")

# Constants
CAR_W, CAR_H = 40, 25
SPEED = 5
INTERSECTION = (WIDTH // 2, HEIGHT // 2)
LANE_SPACING = 70

# Colors
ROAD_COLOR = (40, 40, 40)
LANE_COLOR = (80, 80, 80)
LINE_COLOR = (200, 200, 0)
CAR_COLOR_NORMAL = (0, 150, 255)
CAR_COLOR_MOVING = (255, 100, 100)
CAR_COLOR_PRIORITY = (255, 200, 0)
TEXT_COLOR = (255, 255, 255)
GREEN_LIGHT = (0, 255, 0)
RED_LIGHT = (255, 0, 0)

# Lanes positions - where cars wait BEFORE entering intersection
lane_pos = {
    # Lane A (BOTTOM) - cars wait at bottom, facing UP
    "AL3": (WIDTH // 2 - 80, HEIGHT - 150),
    "AL2": (WIDTH // 2 - 20, HEIGHT - 150),

    # Lane B (LEFT) - cars wait at left, facing RIGHT
    "BL3": (150, HEIGHT // 2 - 80),
    "BL2": (150, HEIGHT // 2 - 20),

    # Lane C (TOP) - cars wait at top, facing DOWN
    "CL3": (WIDTH // 2 + 80, 150),
    "CL2": (WIDTH // 2 + 20, 150),

    # Lane D (RIGHT) - cars wait at right, facing LEFT
    "DL3": (WIDTH - 150, HEIGHT // 2 + 80),
    "DL2": (WIDTH - 150, HEIGHT // 2 + 20),
}

# Lane directions for queueing (AWAY from intersection)
lane_dir = {
    "AL3": (0, 1), "AL2": (0, 1),
    "BL3": (-1, 0), "BL2": (-1, 0),
    "CL3": (0, -1), "CL2": (0, -1),
    "DL3": (1, 0), "DL2": (1, 0),
}

# Intersection entry points - where cars enter the intersection edge
intersection_approach = {

    "AL2": (WIDTH // 2 - 20, HEIGHT // 2 + 80),
    "AL3": (WIDTH // 2 - 80, HEIGHT // 2 + 80),


    "BL2": (WIDTH // 2 - 80, HEIGHT // 2 - 20),
    "BL3": (WIDTH // 2 - 80, HEIGHT // 2 - 80),


    "CL2": (WIDTH // 2 + 20, HEIGHT // 2 - 80),
    "CL3": (WIDTH // 2 + 80, HEIGHT // 2 - 80),


    "DL2": (WIDTH // 2 + 80, HEIGHT // 2 + 20),
    "DL3": (WIDTH // 2 + 80, HEIGHT // 2 + 80),
}



intersection_exit = {

    "AL1": (WIDTH // 2 - 20, HEIGHT // 2 + 80),

    "BL1": (WIDTH // 2 + 80, HEIGHT // 2 - 20),

    "CL1": (WIDTH // 2 + 20, HEIGHT // 2 - 80),

    "DL1": (WIDTH // 2 - 80, HEIGHT // 2 + 20),
}

# Final destinations (off screen)
final_destination = {
    "AL1": (WIDTH // 2 - 20, HEIGHT + 100),
    "BL1": (WIDTH + 100, HEIGHT // 2 - 20),
    "CL1": (WIDTH // 2 + 20, -100),
    "DL1": (-100, HEIGHT // 2 + 20),
}

# Map lanes to intersection sides
lane_to_intersection = {
    "AL2": "A", "AL3": "A",
    "BL2": "B", "BL3": "B",
    "CL2": "C", "CL3": "C",
    "DL2": "D", "DL3": "D"
}

# States for the lanes
lanes = {k: [] for k in lane_pos}
moving = []
intersection_busy = {"A": False, "B": False, "C": False, "D": False}

# Font for UI
font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 18)


def spawn_car(lane):
    """Spawn a car at the lane's starting position."""
    idx = len(lanes[lane])
    bx, by = lane_pos[lane]
    dx, dy = lane_dir.get(lane, (0, 0))

    # Spawn cars in a queue behind each other (AWAY from intersection)
    x = bx + dx * idx * LANE_SPACING
    y = by + dy * idx * LANE_SPACING

    is_priority = "L2" in lane
    lanes[lane].append({
        "x": x,
        "y": y,
        "priority": is_priority,
        "lane": lane
    })


def start_move():
    """Start moving a car from the queue."""
    if tg.moves.is_empty():
        return

    move = tg.moves.dequeue()
    if not move:
        return


    parts = move.split("::")
    route = parts[0]
    car_id = parts[1] if len(parts) > 1 else "unknown"

    src, dst = route.split("->")

    # VALIDATION: Check for impossible routes
    source_road = src[0]
    target_road = dst[0]

    if source_road == target_road:
        print(f"[ERROR] VISUAL: Impossible route detected: {src} -> {dst} for {car_id}")
        return  # Skip this impossible move

    direction = lane_to_intersection.get(src)

    # Check if intersection is busy for this direction
    if direction and intersection_busy[direction]:
        tg.moves.enqueue(move)  # requeue
        return

    # Spawn car if lane is empty visually
    if not lanes[src]:
        spawn_car(src)

    if lanes[src]:
        car = lanes[src].pop(0)
        if direction:
            intersection_busy[direction] = True

        moving.append({
            "x": car["x"],
            "y": car["y"],
            "phase": 0,
            "src": src,
            "dst": dst,
            "direction": direction,
            "priority": car.get("priority", False),
            "car_id": car_id
        })


def update_moving():
    """Update positions of moving cars through all phases."""
    for car in moving[:]:
        # Determine target based on phase
        if car["phase"] == 0:
            # Phase 0: Move from spawn to intersection entry
            tx, ty = intersection_approach[car["src"]]
        elif car["phase"] == 1:
            # Phase 1: Move to intersection center
            tx, ty = INTERSECTION
        elif car["phase"] == 2:
            # Phase 2: Move to intersection exit
            tx, ty = intersection_exit[car["dst"]]
        else:
            # Phase 3: Move to final destination (off screen)
            tx, ty = final_destination[car["dst"]]

        dx = tx - car["x"]
        dy = ty - car["y"]

        # Move towards target
        if abs(dx) > SPEED:
            car["x"] += SPEED if dx > 0 else -SPEED
        elif dx != 0:
            car["x"] = tx

        if abs(dy) > SPEED:
            car["y"] += SPEED if dy > 0 else -SPEED
        elif dy != 0:
            car["y"] = ty

        # Check if reached target
        if car["x"] == tx and car["y"] == ty:
            car["phase"] += 1

            # After phase 3, car is done - remove it
            if car["phase"] > 3:
                moving.remove(car)
                if car["direction"]:
                    intersection_busy[car["direction"]] = False


def draw_background():
    """Draw the background."""
    if bg:
        screen.blit(bg, (0, 0))
    else:
        screen.fill(ROAD_COLOR)

        # Draw intersection
        intersection_size = 160
        pygame.draw.rect(screen, LANE_COLOR,
                         (WIDTH // 2 - intersection_size // 2,
                          HEIGHT // 2 - intersection_size // 2,
                          intersection_size, intersection_size))

        # Draw roads
        road_width = 160
        # Vertical road
        pygame.draw.rect(screen, LANE_COLOR,
                         (WIDTH // 2 - road_width // 2, 0, road_width, HEIGHT))
        # Horizontal road
        pygame.draw.rect(screen, LANE_COLOR,
                         (0, HEIGHT // 2 - road_width // 2, WIDTH, road_width))

        # Draw lane labels
        label_a = font.render("A", True, (255, 255, 0))
        label_b = font.render("B", True, (255, 255, 0))
        label_c = font.render("C", True, (255, 255, 0))
        label_d = font.render("D", True, (255, 255, 0))

        screen.blit(label_a, (WIDTH // 2 - 10, HEIGHT - 100))  # Bottom
        screen.blit(label_b, (100, HEIGHT // 2 - 10))  # Left
        screen.blit(label_c, (WIDTH // 2 - 10, 100))  # Top
        screen.blit(label_d, (WIDTH - 120, HEIGHT // 2 - 10))  # Right


def draw_traffic_lights():
    """Draw traffic light indicators."""
    light_positions = {
        "A": (WIDTH // 2 - 220, HEIGHT - 80),  # Bottom
        "B": (80, HEIGHT // 2 - 220),  # Left
        "C": (WIDTH // 2 + 220, 80),  # Top
        "D": (WIDTH - 80, HEIGHT // 2 + 220)  # Right
    }

    lights_status = {
        "A": tg.LaneA_lights,
        "B": tg.LaneB_lights,
        "C": tg.LaneC_lights,
        "D": tg.LaneD_lights
    }

    for lane, pos in light_positions.items():
        color = GREEN_LIGHT if lights_status[lane] == "GREEN" else RED_LIGHT
        pygame.draw.circle(screen, color, pos, 15)
        pygame.draw.circle(screen, (255, 255, 255), pos, 15, 2)

        # Draw label
        label = font.render(f"{lane}", True, TEXT_COLOR)
        screen.blit(label, (pos[0] - 8, pos[1] - 35))


def draw_cars():
    """Draw all cars."""
    # Draw waiting cars
    for lane, cars in lanes.items():
        for car in cars:
            color = CAR_COLOR_PRIORITY if car.get("priority") else CAR_COLOR_NORMAL
            pygame.draw.rect(screen, color, (car["x"], car["y"], CAR_W, CAR_H))
            pygame.draw.rect(screen, (255, 255, 255), (car["x"], car["y"], CAR_W, CAR_H), 1)

    # Draw moving cars (same color as when waiting)
    for car in moving:
        color = CAR_COLOR_PRIORITY if car.get("priority") else CAR_COLOR_NORMAL
        pygame.draw.rect(screen, color, (car["x"], car["y"], CAR_W, CAR_H))
        pygame.draw.rect(screen, (255, 255, 255), (car["x"], car["y"], CAR_W, CAR_H), 2)

def draw():
    """Main draw function."""
    draw_background()
    draw_traffic_lights()
    draw_cars()
    pygame.display.flip()


# Main loop
MOVE_TIMER = 0
FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    MOVE_TIMER += clock.get_time()
    if MOVE_TIMER > 600:
        start_move()
        MOVE_TIMER = 0

    update_moving()
    draw()
    clock.tick(FPS)
        MOVE_TIMER = 0

    update_moving()
    draw()
    clock.tick(FPS)
