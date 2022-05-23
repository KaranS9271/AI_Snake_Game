# **SNAKE GAME USING DEEP LEARNING**

## **DESCRIPTION**

   The goal of the game is to reach the target pixel, which changes position every time you reach it, without hitting the boundary or any obstacle or yourself (you are the line). The line keeps getting longer constantly as you reach the target pixel, in some games the tail stays fixed whereas in some the tail keeps moving. Our goal in this project is to train the machine in a way that it can play the aforementioned snake game without any user interaction. For this purpose, we propose a Reinforcement Learning algorithm. The few algorithms we will explore are Deep Q Learning and Actor-Critic method. In this project, we emphasize implementing the Actor-Critic model within the “Snake Classics” game. The Actor-Critic method outperforms existing models by interlinking value and policy-based reinforcement learning in a single algorithm. In the Actor-Critic method, the Actor is a policy-based model that selects the action and maps states to action probabilities, whereas the Critic is a value-based model that evaluates the state by mapping the input states to Q-values. The model can work with continuous action space problems offering a better convergence rate and reducing learning time. Further, we aim to build a comparative analysis of the Actor-Critic method with Deep- Q Learning, A* Algorithm, BFS, and Hamiltonian Cycle methods respectively.   

## INSTALL AND RUN PROJECT

Navigate to the stored folder and run below commands on the terminal: 
    
    python main.py "basic"

    python main.py "hamiltonian"

    python main.py "bfs"

    python main.py "astar"

    python main.py "astar2"

    python main.py "dql"

    python main.py "a2c"

## PROJECT STRUCTURE

### Actor_Critic: directory for the Actor-Critic algorithm

    actor_critic.py :  contains actor-critic network
    reinforce.py : contains Reinforce network
    rlsnake_env.py : sets the snake game environment
    rlsnake_env_v1: sets the snake game environment
    simulate.py : display action on the screen for the snake game
    tfagent.py : tensorflow agent which selects action
    train.py: train the actor-critic model

### A* Algorithm
    Astar/Astar.py: code for running A* algorithm
    Astar2/Astar2.py: code for running A* algorithm (different heuristic, here Manhattan distance)


### Bfs snake: directory for the Breadth-First Search algorithm.
    
    bfs_snake_game.py: contains Snake and Sqaure class
    BFS.py: contains code for running the project
    Config.py: contains game settings and global variables like width, height, etc.


### Deep_Q_Learning: directory for Deep Q Learning algorithm.
    
    agents.py: store the memory of past experiences for Deep Q Learning
    helper.py: for plotting the graph for learning
    model.py: code for Deep Q learning algorithm
    snake_game.py: interface (User Interface) for Deep Q Learning algorithm

### Main Files

    main.py: main file for running all algorithm

    requirement.txt: required module for running the project 

### Technologies Used
    - Python
    - Pygame
    - Tensorflow
    - SDL2
    - SDL2.dll
    - tqdm
    - NumPy
    - Gym

## How does it work?
### Hamitonian Implementation:

  The Hamiltonian path is a path on the graph (directed or undirected graph) that visits each vertex exactly once. Hamiltonian on snake game ensures that a snake will never intercept itself, guaranteeing to win the game every single time. 
 
<p align="center">
<img src=https://user-images.githubusercontent.com/93997063/169721490-c738b08c-789b-4d86-b2f2-8093c13e31b6.gif width = 75% align = "right" alt = "Hamiltonian"></img>
</p>

### Breadth-First Search:

  The snake follows the Breadth-First Search algorithm:
1.	The snake finds the shortest path between the apple and its head (call it path_1). If path_1 is not available, then make the original snake follow path_1. 
2.	Make the original snake follow path_1 by creating a virtual snake identical to the original snake.
3.	Check if the path between the virtual snake's head and its tail is available (let's call it path_2), when the virtual snake reaches the apple, if so, then make the original snake follow path_1.
 
