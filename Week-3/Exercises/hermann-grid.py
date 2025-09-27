from expyriment import design, control, stimuli
from expyriment.misc.constants import C_BLACK, C_WHITE

def Hermann_grid(exp, rows, cols, square_size, gap_size, square_colour):
    """
    exp: The active Expyriment experiment object.
    rows: The number of rows in the grid.
    cols: The number of columns in the grid.
    square_size: The side length of each square in pixels.
    gap_size: The space between each square in pixels.
    square_colour: colour of the squares.
    """

    # total width and height of the grid
    total_grid_width = cols * square_size + (cols - 1) * gap_size
    total_grid_height = rows * square_size + (rows - 1) * gap_size

    step = square_size + gap_size

    # center position of the top-left square (row 0, col 0).
    start_x = -total_grid_width / 2.0 + square_size / 2.0
    start_y =  total_grid_height / 2.0 - square_size / 2.0

    positions = []
    for i in range(rows):
        for j in range(cols):
            x = start_x + j * step
            y = start_y - i * step
            positions.append((x, y))

    squares = [stimuli.Rectangle(size=(square_size, square_size),
                                 position=pos,
                                 colour=square_colour)
               for pos in positions]


    canvas = stimuli.BlankScreen(colour=exp.background_colour)
    canvas.present(clear=True, update=False)

    for square in squares:
        square.present(clear=False, update=False)

    exp.screen.update()

N_ROWS = 7
N_COLS = 10
SQUARE_SIZE = 60  
GAP_SIZE = 15     
SQUARE_COLOUR = C_BLACK
BACKGROUND_COLOUR = C_WHITE


control.set_develop_mode(True)
exp = design.Experiment(name="Hermann Grid",
                        background_colour=BACKGROUND_COLOUR)
control.initialize(exp)
control.start(subject_id=1)
Hermann_grid(exp,
                  rows=N_ROWS,
                  cols=N_COLS,
                  square_size=SQUARE_SIZE,
                  gap_size=GAP_SIZE,
                  square_colour=SQUARE_COLOUR)

exp.keyboard.wait()
control.end()

# The illusion is related to ratio of gap size to square size