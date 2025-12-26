import time
import threading
#Making the class for Queue
class Queue:
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

#creating a queue for the lanes
lanes = {
    "AL1": Queue(), "AL2": Queue(), "AL3": Queue(),
    "BL1": Queue(), "BL2": Queue(), "BL3": Queue(),
    "CL1": Queue(), "CL2": Queue(), "CL3": Queue(),
    "DL1": Queue(), "DL2": Queue(), "DL3": Queue(),
}
moves = Queue()
#Traffic Lights (every ten seconds the lights change )
LaneA_lights = "RED"
LaneB_lights = "RED"
LaneC_lights = "RED"
LaneD_lights = "RED"
def lights_changer():
    global LaneA_lights, LaneB_lights, LaneD_lights, LaneC_lights
    flag = True
    while True :
        if flag :
            LaneA_lights = "GREEN"
            LaneB_lights = "RED"
            LaneD_lights = "RED"
            LaneC_lights = "GREEN"
            print("A:",LaneA_lights,"B:",LaneB_lights,"D:",LaneD_lights,"C:",LaneC_lights,"\n")

            flag = False
            time.sleep(9)
        else :
            LaneA_lights = "RED"
            LaneB_lights = "GREEN"
            LaneD_lights = "GREEN"
            LaneC_lights = "RED"
            print("A:",LaneA_lights,"B:",LaneB_lights,"D:",LaneD_lights,"C:",LaneC_lights,"\n")
            flag = True
            time.sleep(9)


def generator():
    i =0
    while True :
        #for the non priority lanes (cars are generated every 10 seconds)
        lanes["AL3"].enqueue(f"car_AL3_{i}")
        lanes["BL3"].enqueue(f"car_BL3_{i}")
        lanes["CL3"].enqueue(f"car_CL3_{i}")
        lanes["DL3"].enqueue(f"car_DL3_{i}")
        print(f"Generated cars {i} in AL3, BL3, CL3, DL3\n")

        time.sleep(10)

        #for the priority lanes (cars are generated every 5 seconds)

        lanes["AL2"].enqueue(f"car_AL2_{i}")
        lanes["BL2"].enqueue(f"car_BL2_{i}")
        lanes["CL2"].enqueue(f"car_CL2_{i}")
        lanes["DL2"].enqueue(f"car_DL2_{i}")
        print(f"Generated cars {i} in AL2, BL2, CL2, DL2\n")
        i += 1

        time.sleep(5)


def traversal():
    global LaneA_lights, LaneB_lights, LaneC_lights, LaneD_lights
    global moves

    while True:
        al2_size = lanes["AL2"].size()
        priority_mode = al2_size > 10

        if LaneA_lights == "GREEN":
            if priority_mode:
                if not lanes["AL2"].is_empty():
                    car = lanes["AL2"].dequeue()
                    lanes["BL1"].enqueue(car)
                    print("PRIORITY: AL2 car moved to BL1")
                    moves.enqueue("AL2->BL1")

                    if lanes["AL2"].size() < 5:
                        priority_mode = False
            else:
                if not lanes["AL2"].is_empty():
                    car = lanes["AL2"].dequeue()
                    lanes["BL1"].enqueue(car)
                    print("AL2 car moved to BL1")
                    moves.enqueue("AL2->BL1")

                if not lanes["AL3"].is_empty():
                    car = lanes["AL3"].dequeue()
                    lanes["CL1"].enqueue(car)
                    print("AL3 car moved to CL1")
                    moves.enqueue("AL3->CL1")

        if LaneB_lights == "GREEN":
            if priority_mode and LaneA_lights != "GREEN":
                if not lanes["AL2"].is_empty():
                    car = lanes["AL2"].dequeue()
                    lanes["BL1"].enqueue(car)
                    print("PRIORITY OVERRIDE: AL2 car moved to BL1 (B green)")
                    moves.enqueue("AL2->BL1")

                    if lanes["AL2"].size() < 5:
                        priority_mode = False
            else:
                if not lanes["BL2"].is_empty():
                    car = lanes["BL2"].dequeue()
                    lanes["CL1"].enqueue(car)
                    print("BL2 car moved to CL1")
                    moves.enqueue("BL2->CL1")

                elif not lanes["BL3"].is_empty():
                    car = lanes["BL3"].dequeue()
                    lanes["AL1"].enqueue(car)
                    print("BL3 car moved to AL1")
                    moves.enqueue("BL3->AL1")

        if LaneD_lights == "GREEN":
            if priority_mode and LaneA_lights != "GREEN":
                if not lanes["AL2"].is_empty():
                    car = lanes["AL2"].dequeue()
                    lanes["BL1"].enqueue(car)
                    print("PRIORITY OVERRIDE: AL2 car moved to BL1 (D green)")
                    moves.enqueue("AL2->BL1")

                    if lanes["AL2"].size() < 5:
                        priority_mode = False
            else:
                if not lanes["DL2"].is_empty():
                    car = lanes["DL2"].dequeue()
                    lanes["CL1"].enqueue(car)
                    print("DL2 car moved to CL1")
                    moves.enqueue("DL2->CL1")

                elif not lanes["DL3"].is_empty():
                    car = lanes["DL3"].dequeue()
                    lanes["AL1"].enqueue(car)
                    print("DL3 car moved to AL1")
                    moves.enqueue("DL3->AL1")

        if LaneC_lights == "GREEN":
            if priority_mode and LaneA_lights != "GREEN":
                if not lanes["AL2"].is_empty():
                    car = lanes["AL2"].dequeue()
                    lanes["BL1"].enqueue(car)
                    print("PRIORITY OVERRIDE: AL2 car moved to BL1 (C green)")
                    moves.enqueue("AL2->BL1")

                    if lanes["AL2"].size() < 5:
                        priority_mode = False
            else:
                if not lanes["CL2"].is_empty():
                    car = lanes["CL2"].dequeue()
                    lanes["DL1"].enqueue(car)
                    print("CL2 car moved to DL1")
                    moves.enqueue("CL2->DL1")

                elif not lanes["CL3"].is_empty():
                    car = lanes["CL3"].dequeue()
                    lanes["BL1"].enqueue(car)
                    print("CL3 car moved to BL1")
                    moves.enqueue("CL3->BL1")

        time.sleep(1)
if __name__ == "__main__":
    print("Running Traffic Generator directly")
    threading.Thread(target=lights_changer, daemon=True).start()
    threading.Thread(target=generator, daemon=True).start()
    threading.Thread(target=traversal, daemon=True).start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped")
