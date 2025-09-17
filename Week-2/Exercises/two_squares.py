from expyriment import design, control, stimuli
control.set_develop_mode()

exp = design.Experiment("Two Squares")
control.initialize(exp)
control.start()

square_size = (50, 50)
left_square = stimuli.Rectangle(size=square_size, colour='red', position=(-100, 0))
right_square = stimuli.Rectangle(size=square_size, colour='green', position=(100, 0))
left_square.present(clear=True, update=False)
right_square.present(clear=False, update=True)  

exp.keyboard.wait()
control.end()