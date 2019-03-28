import pygame  # Game library to draw onto the window
from pygame.locals import USEREVENT  # Import some local pygame variables
from random import randrange  # For a little randomness in the tetrominos
import sys  # For exiting the program


class TetraminoShape:
    """Encapsulate a shape of tetramino, this includes the rotating and initial
    randomization
    """

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

    def __init__(self, shape, tetris):
        """Construct a TetraminoShape object

        Args:
            shape (str): The shape (chosen from the static shapes)
            tetris (Tetris): Reference to the Tetris objecct
        """

        # Initialize variables
        self.shape_keyword = shape
        self.shape = TetraminoShape.SHAPES[shape][0]
        self.color = TetraminoShape.SHAPES[shape][1]
        self.tetris = tetris
        self.rotated = 1

    def rotate(self):
        """Rotate the tetramino if the space it will occupy is not occupied or
        off of the screen
        """

        # One case for each shape in each rotated position

        # LINE IN UPRIGHT POSITION
        if (self.shape_keyword == TetraminoShape.LINE
                and self.rotated % 2 == 1 and tetris.valid_position(
                    self.shape[0][0] - 2, self.shape[0][1] - 2)
                and tetris.valid_position(self.shape[1][0] - 1,
                                          self.shape[1][1] - 1)
                and tetris.valid_position(self.shape[3][0] + 1,
                                          self.shape[3][1] + 1)):
            #
            self.shape[0] = [self.shape[0][0] - 2, self.shape[0][1] - 2]
            self.shape[1] = [self.shape[1][0] - 1, self.shape[1][1] - 1]
            # self.shape[2] = [self.shape[2][0] + 1, self.shape[3][1] - 1]
            self.shape[3] = [self.shape[3][0] + 1, self.shape[3][1] + 1]
            self.rotated += 1

        # LINE IN HORIZONTAL POSITION
        elif (self.shape_keyword == TetraminoShape.LINE
              and self.rotated % 2 == 0 and tetris.valid_position(
                  self.shape[0][0] + 2, self.shape[0][1] + 2) and
              tetris.valid_position(self.shape[0][0] + 1, self.shape[0][1] + 1)
              and tetris.valid_position(self.shape[0][0] - 1,
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


class Tetramino:
    def __init__(self, shape, screen, tetris):
        """Construct a Tetamino at a random position above the view of the
         board

        Args:
            shape (Tuple[List[List[int, int]], Tuple[int, int, int]]):
                The shape and color of the tetramino
            screen (pygame.Screen): Screen to draw on
        """
        self.tetris = tetris
        self.shape = TetraminoShape(shape, tetris)
        self.shape.randomize_horizontal_position()
        self.screen = screen

    def draw(self):
        for i, square in enumerate(self.shape.shape):
            pygame.draw.rect(
                self.screen, (75 * i, 150, 150),
                (self.tetris.col_w * square[0], self.tetris.row_h * square[1],
                 self.tetris.col_w, self.tetris.row_h))

    def debug(self):
        print("--------------------")

    def rotate(self):
        self.shape.rotate()

    def update(self):
        for shape in self.shape.shape:
            if not self.tetris.valid_position(shape[0], shape[1] + 1):
                return False

        self.shape.shape = [[x[0], x[1] + 1] for x in self.shape.shape]
        return True

    def move(self, x=0, y=0):
        self.shape.shape = [[rect[0] + x, rect[1] + y]
                            for rect in self.shape.shape]


class Tetris:
    COLS = 10
    ROWS = 20

    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.col_w = self.w / self.COLS
        self.row_h = self.h / self.ROWS
        self.current_tetramino = None
        self.tetraminos = [Tetramino(TetraminoShape.LINE, screen, self)]
        self.curr_tetramino = self.tetraminos[-1]

    def valid_position(self, x, y):
        if x < 0 or x >= Tetris.COLS or y >= Tetris.ROWS:
            return False
        return True

    def draw(self):
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
        if not self.curr_tetramino.update():
            self.tetraminos.append(
                Tetramino(TetraminoShape.LINE, screen, self))
            self.curr_tetramino = self.tetraminos[-1]


pygame.init()
screen = pygame.display.set_mode((80 * 10, 80 * 20))
TETRIS_DROP = USEREVENT + 1
pygame.time.set_timer(TETRIS_DROP, 250)

done = False
tetris = Tetris(screen)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == TETRIS_DROP:
            tetris.update()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                tetris.curr_tetramino.move(y=1)
            if event.key == pygame.K_LEFT:
                tetris.curr_tetramino.move(x=-1)
            if event.key == pygame.K_RIGHT:
                tetris.curr_tetramino.move(x=1)
            if event.key == pygame.K_UP:
                tetris.curr_tetramino.rotate()
            if event.key == pygame.K_d:
                tetris.curr_tetramino.debug()

    screen.fill((0, 0, 0))
    tetris.draw()

    pygame.display.flip()
