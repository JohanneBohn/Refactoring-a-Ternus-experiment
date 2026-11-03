import random
import expyriment as xpy



# Experimental variables
EXPERIMENT_NAME = "Ternus experiment"

# Visuals
BACKGROUND = (0, 0, 0)
FOREGROUND = (255, 255, 255)

CROSS_SIZE = (20, 20)
CROSS_WIDTH = 4

CANVAS_SIZE = (600, 300)
DOT_RADIUS = 20
RECTANGLE_SIZE = (35, 35)
POLYGON_SHAPE = xpy.misc.geometry.vertices_regular_polygon(3, 54)

POSITION_A = (-120, -50)
POSITION_B = (-40, -50)
POSITION_C = (40, -50)
POSITION_D = (120, -50)

# Experimental design
ISI_VALUES = [0, 50, 500, 1000]
TRIALS_PER_ISI = 1
N_REPETITIONS = 1

# Timings
FIXATION_DURATION = 200
FRAME_DURATION = 250
ITI = 500

# Responses & response keys
KEYS = [xpy.misc.constants.K_LEFT, xpy.misc.constants.K_RIGHT]
LEFT_RESPONSE = "element"
RIGHT_RESPONSE = "group"



# Experiment initialization
exp = xpy.design.Experiment(name=EXPERIMENT_NAME, background_colour=BACKGROUND, foreground_colour=FOREGROUND)
exp.data_variable_names = ["condition", "trial", "isi_ms", "frame_ms", "response", "group_response", "key", "rt_ms"]
xpy.control.initialize(exp)

# DOTS stimuli
dots_frame_1 = xpy.stimuli.Canvas(size=CANVAS_SIZE, colour=BACKGROUND)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_A, colour=FOREGROUND).plot(dots_frame_1)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_B, colour=FOREGROUND).plot(dots_frame_1)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_C, colour=FOREGROUND).plot(dots_frame_1)

dots_frame_2 = xpy.stimuli.Canvas(size=CANVAS_SIZE, colour=BACKGROUND)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_B, colour=FOREGROUND).plot(dots_frame_2)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_C, colour=FOREGROUND).plot(dots_frame_2)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_D, colour=FOREGROUND).plot(dots_frame_2)

# SHAPES stimuli
shapes_frame_1 = xpy.stimuli.Canvas(size=CANVAS_SIZE, colour=BACKGROUND)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_A, colour=FOREGROUND).plot(shapes_frame_1)
xpy.stimuli.Shape(vertex_list=POLYGON_SHAPE, position=POSITION_B, colour=FOREGROUND).plot(shapes_frame_1)
xpy.stimuli.Rectangle(size=RECTANGLE_SIZE, position=POSITION_C, colour=FOREGROUND).plot(shapes_frame_1)

shapes_frame_2 = xpy.stimuli.Canvas(size=CANVAS_SIZE, colour=BACKGROUND)
xpy.stimuli.Shape(vertex_list=POLYGON_SHAPE, position=POSITION_B, colour=FOREGROUND).plot(shapes_frame_2)
xpy.stimuli.Rectangle(size=RECTANGLE_SIZE, position=POSITION_C, colour=FOREGROUND).plot(shapes_frame_2)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_D, colour=FOREGROUND).plot(shapes_frame_2)

# Fixation cross and text screens
fixation_cross = xpy.stimuli.FixCross(size=CROSS_SIZE, line_width=CROSS_WIDTH, colour=FOREGROUND)
fixation_screen = xpy.stimuli.BlankScreen(colour=BACKGROUND)
fixation_cross.plot(fixation_screen)
instruction_screen = xpy.stimuli.TextScreen(heading=EXPERIMENT_NAME, text="Keep your eyes on the central cross.\n\nLEFT = element motion\nRIGHT = group motion\n\nPress SPACE to start.")
response_screen = xpy.stimuli.TextScreen(heading="What did you see?", text="LEFT = element motion\nRIGHT = group motion")
blank_screen = xpy.stimuli.BlankScreen(colour=BACKGROUND)

# Fixation on stimulus and text screens
fixation_cross.plot(dots_frame_1)
fixation_cross.plot(dots_frame_2)
fixation_cross.plot(shapes_frame_1)
fixation_cross.plot(shapes_frame_2)
fixation_cross.plot(instruction_screen)
fixation_cross.plot(response_screen)

# Preloading

for frame in [dots_frame_1, dots_frame_2, shapes_frame_1, shapes_frame_2, instruction_screen, response_screen, blank_screen]:
    frame.preload()


def create_block(condition):
    """
    Creates the DOTS and SHAPES blocks.
    """
    block = xpy.design.Block(name = condition)
    block.set_factor("condition", condition)
    for isi in ISI_VALUES:
        for _ in range(TRIALS_PER_ISI):
            trial = xpy.design.Trial()
            trial.set_factor("isi_ms", isi)
            block.add_trial(trial)
    block.shuffle_trials()
    return block

dots_block = create_block("DOTS")
shapes_block = create_block("SHAPES")


def add_stimuli(block, frame_1, frame_2):
    """
    Adds stimuli to blocks.
    """
    for trial in block.trials:
        for frame in [frame_1, frame_2, fixation_screen, response_screen, fixation_screen, blank_screen]:
            trial.add_stimulus(frame)

add_stimuli(dots_block, dots_frame_1, dots_frame_2)
add_stimuli(shapes_block, shapes_frame_1, shapes_frame_2)


# Experiment start
exp.add_block(dots_block)
exp.add_block(shapes_block)
xpy.control.start(skip_ready_screen=True)

# Instructions
instruction_screen.present()
exp.keyboard.wait(keys=[xpy.misc.constants.K_SPACE])

# Trial presentation
for block in exp.blocks:
    for trial in block.trials:
        isi = trial.get_factor("isi_ms")
        trial.stimuli[2].present()
        exp.clock.wait(FIXATION_DURATION)

        for i in range(N_REPETITIONS):
            for i in [0,1]:
                trial.stimuli[i].present()
                exp.clock.wait(FRAME_DURATION)
                if isi > 0:
                    trial.stimuli[4].present()
                    exp.clock.wait(isi)

        # Response collection
        trial.stimuli[3].present()
        key, reaction_time = exp.keyboard.wait(keys=KEYS)

        if key == KEYS[0]:
            motion = LEFT_RESPONSE
            group_response = 0
        else:
            motion = RIGHT_RESPONSE
            group_response = 1

        # Intertrial interval
        trial.stimuli[5].present()
        exp.clock.wait(ITI)
        # Data saving
        exp.data.add([block.get_factor("condition"), trial.id, isi, FRAME_DURATION, motion, group_response, key, reaction_time])
        exp.data.save()

# Experiment end
xpy.control.end()