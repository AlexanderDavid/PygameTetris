import pygame  # Game library to draw onto the window
from pygame.locals import USEREVENT  # Import some local pygame variables
from random import randrange  # For a little randomness in the tetrominos
import sys  # For exiting the program


class Tetramino:

    # Static variables for the tetramino type
    LINE = "LINE"
    T = "T"
    L = "L"
    BLOCK = "BLOCK"

    # Static dictionary that contains the tetramino shapes and colors
    SHAPES = {
        "LINE": ([[0, -1], [0, -2], [0, -3], [0, -4]], (255, 0, 0)),
        "T": ([[0, -1], [1, -1], [2, -1], [1, -2]], (0, 255, 0)),
        "L": ([[0, -1], [0, -2], [0, -3], [1, -1]], (255, 0, 0)),
        "BLOCK": ([[0, -1], [0, -2], [-1, -1], [-1, -2], (255, 255, 0)])
    }

    def __init__(self, shape, screen, tetris):
        """Construct a Tetamino at a random position above the view of the
         board

        Args:
            shape (Tuple[List[List[int, int]], Tuple[int, int, int]]):
                The shape and color of the tetramino
            screen (pygame.Screen): Screen to draw on
        """
        self.tetris = tetris
        self.screen = screen
        self.shape_keyword = shape
        self.shape = self.SHAPES[shape][0]
        self.color = self.SHAPES[shape][1]
        self.randomize_horizontal_position()
        self.tetris = tetris
        self.rotated = 1

    def rotate(self):
        """Rotate the tetramino if the space it will occupy is not occupied or
        off of the screen
        """

        # One case for each shape in each rotated position

        # LINE IN UPRIGHT POSITION
        if (self.shape_keyword == self.LINE
                and self.rotated % 2 == 1 and self.tetris.is_valid_position(
                    self.shape[0][0] - 2, self.shape[0][1] - 2)
                and self.tetris.is_valid_position(self.shape[1][0] - 1,
                                                  self.shape[1][1] - 1)
                and self.tetris.is_valid_position(self.shape[3][0] + 1,
                                                  self.shape[3][1] + 1)):
            #
            self.shape[0] = [self.shape[0][0] - 2, self.shape[0][1] - 2]
            self.shape[1] = [self.shape[1][0] - 1, self.shape[1][1] - 1]
            # self.shape[2] = [self.shape[2][0] + 1, self.shape[3][1] - 1]
            self.shape[3] = [self.shape[3][0] + 1, self.shape[3][1] + 1]
            self.rotated += 1

        # LINE IN HORIZONTAL POSITION
        elif (self.shape_keyword == self.LINE
              and self.rotated % 2 == 0 and self.tetris.is_valid_position(
                  self.shape[0][0] + 2, self.shape[0][1] + 2)
              and self.tetris.is_valid_position(self.shape[0][0] + 1,
                                                self.shape[0][1] + 1)
              and self.tetris.is_valid_position(self.shape[0][0] - 1,
                                                self.shape[0][1] - 1)):
            self.shape[0] = [self.shape[0][0] + 2, self.shape[0][1] + 2]
            self.shape[1] = [self.shape[1][0] + 1, self.shape[1][1] + 1]
            # self.shape[2] = [self.shape[2][0] + 1, self.shape[3][1] - 1]
            self.shape[3] = [self.shape[3][0] - 1, self.shape[3][1] - 1]
            self.rotated += 1

    def randomize_horizontal_position(self):
        width = self.get_tetromino_width()
        offset = randrange(Tetris.COLS - width)
        self.shape = [[x[0] + offset, x[1]] for x in self.shape]

    def get_tetromino_width(self):
        return (lambda arr: max(arr) - min(arr))([x[0] for x in self.shape])

    def draw(self):
        for i, square in enumerate(self.shape):
            pygame.draw.rect(
                self.screen, (75 * i, 150, 150),
                (self.tetris.col_w * square[0], self.tetris.row_h * square[1],
                 self.tetris.col_w, self.tetris.row_h))

    def debug(self):
        print("--------------------")

    def update(self):
        for shape in self.shape:
            return False

        self.shape = [[x[0], x[1] + 1] for x in self.shape]
        return True

    def move(self, x=0, y=0):
        for shape in self.shape:
            if not self.tetris.is_valid_position(shape[0] + x, shape[1] + y):
                return False

        self.shape = [[rect[0] + x, rect[1] + y] for rect in self.shape]
        return True