<p align="center">
<img src=https://user-images.githubusercontent.com/93997063/169722630-e1d6510f-f91d-4dcb-830b-268e2b9b1f3b.gif width = 75% align = "right" alt = "BFS"></img>
</p>

### A* Algorithm:
1.	Create start and end nodes.
2.	Initialize both open and closed lists.
3.	Add the start node to the open list. Loop until you find the end.
4.	Search for the adjacent squares.
5.	Get the current node. Pop current off the open list and add to the closed list.
6.	Generate a child list. Get node position and make sure it is within range and a walkable terrain.
7.	Create a new node and append it to the child list loop through the child list. If a child is on a closed list. Create f, g, and h values.
8.	If a child is already on the open list continue and add a child to the open list.
Generate matrix of current state to pass A* algorithm.
 
<p align="center">
<img src=https://user-images.githubusercontent.com/93997063/169722646-d06872c0-40cf-42d3-b54a-de2cf079075d.gif width = 75% align = "right" alt = "ASTAR"></img>
</p>

### A2* algorithm:
Here we change the heuristic of the algorithm where we use Manhattan distance to the endpoint. And when finding the goal, create a list named path which returns the reversed path. 

<p align="center">
<img src=https://user-images.githubusercontent.com/93997063/169722661-3b8b9348-a42f-4910-97f6-8e1c1b3032db.gif width = 75% align = "right" alt = "ASTAR2"></img>
</p>

### Deep Q Learning algorithm:
  Here we use a neural network to approximate the Q-value function. The state is given as input and the Q-value of all possible actions is generated as output. 
1.	The memory of all past experiences is stored in memory.
2.	The maximum of the Q-network determines the next action.
3.	Here we took the Mean Squared Error of the predicted Q-value and target Q-value.
4.	Updating the Q-value is done using the Bellman equation.


<p align="center">
<img src=https://user-images.githubusercontent.com/93997063/169722675-b4ca6642-4da1-45ce-97e3-441d6f101faf.gif width = 75% alt = "DQL"></img>
</p>

### Result: 

<p align="center">
   &nbsp &nbsp &nbsp &nbsp & nbsp
   <img src=https://user-images.githubusercontent.com/93997063/169722678-51170dc8-df4a-42e8-a410-7aadada497d0.JPG width = 75% alt = "DLQ_Results"></img>
</p>



### Actor-Critic Method:
  Actor-Critic consists of two component: Actor and Critic. Actor approximates the agent policy directly. Policy is probability distribution over the set of actions where we take state as input and output of probability of selecting each action. Critic approximates the value function. It tells how good an action is based on whether or not resulting state is valuable. So Actor selects the action, the critic evaluate the state and result is compares to the reward from the environment. Updates of weights of deep neural network is carried out at each time step as Actor Critic belong to class called as Temporal difference learning.
1.	Initialize actor critic network. The network is series of fully connected layers that maps from environment observation to a point in environment space. 
2.	Fed network to TensorFlow agent. TensorFlow agent selects action according to actor network (probability distribution)
3.	Repeat for large number of episodes:
4.	Reset the environment, score (here old_score), terminal flag (here game_over)
5.	While state is not terminal
a.	Select action according to actor network.
b.	Take action and receive reward and new state
6.	Plot scores over time to show learning.
 
Actor-Critic 4x4 grid

<p align="center">
<img src=https://user-images.githubusercontent.com/93997063/169722699-b2fedc17-4faf-45db-bc3a-f688d145e6ee.gif width = 60% align = "right" alt = "DLQ_Results"></img>
</p>
 

Actor-Critic 10x10 grid

<p align="center">
<img src=https://user-images.githubusercontent.com/93997063/169722703-5172f76e-5ea9-447b-a03e-b977a3403177.gif
     width = 75% align = "right" alt = "Actor Critic (10 * 10 grid)"></img>
</p>
