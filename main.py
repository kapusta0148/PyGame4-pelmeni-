import pygame
import numpy as np
import sys


WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

class TorusGrid:
    def __init__(self):
        self.grid = np.zeros((ROWS, COLS), dtype=int)

    def count_neighbors(self, x, y):
        return sum([
            self.grid[(x-1) % ROWS][(y-1) % COLS],
            self.grid[(x-1) % ROWS][y],
            self.grid[(x-1) % ROWS][(y+1) % COLS],
            self.grid[x][(y-1) % COLS],
            self.grid[x][(y+1) % COLS],
            self.grid[(x+1) % ROWS][(y-1) % COLS],
            self.grid[(x+1) % ROWS][y],
            self.grid[(x+1) % ROWS][(y+1) % COLS]
        ])

    def update(self):
        new_grid = self.grid.copy()
        for i in range(ROWS):
            for j in range(COLS):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    new_grid[i][j] = 1 if 2 <= neighbors <= 3 else 0
                else:
                    new_grid[i][j] = 1 if neighbors == 3 else 0
        self.grid = new_grid

    def randomize(self):
        total_cells = ROWS * COLS
        cells_to_fill = int(total_cells * 0.2)
        self.grid = np.zeros((ROWS, COLS), dtype=int)
        indices = np.random.choice(total_cells, cells_to_fill, replace=False)
        for idx in indices:
            i, j = divmod(idx, COLS)
            self.grid[i][j] = 1

    def clear(self):
        self.grid = np.zeros((ROWS, COLS), dtype=int)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    grid = TorusGrid()
    running = False
    music_playing = False
    speed = 10
    music_position = 0
    pygame.display.set_caption("Life of Kvadratics")
    pygame.mixer.music.load('End_song.mp3')
    pygame.mixer.music.set_volume(0.5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    if music_playing:
                        music_position = pygame.mixer.music.get_pos() / 1000
                        pygame.mixer.music.pause()
                        music_playing = False
                    else:
                        pygame.mixer.music.play(-1, music_position)
                        music_playing = True
                elif event.key == pygame.K_r:
                    grid.randomize()
                elif event.key == pygame.K_c:
                    grid.clear()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    i, j = y // CELL_SIZE, x // CELL_SIZE
                    grid.grid[i][j] = 1 - grid.grid[i][j]
                elif event.button == 4:
                    speed = min(60, speed + 1)
                elif event.button == 5:
                    speed = max(1, speed - 1)

        screen.fill(WHITE)

        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        for i in range(ROWS):
            for j in range(COLS):
                if grid.grid[i][j] == 1:
                    pygame.draw.rect(screen, BLACK,
                                   (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

        if running:
            grid.update()

        font = pygame.font.SysFont("Arial", 18)
        speed_text = font.render(f"Speed: {speed} FPS", True, RED)
        music_text = font.render("Music: " + ("ON" if music_playing else "OFF"), True, RED)
        screen.blit(speed_text, (10, 10))
        screen.blit(music_text, (10, 30))

        pygame.display.flip()
        clock.tick(speed)

if __name__ == "__main__":
    main()
    """Control:
        Space - play/stop game
        mouse wheel - speed up/speed down
        Left Button Mouse - create kvadratik/kill kvadratik
        R - Create 20% of Kvadratiks randomno
        C - Kill all Kvadratiki :(
        Shift - turn on the most powerful song about life"""
