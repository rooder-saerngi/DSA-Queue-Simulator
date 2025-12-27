import time
import threading

# ------------------- QUEUE CLASSES -------------------

class VehicleQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, element):
        self.queue.append(element)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def __str__(self):
        return str(self.queue)


class PriorityQueue:
    def __init__(self, max_size=10):
        self.queue = []  # Store tuples: (priority, element)
        self.max_size = max_size

    def enqueue(self, element, priority=0):
        self.queue.append((priority, element))
        self.queue.sort(key=lambda x: x[0])

    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)[1]

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return self.size() > self.max_size

    def change_priority(self, new_priority):
        if self.queue:
            elements = [elem for _, elem in self.queue]
            self.queue = [(new_priority, elem) for elem in elements]
            self.queue.sort(key=lambda x: x[0])

    def __str__(self):
        return str([elem for _, elem in self.queue])


# ------------------- LANES & MOVES -------------------

lanes = {
    "AL1": VehicleQueue(), "AL2": PriorityQueue(), "AL3": VehicleQueue(),
    "BL1": VehicleQueue(), "BL2": PriorityQueue(), "BL3": VehicleQueue(),
    "CL1": VehicleQueue(), "CL2": PriorityQueue(), "CL3": VehicleQueue(),
    "DL1": VehicleQueue(), "DL2": PriorityQueue(), "DL3": VehicleQueue(),
}

moves = VehicleQueue()

# Exit mapping: all cars go straight
lane_exit = {
    "AL2": "AL1",
    "AL3": "AL1",
    "BL2": "BL1",
    "BL3": "BL1",
    "CL2": "CL1",
    "CL3": "CL1",
    "DL2": "DL1",
    "DL3": "DL1",
}

# ------------------- TRAFFIC LIGHTS -------------------

LaneA_lights = "RED"
LaneB_lights = "RED"
LaneC_lights = "RED"
LaneD_lights = "RED"
flag = True

def lights_changer():
    global LaneA_lights, LaneB_lights, LaneC_lights, LaneD_lights, flag

    while True:
        if flag:
            LaneA_lights = "GREEN"
            LaneB_lights = "RED"
            LaneD_lights = "RED"
            LaneC_lights = "GREEN"
            print(f"A:{LaneA_lights} B:{LaneB_lights} D:{LaneD_lights} C:{LaneC_lights}\n")
            flag = False
            time.sleep(9)
        else:
            LaneA_lights = "RED"
            LaneB_lights = "GREEN"
            LaneD_lights = "GREEN"
            LaneC_lights = "RED"
            print(f"A:{LaneA_lights} B:{LaneB_lights} D:{LaneD_lights} C:{LaneC_lights}\n")
            flag = True
            time.sleep(9)

# ------------------- CAR GENERATOR -------------------

added = VehicleQueue()

def generator():
    global added
    i = 0
    while True:
        # Generate non-priority L3 lanes every 10 seconds
        for lane_name in ["AL3", "BL3", "CL3", "DL3"]:
            lanes[lane_name].enqueue(f"car_{lane_name}_{i}")
            print(f"Generated cars {i} in AL3, BL3, CL3, DL3")
            added.enqueue(f"car in {lane_name}")

        time.sleep(10)

        # Generate priority L2 lanes with size-based priority
        for lane_name in ["AL2", "BL2", "CL2", "DL2"]:
            lane = lanes[lane_name]
            priority = -10 if lane.size() > 10 else 0
            lane.enqueue(f"car_{lane_name}_{i}", priority=priority)
            print(f"Generated cars {i} in {lane_name}")
            added.enqueue(f"car in {lane_name}")

        i += 1
        time.sleep(10)

# ------------------- PRIORITY & MOVEMENT -------------------

def set_priority(lane_name):
    """Set priority for an L2 lane based on its size."""
    lane = lanes[lane_name]
    if lane.size() > 10:
        lane.change_priority(-10)  # High priority
    else:
        lane.change_priority(0)    # Normal priority

def move_car(lane_name):
    """Dequeue from a lane and enqueue to its straight exit."""
    lane = lanes[lane_name]
    if not lane.is_empty():
        car = lane.dequeue()
        target_lane = lane_exit[lane_name]
        lanes[target_lane].enqueue(car)
        print(f"{lane_name} car moved to {target_lane}")
        moves.enqueue(f"{lane_name}->{target_lane}")

# ------------------- TRAVERSAL -------------------

def traversal():
    global LaneA_lights, LaneB_lights, LaneC_lights, LaneD_lights

    while True:
        # Update priorities for all L2 lanes
        for l2_lane in ["AL2", "BL2", "CL2", "DL2"]:
            set_priority(l2_lane)

            # If L2 lane has more than 10 cars, move excess to L1 straight
            lane = lanes[l2_lane]
            while lane.size() > 10:
                print(f"{l2_lane} has more than 10 cars, moving excess to {lane_exit[l2_lane]}")
                move_car(l2_lane)

        # Traffic light green logic - straight only
        if LaneA_lights == "GREEN":
            move_car("AL2")
            move_car("AL3")
        if LaneB_lights == "GREEN":
            move_car("BL2")
            move_car("BL3")
        if LaneC_lights == "GREEN":
            move_car("CL2")
            move_car("CL3")
        if LaneD_lights == "GREEN":
            move_car("DL2")
            move_car("DL3")

        time.sleep(1)

# ------------------- MAIN -------------------

if __name__ == "__main__":
    print("Running Traffic Generator directly")
    threading.Thread(target=lights_changer, daemon=True).start()
    threading.Thread(target=generator, daemon=True).start()
    threading.Thread(target=traversal, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped")
