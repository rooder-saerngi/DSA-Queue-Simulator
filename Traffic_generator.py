import time
import threading


# Making classes for the VehicleQueue
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
        return self.size() >= self.max_size

    def change_priority(self, new_priority):
        if self.queue:
            elements = [elem for _, elem in self.queue]
            self.queue = [(new_priority, elem) for elem in elements]
            self.queue.sort(key=lambda x: x[0])

    def __str__(self):
        return str([elem for _, elem in self.queue])


# Making a dictionary for the lanes
lanes = {
    "AL1": VehicleQueue(), "AL2": PriorityQueue(), "AL3": VehicleQueue(),
    "BL1": VehicleQueue(), "BL2": PriorityQueue(), "BL3": VehicleQueue(),
    "CL1": VehicleQueue(), "CL2": PriorityQueue(), "CL3": VehicleQueue(),
    "DL1": VehicleQueue(), "DL2": PriorityQueue(), "DL3": VehicleQueue(),
}

moves = VehicleQueue()

lane_exit = {
     # A lanes
    "AL2": "BL1",  
    "AL3": "CL1",  

    # B lanes
    "BL2": "AL1",  
    "BL3": "DL1", 

    # C lanes
    "CL2": "DL1", 
    "CL3": "AL1",  

    # D lanes
    "DL2": "BL1",  
    "DL3": "CL1",  
}

# Traffic lights initialization
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
            print(f"[LIGHTS] A:GREEN B:RED C:GREEN D:RED")
            flag = False
            time.sleep(5)
        else:
            LaneA_lights = "RED"
            LaneB_lights = "GREEN"
            LaneD_lights = "GREEN"
            LaneC_lights = "RED"
            print(f"[LIGHTS] A:RED B:GREEN C:RED D:GREEN")
            flag = True
            time.sleep(5)


# Generator for the vehicles in each lane
car_counter = 0


def generator():
    global car_counter

    while True:
        # Generate non-priority L3 lanes (left turn) every 5 seconds
        for lane_name in ["AL3", "BL3", "CL3", "DL3"]:
            lanes[lane_name].enqueue(f"car_{lane_name}_{car_counter}")
        print(f"[GEN] Generated cars {car_counter} in L3 lanes (left turn)")

        time.sleep(2.5)

        # Generate priority L2 lanes (straight) with size-based priority
        for lane_name in ["AL2", "BL2", "CL2", "DL2"]:
            lane = lanes[lane_name]
            priority = -10 if lane.size() > 10 else 0
            lane.enqueue(f"car_{lane_name}_{car_counter}", priority=priority)
        print(f"[GEN] Generated cars {car_counter} in L2 lanes (priority/straight)")

        car_counter += 1
        time.sleep(2.5)


# Priority setter
def set_priority(lane_name):
    """Set priority for an L2 lane based on its size."""
    lane = lanes[lane_name]
    if lane.size() > 10:
        lane.change_priority(-10)  # High priority
    else:
        lane.change_priority(0)  # Normal priority


# Traversal for the cars
def move_car(lane_name):
    """Dequeue from a lane and enqueue to its exit lane."""
    lane = lanes[lane_name]
    if not lane.is_empty():
        car = lane.dequeue()
        target_lane = lane_exit[lane_name]

        # VALIDATION: Check for impossible routes
        source_road = lane_name[0]  # A, B, C, or D
        target_road = target_lane[0]

        # A car should NEVER return to the same road it came from
        if source_road == target_road:
            print(f"[ERROR] IMPOSSIBLE ROUTE: {car} trying to go {lane_name} -> {target_lane}")
            print(f"[ERROR] This should never happen! Check lane_exit mapping!")
            return False

        print(f"[MOVE] {car} from {lane_name} -> {target_lane}")
        moves.enqueue(f"{lane_name}->{target_lane}::{car}")
        return True
    return False

def stats_display():
    """Display current lane statistics."""
    while True:
        time.sleep(10)
        print("\n" + "="*60)
        print("LANE STATISTICS & ROUTES:")
        print("="*60)
        for lane_name in sorted(lanes.keys()):
            if "L1" in lane_name:
                continue  # Skip entry lanes
            size = lanes[lane_name].size()
            target = lane_exit.get(lane_name, "N/A")
            lane_type = "Priority" if "L2" in lane_name else "Left Turn"
            print(f"{lane_name} -> {target} ({lane_type}): {size} vehicles")
        print(f"Moves pending: {moves.size()}")
        print("="*60 + "\n")


def traversal():
    global LaneA_lights, LaneB_lights, LaneC_lights, LaneD_lights

    while True:
        # Update priorities for all L2 lanes
        for l2_lane in ["AL2", "BL2", "CL2", "DL2"]:
            set_priority(l2_lane)

            # If L2 lane has more than 10 cars, move excess immediately
            lane = lanes[l2_lane]
            if lane.size() > 10:
                print(f"[PRIORITY] {l2_lane} has {lane.size()} cars (>10), moving excess")
                while lane.size() > 10:
                    move_car(l2_lane)

        # Traffic light green logic - move cars when light is green
        if LaneA_lights == "GREEN":
            move_car("AL2")  # Priority lane (straight)
            move_car("AL3")  # Left turn lane

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

# So that the file doesn't auto run while being imported in the simulator
if __name__ == "__main__":

    threading.Thread(target=lights_changer, daemon=True).start()
    threading.Thread(target=generator, daemon=True).start()
    threading.Thread(target=traversal, daemon=True).start()
    threading.Thread(target=stats_display, daemon=True).start()


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped")
