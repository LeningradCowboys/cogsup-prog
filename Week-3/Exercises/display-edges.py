from expyriment import stimuli, control,design
control.set_develop_mode(True)
exp = design.Experiment("display-edges")
control.initialize(exp)
control.start()

width, height = exp.screen.size
side = width * 0.05
x = width/2 - side/2
y = height/2 - side/2
rectangle1 = stimuli.Rectangle(size=(side, side), line_width = 1, colour=(255,0,0),position=(x,y))
rectangle2 = stimuli.Rectangle(size=(side, side), line_width = 1, colour=(255,0,0),position=(x,-y))
rectangle3 = stimuli.Rectangle(size=(side, side), line_width = 1, colour=(255,0,0),position=(-x,y))
rectangle4 = stimuli.Rectangle(size=(side, side), line_width = 1, colour=(255,0,0),position=(-x,-y))
rectangle1.present(clear=False, update = False)
rectangle2.present(clear=False, update = False)
rectangle3.present(clear=False, update = False)
rectangle4.present(clear=False, update = True)
exp.keyboard.wait()
control.end()