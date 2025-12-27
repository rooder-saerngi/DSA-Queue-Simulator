# dsa_queue_simulator
 

This project is a traffic management simulator for a 4-way intersection, built to demonstrate how queue data structures can be used to control vehicle flow.
It combines data structures, multithreading, and real-time visualization using PyGame.

Features

Queue-based vehicle handling
Custom VehicleQueue and PriorityQueue classes manage cars in each lane.

Priority lane support (L2)
When more than 10 vehicles are waiting in a priority lane, it automatically gets higher priority.

Traffic light synchronization
Lanes A & C and B & D alternate green lights to avoid deadlock.

Real-time visualization
Vehicles, lanes, and traffic lights are rendered using PyGame.

Thread-safe execution
Multiple threads run safely using locks to prevent race conditions.


Data Structures Used:

| Data Structure   | Implementation        | Purpose               |
| ---------------- | --------------------- | --------------------- |
| `VehicleQueue`   | Custom FIFO queue     | Normal lanes (L1, L3) |
| `PriorityQueue`  | Custom priority queue | Priority lanes (L2)   |
| `threading.Lock` | Python lock           | Ensures thread safety |


Lane Configuration

4 Roads

A: Bottom

B: Left

C: Top

D: Right

3 Lanes per Road

L1 – Entry lane

L2 – Priority lane (straight movement)

L3 – Left-turn lane


Traffic Flow Logic
Normal Operation

Vehicles are served fairly from all lanes

L2 lanes act as priority lanes

L3 lanes handle left turns

High-Priority Condition

If an L2 lane has more than 10 vehicles:

Its priority is increased

Extra vehicles are moved immediately when the light turns green

Priority returns to normal once traffic reduces

Traffic Light System

A & C lanes turn green together (5 seconds)

B & D lanes turn green together (5 seconds)

Lights alternate continuously to prevent congestion and deadlocks

.
├── Traffic_Generator.py    # Core logic (queues, lights, vehicle generation)
├── Simulator.py            # PyGame visualization
├── Road.png                # Optional background image
└── README.md               # Project documentation

| FILE                     | Purpose                      |
| -------------------------| ---------------------------- |
| Traffic_Generator.py     | Core logic                   |          
| Simulator.py             |  PyGame visualization        |
| Road.png                 | image                        |
| README.md                | Project documentation        |


to run first install pygame:
(```pip install pygame```)

then run (```simulator.py```)

Key functions 
Traffic_Generator.py
| Function           | Purpose                      |
| ------------------ | ---------------------------- |
| `enqueue()`        | Add vehicle to queue         |
| `dequeue()`        | Remove vehicle (FIFO)        |
| `set_priority()`   | Adjust priority for L2 lanes |
| `move_car()`       | Move vehicle between lanes   |
| `lights_changer()` | Toggle traffic lights        |
| `generator()`      | Create vehicles              |
| `traversal()`      | Control vehicle movement     |

Simulator.py
| Function          | Purpose                      |
| ----------------- | ---------------------------- |
| `spawn_car()`     | Create a visual car          |
| `start_move()`    | Begin animation              |
| `update_moving()` | Update positions every frame |

Time Complexity

Queue operations: O(1)

Priority sorting: O(k log k)

Overall per cycle: O(n + k log k)

This is efficient enough for real-time simulation and scales well with traffic size.





