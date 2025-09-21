from expyriment import stimuli, design, control
from expyriment.misc import geometry
from math import cos, sin, sqrt, pi, tan

def make_regular_polygon(n, side, position, colour):
    """
    Regular n-gon (side length = side, center = position, color = colour)
    """

    shape = stimuli.Shape(position=position,
                          colour=colour,
                          vertex_list=geometry.vertices_regular_polygon(n, side))

    # Compute top anchor y offset depending on odd/even number of sides
    if n % 2 == 1:  # odd n
        offset = side/2 * (1+cos(pi/n))/(2*sin(pi/n))
    else:           # even n
        offset = side / (2.0 * tan(pi/n))

    # Top anchor coordinate (x = position x, y = position y + offset)
    top_y= position[1] + offset

    return shape, top_y

control.set_develop_mode()  
exp = design.Experiment(name="Labeled Shapes Function")
control.initialize(exp)     # 1) 初始化
control.start(subject_id=1)
# Compute side length and height
side_triangle = 50.0
# 三角形高度 = sqrt(3)/2 * a
height = sqrt(3) / 2 * side_triangle

# hexagon height = triangle height
side_hexagon = height / sqrt(3)

# positions
triangle_pos = (-100, 0)
hexagon_pos  = ( 100, 0)

# Generate shapes
triangle, tri_top_y = make_regular_polygon(3, side_triangle, triangle_pos, (128,0,128))
hexagon,  hex_top_y = make_regular_polygon(6, side_hexagon, hexagon_pos, (255,255,0))


# Vertical lines and labels
line_up_left = stimuli.Line(
    start_point=(triangle_pos[0], tri_top_y),
    end_point=(triangle_pos[0], tri_top_y + 50),
    line_width=3,
    colour=(255,255,255)
)
label_left = stimuli.TextLine(
    "triangle",
    position=(triangle_pos[0], tri_top_y+ 50 + 20),
    text_colour=(255,255,255)
)

line_up_right = stimuli.Line(
    start_point=(hexagon_pos[0], hex_top_y),
    end_point=(hexagon_pos[0], hex_top_y+ 50),
    line_width=3,
    colour=(255,255,255)
)
label_right = stimuli.TextLine(
    "hexagon",
    position=(hexagon_pos[0], hex_top_y + 50 + 20),
    text_colour=(255,255,255) 
)

# Present all stimuli
triangle.present(clear=False, update=False)
hexagon.present(clear=False, update=False)
line_up_left.present(clear=False, update=False)
label_left.present(clear=False, update=False)
line_up_right.present(clear=False, update=False)
label_right.present(clear=False)
exp.keyboard.wait()
control.end()