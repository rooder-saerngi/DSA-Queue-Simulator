# dsa_queue_simulator
 

This File contains the workings and description of the assignment 

in this project there are two main files :
1.Traffic_Generator.py
2.simulator.py

1.Traffic_Generator.py:

Imports Time and threading for multithreading 
contains the code consisting of 12 queues named A,B,C,D lanes with L1,L2,L3 and L2 being the priority lane and L1 and L3 being normal lanes 
cars get generated with the generator() function in L2 and L3 and L1 is lane where the incoming cars are enqueued.

the main functions in this are :
1.Light_Changer() - changes the lights every couple of seconds from the two states of RED and GREEN 

2.generator() - generates cars every couple seconds, every 10 seconds for the Non priority Lane (L3) and every 5 seconds for the priority lane (L2)

3.Traversal() -implements traversal from one lane to another like BL2 to AL1, CL3 to AL1 

2.simulator.py :
work in progress 
going to implemnt visualisation of the traffic using pygame 





