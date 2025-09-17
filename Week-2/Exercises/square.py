# Import the main modules of expyriment
from expyriment import design, control, stimuli

control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Square")
#在蓝色正方形（边长50）内部显示一个注视十字半秒钟，
# 随后移除注视十字，仅保留蓝色正方形（边长50）直至按下任意键。

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp) # Set the background color to blue

# Create a fixation cross (color, size, and position will take on default values)
fixation = stimuli.FixCross() # At this stage the fixation cross is not yet rendered

# Create a 50px-radius square
square = stimuli.Rectangle(size=(50, 50), colour='blue')

# Start running the experiment
control.start(subject_id=1)


# present the blue rectangle
square.present(clear=True, update=True)

# Present the fixation cross
fixation.present(clear=False, update=True)

# Leave it on-screen for 1,000 ms
exp.clock.wait(500)

square.present(clear=True, update=True)

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()