# Snake Game AI with Reinforcement Learning

This project implements an AI that learns to play the Snake game using Reinforcement Learning, specifically Q-Learning with PyTorch. The implementation is based on the tutorial by Patrick Loeber [Python Engineer](https://youtu.be/L8ypSXwyBds?si=kX0KxCnwEvtvc6QZ) with additional improvements to the reward system and game mechanics.

## Project Overview

The AI agent learns to play Snake through trial and error, using a neural network to approximate Q-values for different actions. The project includes several improvements over the basic implementation:

- Enhanced reward system with distance-based rewards
- Anti-pattern penalties to prevent circular movement
- Efficiency bonuses for quick food collection
- Dynamic timeout adjustments based on snake length

## Requirements

```
pygame
torch
numpy
matplotlib
ipython
```

## Project Structure

- `snake_pygame.py`: Contains the Snake game implementation
- `agent.py`: Implements the AI agent using Q-learning
- `model.py`: Defines the neural network architecture and training logic
- `plot.py`: Contains utility functions for plotting training progress

## Features

### Game Mechanics
- Classic Snake game implementation using Pygame
- Customizable game parameters (board size, speed, block size)
- Score tracking and visual display

### AI Implementation
- Deep Q-Learning with PyTorch
- Epsilon-greedy exploration strategy
- Experience replay for better learning
- State representation including:
  - Danger detection in different directions
  - Food location relative to snake
  - Current direction
  - Collision detection

### Training Improvements
- Progressive reward system
- Anti-circular movement penalties
- Distance-based rewards
- Efficiency bonuses
- Dynamic timeout adjustments

## How to Run

1. Install the required packages:
```bash
pip install pygame torch numpy matplotlib ipython
```

2. Run the training:
```bash
python agent.py
```

## Code Structure

### Snake Game (`snake_pygame.py`)
- `SnakeGameAI` class: Implements the game logic
- Custom reward calculation
- State management
- Movement and collision detection

### Agent (`agent.py`)
- `Agent` class: Implements the AI logic
- State processing
- Action selection
- Memory management
- Training loops

### Model (`model.py`)
- `Linear_QNet`: Neural network architecture
- `QTrainer`: Training implementation
- Model saving/loading functionality

### Helper (`helper.py`)
- Plotting functionality for training progress
- Performance visualization

## Training Process

The agent learns through the following process:
1. Gets the current state
2. Predicts action through the neural network
3. Performs the action and gets reward
4. Updates its memory
5. Learns from its memory through experience replay

## Model Architecture

The neural network consists of:
- Input layer (11 neurons)
- Hidden layer (256 neurons)
- Output layer (3 neurons - [straight, right, left])

## Acknowledgments

This project is based on the tutorial by Patrick Loeber (Python Engineer) with additional improvements to enhance learning efficiency and prevent common issues like circular movement patterns.

## Improvements Over Original Tutorial

1. Enhanced Reward System:
   - Added distance-based rewards
   - Implemented anti-pattern penalties
   - Added efficiency bonuses
   - Improved progress tracking

2. Game Mechanics:
   - Dynamic timeout adjustments
   - Better collision detection
   - Circular movement prevention

3. State Management:
   - Improved state representation
   - Better position tracking
   - Enhanced food placement logic

## Future Improvements

Potential areas for further enhancement:
- Implementing prioritized experience replay
- Adding different neural network architectures
- Implementing A3C or other advanced RL algorithms
- Adding different difficulty levels
- Implementing curriculum learning