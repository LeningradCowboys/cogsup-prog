# ternus.py
from expyriment import design, control, stimuli
from expyriment.misc.constants import K_SPACE, C_RED, C_GREEN, C_BLUE, C_YELLOW

# ---------- Global settings ----------
FRAME_MS = 1000.0 / 60.0    # 假定 60Hz，1 帧 ≈ 16.67 ms

def _ms_for_frames(frames: int) -> int:
    return int(round(frames * FRAME_MS))

# ---------- helpers ----------
def present_for(stims, frames=12):
    """
    Present a list of stimuli for a given number of frames,
    compensating for the time taken to draw them.
    """
    # 1) clear back buffer → 2) draw → 3) flip (double-buffering principle)
    exp.screen.clear()
    t0 = exp.clock.time
    for s in stims:
        s.present(clear=False, update=False)
    exp.screen.update()
    draw_dt = exp.clock.time - t0
    target_ms = _ms_for_frames(frames)
    left = max(0, target_ms - draw_dt)
    if left > 0:
        exp.clock.wait(left)

def make_circles(radius, x_positions, colour=(220, 220, 220)):
    """    Create three circles of the same radius at given x positions; y=0 centered."""
    circles = []
    for x in x_positions:
        c = stimuli.Circle(radius=radius, colour=colour, position=(x, 0))
        circles.append(c)
    return circles

def add_tags(circles, tag_colours):
    """
    Add a small colored circle (yellow/red/green, etc.)
    at the "center" of each big circle.
    """
    r = circles[0].radius
    tag_r = max(4, int(r * 0.25)) 

    for big, col in zip(circles, tag_colours):
        small = stimuli.Circle(radius=tag_r, colour=col, position=(0, 0))
        small.plot(big)   
        big.preload()     

# ---------- trial ----------
def run_trial(radius=50, ISI=18, with_tags=False):
    gap = int(radius * 3) 
    slots = [-1.5 * gap, -0.5 * gap, +0.5 * gap, +1.5 * gap]
    A_pos = [int(x) for x in slots[:3]]
    B_pos = [int(x) for x in slots[1:]]

    A = make_circles(radius, A_pos)
    B = make_circles(radius, B_pos)

    if with_tags:
        add_tags(A, [C_YELLOW, C_GREEN, C_BLUE])
        add_tags(B, [C_GREEN, C_BLUE, C_YELLOW])
    else:
        for s in A + B:
            s.preload()

    blank_ms = int(round(ISI * (1000.0/60.0)))

    while True:
        if exp.keyboard.check(K_SPACE):
            break
        present_for(A, frames=12)
        if blank_ms > 0:
            exp.screen.clear(); exp.screen.update()
            exp.clock.wait(blank_ms)
        present_for(B, frames=12)
        if blank_ms > 0:
            exp.screen.clear(); exp.screen.update()
            exp.clock.wait(blank_ms)

# ---------- main ----------
if __name__ == "__main__":
    exp = design.Experiment(name="Ternus illusion")
    control.set_develop_mode()          
    control.initialize(exp)
    control.start(subject_id=1)

    stimuli.TextLine("Ternus: press SPACE to start").present()
    exp.keyboard.wait([K_SPACE])

    stimuli.TextLine("1/3: Element motion (low ISI). Press SPACE.").present()
    exp.keyboard.wait([K_SPACE])
    run_trial(radius=50, ISI=1,  with_tags=False)


    stimuli.TextLine("2/3: Group motion (high ISI). Press SPACE.").present()
    exp.keyboard.wait([K_SPACE])
    run_trial(radius=50, ISI=18, with_tags=False)  


    stimuli.TextLine("3/3: Element motion with color tags. Press SPACE.").present()
    exp.keyboard.wait([K_SPACE])
    run_trial(radius=50, ISI=18, with_tags=True)

    control.end()
