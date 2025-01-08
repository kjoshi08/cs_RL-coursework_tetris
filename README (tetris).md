
# Tetris-like Reinforcement Learning Game

This project is a Tetris-inspired game implemented with a focus on reinforcement learning concepts, particularly value function approximation using Q-learning. The goal of the game is to place blocks efficiently without exceeding a red boundary, earning rewards for optimal placements.

## Features

- **Game Mechanics**:
  - A 6x4 grid where blocks (2x2 yellow and 4x1 cyan) fall from the top.
  - Players can move blocks left, right, or let them drop.
  - Rows clear when completely filled, rewarding the player and altering the state.
  - The game ends when a block extends above the red boundary.

- **Reinforcement Learning**:
  - Q-learning with a neural network approximates the value function for state-action pairs.
  - Rewards:
    - +100 for successful block placement within the boundary.
    - No reward for intermediate steps unless a goal is achieved.

- **Grid Representation**:
  - Binary vector for cell occupancy.
  - Extra information for block type and position.

## Approximation of State Space

The state space was approximated using a combination of:

1. **Grid Configurations**:
   - 2^24 (6x4 grid) possible arrangements of filled and empty cells.

2. **Block Placements**:
   - 15 possible placements for the 2x2 yellow block.
   - 6 possible placements for the 4x1 cyan block.

   Combining these yields approximately 352 million states.

## Reinforcement Learning Strategy

- **State Representation**:
  - Flattened grid representation combined with block position data.

- **Q-Learning with Neural Network**:
  - A 3-layer neural network with ReLU activations predicts Q-values.
  - Updates follow the Bellman equation:
    \[
    Q(s, a) \leftarrow r + \gamma \max Q(s', a')
    \]

- **Epsilon-Greedy Exploration**:
  - Balances exploration (random actions) and exploitation (Q-value maximization).

## Game Code Overview

- **Gameplay**:
  - Developed in Python with Pygame for rendering.
  - Blocks fall automatically, with the player controlling movement.

- **AI Implementation**:
  - Q-learning updates based on state transitions, rewards, and terminal conditions.
  - Training involves approximating Q-values for effective gameplay.

- **Rewards**:
  - +100 for placing a block within bounds.
  - Additional rewards for clearing rows.

## How to Play

1. Run the game script (`pygame` required).
2. Use predefined moves to guide the blocks.
3. The game ends either when time runs out or a block crosses the red boundary.