class Tetris:
    # Columns and rows that the board has
    COLS = 10
    ROWS = 20

    def __init__(self, screen):
        """Construct a Tetris board object

        Args:
            screen (Pygame.Screen): Surface to draw on
        """
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.col_w = self.w / self.COLS
        self.row_h = self.h / self.ROWS
        self.current_tetramino = None
        self.tetraminos = [Tetramino(Tetramino.LINE, screen, self)]
        self.curr_tetramino = self.tetraminos[-1]

    def is_valid_position(self, x, y):
        """Check if a position is either at the
        bottom of the screen or on top of a tetramino that has already
        fallen

        Args:
            x (int): X position on the grid
            y (int): Y position on the grid

        Returns:
            bool: If the X Y position is the valid
        """
        if y >= Tetris.ROWS or x < 0 or x >= Tetris.COLS:
            return False

        return True

    def draw(self):
        """Draw all of the tetraminos and the grid
        """
        for tetramino in self.tetraminos:
            tetramino.draw()

        for i in range(0, self.COLS + 1):
            pygame.draw.lines(self.screen, (255, 255, 255),
                              False, [(self.col_w * i, 0),
                                      (self.col_w * i, self.h)], 5)

        for i in range(0, self.ROWS + 1):
            pygame.draw.lines(self.screen, (255, 255, 255),
                              False, [(0, self.row_h * i),
                                      (self.w, self.row_h * i), 5])

    def update(self):
        """Update the current tetraminos position and check if there
        is a filled line that needs to go away
        """
        self.curr_tetramino.move(y=1)

    def key_down(self, key):
        # Pressing the down key should move the tetramino down
        if key == pygame.K_DOWN:
            self.curr_tetramino.move(y=1)

        # Pressing the left key should move the tetramino left
        elif key == pygame.K_LEFT:
            self.curr_tetramino.move(x=-1)

        # Pressing the right key should move the tetramino right
        elif key == pygame.K_RIGHT:
            self.curr_tetramino.move(x=1)

        # Pressing the up key should rotate the tetramino
        elif key == pygame.K_UP:
            self.curr_tetramino.rotate()

        # Call the debug function on the current falling tetramino
        # If the d button is pressed
        elif key == pygame.K_d:
            self.curr_tetramino.debug()


def main():
    """Main game loop and initialization
    """

    # Initialize the game and local variables
    pygame.init()
    screen = pygame.display.set_mode((80 * 10, 80 * 20))
    TETRIS_DROP = USEREVENT + 1
    done = False
    tetris = Tetris(screen)

    # Set the timer going for forced drop
    pygame.time.set_timer(TETRIS_DROP, 400)

    # Infinite loop while the game is running
    while not done:
        # Get the events that have happened since last loop
        for event in pygame.event.get():
            # If the exit button was pressed then end the loop
            if event.type == pygame.QUIT:
                done = True

            # If the tetris drop timer fired update the game
            elif event.type == TETRIS_DROP:
                tetris.update()

            # If the event was a keydown send the key to the tetris object
            elif event.type == pygame.KEYDOWN:
                tetris.key_down(event.key)

        # Refresh the screen
        screen.fill((0, 0, 0))
        # Draw the new board
        tetris.draw()

        # Flip the buffer
        pygame.display.flip()


# Run the main game loop
if __name__ == '__main__':
    main()
