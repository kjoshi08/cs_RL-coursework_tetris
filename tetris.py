import pygame
import random
import sys
import time


# Pygame initialization
pygame.init()


# Constants
GRID_WIDTH, GRID_HEIGHT = 6, 4  # Grid dimensions
CELL_SIZE = 50  # Pixel size of each cell
WINDOW_WIDTH, WINDOW_HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE + 50  # Extra height for score display
FPS = 1  # Slow down the game


# Colors
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Block types
BLOCKS = {
    "yellow": {"shape": [(0, 0), (0, 1), (1, 0), (1, 1)], "color": YELLOW},  # 2x2 block
    "cyan": {"shape": [(0, 0), (1, 0), (2, 0), (3, 0)], "color": CYAN}  # 4x1 block
}


# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("6x4 Tetris with Rewards")


# Game variables
clock = pygame.time.Clock()
game_over = False
score = 0
reward = 0
start_time = time.time()  # Record start time


# Game grid
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]




# Function to draw the game grid and blocks
def draw_grid():
    screen.fill(BLACK)
    # Draw the red border around the grid
    pygame.draw.rect(screen, RED, (0, 50, WINDOW_WIDTH, WINDOW_HEIGHT - 50), 3)


    # Draw the grid cells
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col]:
                pygame.draw.rect(screen, grid[row][col],
                                 (col * CELL_SIZE, row * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE), 1)




# Function to display score and reward
def display_score_and_reward():
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    reward_text = font.render(f"Reward: {reward}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(reward_text, (WINDOW_WIDTH - 150, 10))




# Function to check if a position is within bounds
def is_within_bounds(x, y):
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT




# Function to check if a block can be placed at a given position
def can_place_block(block, x, y):
    for cell in block["shape"]:
        cell_x, cell_y = x + cell[1], y + cell[0]
        if not is_within_bounds(cell_x, cell_y) or grid[cell_y][cell_x]:
            return False
    return True




# Function to place a block on the grid
def place_block(block, x, y):
    for cell in block["shape"]:
        cell_x, cell_y = x + cell[1], y + cell[0]
        if is_within_bounds(cell_x, cell_y):
            grid[cell_y][cell_x] = block["color"]




# Function to clear full rows and update the score
def clear_rows():
    global score, reward
    cleared_rows = 0
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            grid.pop(row)
            grid.insert(0, [None] * GRID_WIDTH)
            cleared_rows += 1
    reward += cleared_rows * 100  # Reward for cleared rows
    score += cleared_rows * 100




# Function to check if game over condition is met
def check_game_over(block, x, y):
    for cell in block["shape"]:
        cell_x, cell_y = x + cell[1], y + cell[0]
        if cell_y < 0:
            return True
    return False




# Function to get a random block
def get_random_block():
    block_type = random.choice(list(BLOCKS.keys()))
    return BLOCKS[block_type]




# Function to execute a list of moves for the block
def execute_moves(block, x, y, moves):
    global reward, game_over
    for move in moves:
        if move == "left" and can_place_block(block, x - 1, y + 1):
            x -= 1
        elif move == "right" and can_place_block(block, x + 1, y + 1):
            x += 1
        y += 1  # Move down each step


        # Check if block placement is valid, place the block if it can't move further
        if not can_place_block(block, x, y):
            if check_game_over(block, x, y - 1):
                game_over = True
                return x, y - 1  # Return current position to avoid NoneType error
            place_block(block, x, y - 1)
            clear_rows()
            reward += 100  # Reward for placing a block without extending above red rectangle
            break
    return x, y




# Game loop
current_block = get_random_block()
block_x, block_y = GRID_WIDTH // 2 - 1, -1  # Start above the grid


# Expanded move list for longer gameplay
moves = ["left", "right", "left", "right", "left", "left", "right", "left", "right", "right"] * 50  # Longer moves


# Set game duration to 5 minutes (300 seconds)
game_duration = 300


while not game_over:
    elapsed_time = time.time() - start_time
    if elapsed_time >= game_duration:  # Stop game after set duration
        break


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Execute the predefined moves
    block_x, block_y = execute_moves(current_block, block_x, block_y, moves)
    moves = []  # Clear moves after execution


    # If no more moves, get a new block
    if not moves:
        current_block = get_random_block()
        block_x, block_y = GRID_WIDTH // 2 - 1, -1
        moves = ["left", "right", "left", "right", "left", "left", "right", "left", "right", "right"] * 50


    # Draw everything
    draw_grid()
    display_score_and_reward()  # Display score and reward


    # Draw current block
    for cell in current_block["shape"]:
        cell_x, cell_y = block_x + cell[1], block_y + cell[0]
        if is_within_bounds(cell_x, cell_y):
            pygame.draw.rect(screen, current_block["color"],
                             (cell_x * CELL_SIZE, cell_y * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))


    pygame.display.flip()
    clock.tick(FPS)


# End the game after specified duration
screen.fill(BLACK)
font = pygame.font.SysFont(None, 55)
text = font.render("Time's Up! Game Over!", True, RED)
screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()