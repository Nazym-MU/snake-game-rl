import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 30

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
    
        
    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.prev_distance = self._get_distance_to_food()
        self.moves_without_progress = 0
        self.last_positions = []

    def _get_distance_to_food(self):
        """Calculate Manhattan distance from snake's head to food"""
        return abs(self.head.x - self.food.x) + abs(self.head.y - self.food.y)
    
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
    
    def _is_circular_movement(self):
        """Detect if snake is moving in circles"""
        self.last_positions.append(self.head)
        if len(self.last_positions) > 8:
            self.last_positions.pop(0)
            
            if self.head in self.last_positions[:-1]:
                return True
        return False
    
    def _calculate_reward(self, game_over, ate_food):
        """Caclulate the reward for the current state"""
        reward = 0

        reward -= 0.5 # step penalty

        current_distance = self._get_distance_to_food()
        if current_distance < self.prev_distance:
            reward += 1
            self.moves_without_progress = 0
        else:
            reward -= 1
            self.moves_without_progress += 1
        
        self.prev_distance = current_distance

        if self._is_circular_movement():
            reward -= 5
        
        if self.moves_without_progress > 10:
            reward -= self.moves_without_progress * 0.5

        if game_over:
            reward -= 20
        elif ate_food:
            reward += 30
            self.moves_without_progress = 0

            efficiency_bonus = max(0, 100 - self.frame_iteration)
            reward += efficiency_bonus
        
        if not game_over and not ate_food:
            max_distance = self.w + self.h
            distance_percentage = current_distance / max_distance
            reward += (1 - distance_percentage) * 2
        
        return reward
        
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        ate_food = False

        if self.is_collision():
            game_over = True

        max_steps = min(100 * len(self.snake), self.w * self.h // (BLOCK_SIZE ** 2))
        if self.frame_iteration > max_steps:
            game_over = True
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            ate_food = True
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        reward = self._calculate_reward(game_over, ate_food)
        
        # 6. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]
        
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            