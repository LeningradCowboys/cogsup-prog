from expyriment import design, control, stimuli, io
from expyriment.misc.constants import C_GREY, C_BLACK, C_WHITE

control.set_develop_mode() 
exp = design.Experiment(name="Kanizsa square", background_colour=C_GREY)
control.initialize(exp)

# get screen size
width, height = exp.screen.size
length = width // 4        
radius = width // 20       

# get centers of four circles
centers = [(-length // 2,  length // 2),   # 左上
           ( length // 2,  length // 2),   # 右上
           (-length // 2, -length // 2),   # 左下
           ( length // 2, -length // 2)]   # 右下

colors = [C_BLACK, C_BLACK, C_WHITE, C_WHITE]

def Kanizsa_square(center, colour, r, bg_colour):
    """
    drawing a circle and then covering
    one quadrant with a rectangle of the background color.
    """
    cx, cy = center

    # main circle
    circle = stimuli.Circle(radius=r, colour=colour, anti_aliasing=10)
    circle.reposition(center)

    # determine the sign of x and y to make sure
    # the 'mouth' faces the screen center
    sgn_x = 1 if 0 - cx > 0 else -1 if 0 - cx < 0 else 0
    sgn_y = 1 if 0 - cy > 0 else -1 if 0 - cy < 0 else 0

    # rectangle with the background color to create the 'mouth'
    rec = stimuli.Rectangle(size=(r, r), colour=bg_colour)
    rec.reposition((cx + sgn_x * r / 2.0, cy + sgn_y * r / 2.0))

    return circle, rec

control.start(subject_id=1)
canvas = stimuli.BlankScreen(colour=exp.background_colour)
canvas.present(clear=True, update=False)

for (c, col) in zip(centers, colors):
    circle, rec = Kanizsa_square(c, col, radius, exp.background_colour)
    circle.present(clear=False, update=False)
    rec.present(clear=False, update=False)

exp.screen.update()
exp.keyboard.wait()
control.end()
