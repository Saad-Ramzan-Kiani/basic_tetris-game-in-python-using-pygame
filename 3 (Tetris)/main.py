import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (128, 0, 128)   # Purple
]

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

class Tetris:
    def __init__(self, width, height):
        self.width = width // GRID_SIZE
        self.height = height // GRID_SIZE
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.current_shape = self.new_shape()
        self.shape_x = self.width // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        self.game_over = False
        self.score = 0

    def new_shape(self):
        return random.choice(SHAPES)

    def draw_grid(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 0:
                    color = WHITE
                else:
                    color = COLORS[self.board[y][x] - 1]
                pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def draw_shape(self, screen):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[cell - 1], 
                                     ((self.shape_x + x) * GRID_SIZE, (self.shape_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, GRAY, 
                                     ((self.shape_x + x) * GRID_SIZE, (self.shape_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def rotate_shape(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]

    def valid_move(self, offset_x, offset_y):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.shape_x + x + offset_x
                    new_y = self.shape_y + y + offset_y
                    if new_x < 0 or new_x >= self.width or new_y >= self.height or self.board[new_y][new_x]:
                        return False
        return True

    def place_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.shape_y + y][self.shape_x + x] = cell
        self.clear_lines()
        self.current_shape = self.new_shape()
        self.shape_x = self.width // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        if not self.valid_move(0, 0):
            self.game_over = True

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = self.height - len(new_board)
        self.score += lines_cleared ** 2
        new_board = [[0 for _ in range(self.width)] for _ in range(lines_cleared)] + new_board
        self.board = new_board

    def move(self, dx, dy):
        if self.valid_move(dx, dy):
            self.shape_x += dx
            self.shape_y += dy
        elif dy:
            self.place_shape()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Tetris(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    running = True
    while running:
        screen.fill(BLACK)
        game.draw_grid(screen)
        game.draw_shape(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_shape()

        game.move(0, 1)
        clock.tick(10)
        
        if game.game_over:
            print(f"Game Over! Your score: {game.score}")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
