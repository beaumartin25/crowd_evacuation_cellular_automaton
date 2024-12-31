# Crowd Evacutation Cellular Automata

## Project Overview

This project simulates crowd evacuation scenarios using a cellular automata approach integrated with game theory principles. It aims to recreate and analyze evacuation conflicts by modeling agents on a grid environment, where each agent represents an individual in a crowd. The simulation evaluates both cooperative and defective strategies, showcasing how individuals make decisions under pressure to optimize their chances of a quick and safe evacuation. The integration of game theory helps simulate strategic interactions among agents, revealing insights into behavioral dynamics, cooperation, competition, and social influence in evacuation situations. This project demonstrates the intersection of cellular automata, decision-making algorithms, and game theory analysis in understanding complex evacuation dynamics and crowd behavior.


## Project Structure

`model.py`\
Contains the core `Evacuation` model, which is responsible for stepping through each agent's movement and updating the grid state in every iteration of the simulation.

`agents.py`\
Defines the `EvacuationAgent` class, which implements the game theory logic for decision-making, determining the optimal moves and interactions between agents in the evacuation process.

`app.py`\
Sets up and runs the simulation using Solaria, orchestrating the overall process, initializing agents, and managing the execution flow of the evacuation scenario.


## How to run

make sure to install \
```pip install -U mesa```\
as well as \
```pip install -U mesa[rec]```\
run app using \
```solara run app.py```
