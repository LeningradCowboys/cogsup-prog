from math import sqrt
from expyriment import design, control, stimuli
from expyriment.misc import geometry
control.set_develop_mode()

exp = design.Experiment(name = "Labeled Shapes")
control.initialize(exp)
control.start(subject_id=1)

side = 50.0              
# height of the hexagon
height = side * sqrt(3) / 2
# width of the hexagon
a = side / 2                             

# Triangle
left_shape = stimuli.Shape((-100, 0), (128, 0, 128), vertex_list=geometry.vertices_regular_polygon(3, 50),anti_aliasing=10)

# Hexagon
right_shape = stimuli.Shape((100, 0), (255, 255, 0), vertex_list=geometry.vertices_regular_polygon(6, 25),anti_aliasing=10)

# Vertical lines
top_y = height /2 
line_left  = stimuli.Line((-100, top_y), (-100, top_y + 50), line_width=3, colour='white')
line_right = stimuli.Line(( 100, top_y), ( 100, top_y + 50), line_width=3, colour='white')

# Labels
label_left  = stimuli.TextLine(text="triangle", position=(-100, top_y + 50 + 20), text_colour='white')
label_right = stimuli.TextLine(text="hexagon",  position=( 100, top_y + 50 + 20), text_colour='white')

# Present all stimuli
left_shape.present(clear=True, update=False)
right_shape.present(clear=False, update=False)
line_left.present(clear=False, update=False)
line_right.present(clear=False, update=False)
label_left.present(clear=False, update=False)
label_right.present(clear=False, update=True)

exp.keyboard.wait()
control.end()
