from expyriment import design, control, stimuli

exp = design.Experiment(name="Square")

control.set_develop_mode()
control.initialize(exp)

fixation = stimuli.FixCross()
square = stimuli.Rectangle(size=(100, 100), line_width=5)

def draw(stims):
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()


control.start(subject_id=1)

draw([fixation])
exp.clock.wait(500)

draw([fixation, square])
exp.keyboard.wait()

control.end()
