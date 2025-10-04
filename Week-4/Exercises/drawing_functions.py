from expyriment import design, control, stimuli
import random

def load(stims):
    """Preload all stimuli in the iterable."""
    for stim in stims:
        stim.preload()

def timed_draw(stims):
    t0 = exp.clock.time
    exp.screen.clear()
    for stim in stims:
        if not stim.is_preloaded:
            stim.preload()
        stim.present(clear=False, update=False)

    exp.screen.update()
    
    t1 = exp.clock.time
    return t1 - t0

def present_for(stims, t=1000):
    """Present stimuli for t milliseconds, accounting for drawing time."""  
    draw_time = timed_draw(stims)     
    remain = t - draw_time
    if remain > 0:
        exp.clock.wait(remain)

""" Test functions """
exp = design.Experiment()

control.set_develop_mode()
control.initialize(exp)

fixation = stimuli.FixCross()
load([fixation])

n = 20
positions = [(random.randint(-300, 300), random.randint(-300, 300)) for _ in range(n)]
squares = [stimuli.Rectangle(size=(50, 50), position = pos) for pos in positions]
load(squares)

durations = []

t0 = exp.clock.time
for square in squares:
    if not square.is_preloaded:
        print("Preloading function not implemneted correctly.")
    stims = [fixation, square] 
    present_for(stims, 500)
    t1 = exp.clock.time
    durations.append(t1-t0)
    t0 = t1

print(durations)

control.end()