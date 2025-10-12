from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_1, K_2

""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)

MOVE_STEP = 10       
R_STEP    = 5       
MIN_R     = 10
MAX_R     = 200

""" Stimuli """
def make_circle(r, pos=(0,0)):
    c = stimuli.Circle(r, position=pos, anti_aliasing=10)
    c.preload()
    return c

def key_to_label(key):
    mapping = {
        K_LEFT: "left",
        K_RIGHT: "right",
        K_UP: "up",
        K_DOWN: "down",
        K_1: "1",
        K_2: "2",
        K_SPACE: "space",
    }
    return mapping.get(key, str(key))

""" Experiment """
def run_trial(side="L", radius=75):
    if side.upper() == "L":
        fix_pos = [300, 0]
        circle_pos = [-150, 0]
        cover_text = "Cover your LEFT eye."
    else:
        fix_pos = [-300, 0]
        circle_pos = [150, 0]
        cover_text = "Cover your RIGHT eye."

    instructions = stimuli.TextScreen(
        "Blind Spot Task",
        f"{cover_text}\n\n"
        "Fixate on the cross.\n"
        "Use the ARROW KEYS to move the circle.\n"
        "Use 1 and 2 to change its size.\n"
        "1 is smaller, 2 is larger.\n"
        "Press SPACE when the circle disappears (blind spot found)."
    )
    instructions.present()
    exp.keyboard.wait([K_SPACE])

    fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=fix_pos)
    fixation.preload()

    circle = make_circle(radius, pos=circle_pos)

    while True:
        fixation.present(True, False)
        circle.present(False, True)

        key = exp.keyboard.check([K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1, K_2, K_SPACE])
        if key is None:
            continue
        x, y = circle.position

        if key == K_LEFT:
            x -= MOVE_STEP
        elif key == K_RIGHT:
            x += MOVE_STEP
        elif key == K_UP:
            y += MOVE_STEP
        elif key == K_DOWN:
            y -= MOVE_STEP
        elif key == K_1:
            radius = max(MIN_R, radius - R_STEP)
            circle = make_circle(radius, pos=(x, y))
        elif key == K_2:
            radius = min(MAX_R, radius + R_STEP)
            circle = make_circle(radius, pos=(x, y))


        circle.position = (x, y)
        eye = "left" if side.upper() == "L" else "right"
        exp.data.add([eye, key_to_label(key), radius, circle.position[0], circle.position[1]])
        if key == K_SPACE:
            break


exp.add_data_variable_names(["eye", "keypress", "radius", "x_coord", "y_coord"])
control.start(subject_id=1)

intro = stimuli.TextScreen(
    "Blind Spot Task",
    "You will do two trials: LEFT eye, then RIGHT eye.\n\n"
    "Press SPACE to start."
)
intro.present()
exp.keyboard.wait([K_SPACE])

run_trial(side="L")
run_trial(side="R")

control.end()
