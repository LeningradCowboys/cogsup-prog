from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK
import random
import itertools

""" Constants """
# Participants press the first letter of the color name: r/b/g/o
KEYS = list(map(ord, ["r", "b", "g", "o"]))  # minimal change: reuse KEYS name

TRIAL_TYPES = ["match", "mismatch"]
COLORS = ["red", "blue", "green", "orange"]

# Extended to 8 blocks × 16 trials = 128 trials total
N_BLOCKS = 8
N_TRIALS_IN_BLOCK = 16  # full 4×4 factorial per block

INSTR_START = """
In this task, you must indicate the COLOR of the word on screen (ignore its meaning).
Press R for red, B for blue, G for green, O for orange.\n
Press SPACE to continue.
"""
INSTR_MID = """You have finished another block, well done! Your task stays the same.\nTake a short break, then press SPACE to continue."""
INSTR_END = """Well done!\nPress SPACE to quit the experiment."""

FEEDBACK_CORRECT = """Correct"""
FEEDBACK_INCORRECT = """Incorrect"""

""" Helper functions """
def load(stims):
    for stim in stims:
        stim.preload()

def timed_draw(*stims):
    t0 = exp.clock.time
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()
    t1 = exp.clock.time
    return t1 - t0

def present_for(*stims, t=1000):
    dt = timed_draw(*stims)
    if t - dt > 0:
        exp.clock.wait(t - dt)

def present_instructions(text):
    instructions = stimuli.TextScreen(text=text, text_justification=0, heading="Instructions")
    instructions.present()
    exp.keyboard.wait()

""" Global settings """
exp = design.Experiment(name="Stroop", background_colour=C_WHITE, foreground_colour=C_BLACK)
exp.add_data_variable_names(['block_cnt', 'trial_cnt', 'trial_type', 'word', 'color', 'RT', 'correct'])

control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
fixation = stimuli.FixCross()
fixation.preload()

stims = {w: {c: stimuli.TextLine(w, text_colour=c) for c in COLORS} for w in COLORS}
load([stims[w][c] for w in COLORS for c in COLORS])

feedback_correct = stimuli.TextLine(FEEDBACK_CORRECT)
feedback_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT)
load([feedback_correct, feedback_incorrect])

""" Trial runner """
def run_trial(block_id, trial_id, trial_type, word, color):
    # Show fixation
    present_for(fixation, t=500)

    # Present the stimulus and wait for a color key (r/b/g/o)
    stim = stims[word][color]
    stim.present()
    key, rt = exp.keyboard.wait(KEYS)

    # Correct key is the first letter of the ink color
    correct_key = ord(color[0])
    correct = (key == correct_key)

    # Store trial data
    exp.data.add([block_id, trial_id, trial_type, word, color, rt, correct])

    # Feedback (text-only to avoid color priming)
    present_for(feedback_correct if correct else feedback_incorrect, t=1000)

""" Build balanced blocks: full 4×4 factorial per block, shuffled """
# Base factorial (16 combinations): one of each word×color combination
base = [(w, c) for w in COLORS for c in COLORS]  # 4×4 = 16
assert len(base) == N_TRIALS_IN_BLOCK, "Block size must equal the 4×4 factorial (16)."

# Start experiment
control.start(subject_id=1)

present_instructions(INSTR_START)

for block_id in range(1, N_BLOCKS + 1):
    # Copy and shuffle the 16 factorial trials for this block
    b_trials = base[:]
    random.shuffle(b_trials)

    for trial_id, (word, color) in enumerate(b_trials, 1):
        # Keep trial_type column for downstream analyses
        trial_type = "match" if word == color else "mismatch"
        run_trial(block_id, trial_id, trial_type, word, color)

    if block_id != N_BLOCKS:
        present_instructions(INSTR_MID)

present_instructions(INSTR_END)
control.end()
