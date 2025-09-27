from expyriment import design, control, stimuli
from expyriment.misc.constants import C_GREY, C_BLACK, C_WHITE

control.set_develop_mode()
exp = design.Experiment(name="Kanizsa rectangle", background_colour=C_GREY)
control.initialize(exp)

width, height = exp.screen.size

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

def Kanizsa_rectangle(aspect_ratio=1.0, rect_scale=1.0, circle_scale=1.0):
    """
    aspect_ratio:  width / height of the rectangle
    rect_scale:    scale of the rectangle
    circle_scale:  scale of the circles
    """
    # calculate rectangle width and height
    base_h = (width * 0.25) * rect_scale
    rect_h = int(base_h)
    rect_w = int(base_h * aspect_ratio)

    half_w, half_h = rect_w // 2, rect_h // 2

    # centers of the four circles
    centers = [(-half_w,  half_h),   # 左上
               ( half_w,  half_h),   # 右上
               (-half_w, -half_h),   # 左下
               ( half_w, -half_h)]   # 右下

    colors = [C_BLACK, C_BLACK, C_WHITE, C_WHITE]

    # radius of the circles
    base_r = (width / 20.0) * circle_scale
    r = int(max(2, base_r))

    canvas = stimuli.BlankScreen(colour=exp.background_colour)
    canvas.present(clear=True, update=False)

    for (c, col) in zip(centers, colors):
        circle, rec = Kanizsa_square(c, col, r, exp.background_colour)
        circle.present(clear=False, update=False)
        rec.present(clear=False, update=False)

    exp.screen.update()


control.start(subject_id=1)

Kanizsa_rectangle(aspect_ratio=2, rect_scale=1, circle_scale=1)

exp.keyboard.wait()
control.end()

# I think if the circle is getting smaller then the illusion is getting weaker.
# If the aspect_ratio is too large or too small then the illusion is getting weaker or the circles even overlap.
# If the rectangle is getting larger (rectangle scale larger) then the illusion is getting weaker.