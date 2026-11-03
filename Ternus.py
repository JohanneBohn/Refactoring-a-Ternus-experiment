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
TRIALS_PER_ISI = 5
N_REPETITIONS = 3

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
screen1 = xpy.stimuli.Canvas(size=CANVAS_SIZE, colour=BACKGROUND)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_A, colour=FOREGROUND).plot(screen1)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_B, colour=FOREGROUND).plot(screen1)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_C, colour=FOREGROUND).plot(screen1)

screen2 = xpy.stimuli.Canvas(size=CANVAS_SIZE, colour=BACKGROUND)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_B, colour=FOREGROUND).plot(screen2)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_C, colour=FOREGROUND).plot(screen2)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_D, colour=FOREGROUND).plot(screen2)

# SHAPES stimuli
screen3 = xpy.stimuli.Canvas(size=CANVAS_SIZE, colour=BACKGROUND)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_A, colour=FOREGROUND).plot(screen3)
xpy.stimuli.Shape(vertex_list=POLYGON_SHAPE, position=POSITION_B, colour=FOREGROUND).plot(screen3)
xpy.stimuli.Rectangle(size=RECTANGLE_SIZE, position=POSITION_C, colour=FOREGROUND).plot(screen3)

screen4 = xpy.stimuli.Canvas(size=CANVAS_SIZE, colour=BACKGROUND)
xpy.stimuli.Shape(vertex_list=POLYGON_SHAPE, position=POSITION_B, colour=FOREGROUND).plot(screen4)
xpy.stimuli.Rectangle(size=RECTANGLE_SIZE, position=POSITION_C, colour=FOREGROUND).plot(screen4)
xpy.stimuli.Circle(radius=DOT_RADIUS, position=POSITION_D, colour=FOREGROUND).plot(screen4)

# Fixation cross and text screens
thing1 = xpy.stimuli.FixCross(size=CROSS_SIZE, line_width=CROSS_WIDTH, colour=FOREGROUND)
screen5 = xpy.stimuli.BlankScreen(colour=BACKGROUND)
thing1.plot(screen5)
text1 = xpy.stimuli.TextScreen(heading=EXPERIMENT_NAME, text="Keep your eyes on the central cross.\n\nLEFT = element motion\nRIGHT = group motion\n\nPress SPACE to start.")
text2 = xpy.stimuli.TextScreen(heading="What did you see?", text="LEFT = element motion\nRIGHT = group motion")
screen6 = xpy.stimuli.BlankScreen(colour=BACKGROUND)

# Fixation on stimulus and text screens
thing1.plot(screen1)
thing1.plot(screen2)
thing1.plot(screen3)
thing1.plot(screen4)
thing1.plot(text1)
thing1.plot(text2)

# Preloading
screen1.preload()
screen2.preload()
screen3.preload()
screen4.preload()
screen5.preload()
text1.preload()
text2.preload()
screen6.preload()

# DOTS block and trial construction
dots_block = xpy.design.Block(name="DOTS")
dots_block.set_factor("condition", "DOTS")
for isi in ISI_VALUES:
    for _ in range(TRIALS_PER_ISI):
        trial = xpy.design.Trial()
        trial.set_factor("isi_ms", isi)
        dots_block.add_trial(trial)

# Randomization of DOTS trials
for i in range(len(dots_block.trials) - 1, 0, -1):
    j = random.randint(0, i)
    dots_block.trials[i], dots_block.trials[j] = dots_block.trials[j], dots_block.trials[i]

# SHAPES block and trial construction
shapes_block = xpy.design.Block(name="SHAPES")
shapes_block.set_factor("condition", "SHAPES")
for isi in ISI_VALUES:
    for _ in range(TRIALS_PER_ISI):
        trial = xpy.design.Trial()
        trial.set_factor("isi_ms", isi)
        shapes_block.add_trial(trial)

# Randomization of SHAPES trials
for i in range(len(shapes_block.trials) - 1, 0, -1):
    j = random.randint(0, i)
    shapes_block.trials[i], shapes_block.trials[j] = shapes_block.trials[j], shapes_block.trials[i]

# Stimuli for DOTS trials
for trial in dots_block.trials:
    trial.add_stimulus(screen1)
    trial.add_stimulus(screen2)
    trial.add_stimulus(screen5)
    trial.add_stimulus(text2)
    trial.add_stimulus(screen5)
    trial.add_stimulus(screen6)

# Stimuli for SHAPES trials
for trial in shapes_block.trials:
    trial.add_stimulus(screen3)
    trial.add_stimulus(screen4)
    trial.add_stimulus(screen5)
    trial.add_stimulus(text2)
    trial.add_stimulus(screen5)
    trial.add_stimulus(screen6)

# Experiment start
exp.add_block(dots_block)
exp.add_block(shapes_block)
xpy.control.start(skip_ready_screen=True)

# Counterbalancing
if exp.subject % 2 == 0:
    exp.blocks.reverse()

# Instructions
text1.present()
exp.keyboard.wait(keys=[xpy.misc.constants.K_SPACE])

# Trial presentation
for block in exp.blocks:
    for trial in block.trials:
        isi = trial.get_factor("isi_ms")
        trial.stimuli[2].present()
        exp.clock.wait(FIXATION_DURATION)

        for i in range(N_REPETITIONS):
            trial.stimuli[0].present()
            exp.clock.wait(FRAME_DURATION)
            if isi > 0:
                trial.stimuli[4].present()
                exp.clock.wait(isi)

            trial.stimuli[1].present()
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