from expyriment import design, control, stimuli

control.set_develop_mode()

# Create an object of class Experiment
exp = design.Experiment(name = "Launching_disrupt_space")
# Initialize the experiment
control.initialize(exp)
# Start running the experiment
control.start(subject_id=1)

square_size = (50, 50)
square_length = 50
# Distance to travel               
displacement_x = 400  
# Set speed
step_size = 10 
# Set up spaces
spatial_gap = 15 # the threshold I found

# Create two squares, left one read, right one green
left_square = stimuli.Rectangle(size=square_size, colour='red', position=(-displacement_x, 0))
right_square = stimuli.Rectangle(size=square_size, colour='green', position=(0, 0))
                                            
# Move left square until collision
while right_square.position[0] - left_square.position[0] >square_length + spatial_gap:  
    left_square.move((step_size, 0))                    
    left_square.present(clear=True, update=False)       
    right_square.present(clear=False, update=True)
    exp.clock.wait(30)

# Move right square after collision
while right_square.position[0] < displacement_x:                
    right_square.move((step_size, 0))                   
    left_square.present(clear=True, update=False)       
    right_square.present(clear=False, update=True)
    exp.clock.wait(30)

# clear screen when done
exp.screen.clear()
exp.screen.update() 

# Wait for a key press and end the experiment
exp.keyboard.wait()
control.end()
