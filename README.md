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








