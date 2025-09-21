from expyriment import design, control, stimuli

control.set_develop_mode()

def launching_event(exp, temporal_gap=0, spatial_gap=0, speed_factor=1):
    """Display one launching event.
    
    Parameters
    ----------
    exp : Experiment object
    temporal_gap : int
        Delay in ms between red stop and green onset (0 = no delay).
    spatial_gap : int
        Distance in px left between red and green at the 'collision' moment.
    speed_factor : float
        Speed of green relative to red (1 = same speed, >1 = faster).
    """
    
    square_size = (50, 50)
    square_length = 50
    displacement_x = 400
    step_size = 10

    # Create two squares
    left_square = stimuli.Rectangle(size=square_size, colour='red', position=(-displacement_x, 0))
    right_square = stimuli.Rectangle(size=square_size, colour='green', position=(0, 0))

    # Move red until "collision"
    while right_square.position[0] - left_square.position[0] > square_length + spatial_gap:
        left_square.move((step_size, 0))
        left_square.present(clear=True, update=False)
        right_square.present(clear=False, update=True)
        exp.clock.wait(30)

    # Temporal gap
    if temporal_gap > 0:
        exp.clock.wait(temporal_gap)

    # Move green square after red stops
    while right_square.position[0] < displacement_x:
        right_square.move((step_size * speed_factor, 0))
        left_square.present(clear=True, update=False)
        right_square.present(clear=False, update=True)
        exp.clock.wait(30)

    # Clear screen for 500 ms before next condition
    exp.screen.clear()
    exp.screen.update()
    exp.clock.wait(500)


# ==== Main program ====
exp = design.Experiment(name="3E: Launching function")
control.initialize(exp)
control.start(subject_id=1)

# 1) Michottean launching
launching_event(exp, temporal_gap=0, spatial_gap=0, speed_factor=1)

# # 2) Launching with temporal gap
launching_event(exp, temporal_gap=50, spatial_gap=0, speed_factor=1)

# # 3) Launching with spatial gap
launching_event(exp, temporal_gap=0, spatial_gap=50, speed_factor=1)

# # 4) Triggering (green moves faster)
launching_event(exp, temporal_gap=0, spatial_gap=0, speed_factor=3)

# End
exp.keyboard.wait()
control.end()
