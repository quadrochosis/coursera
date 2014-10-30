# Interactive Python Coursera Mini Project 3: Stopwatch- The Game

# This game will consist of a stopwatch with three buttons: 
# start, stop and reset. If the player stops the stopwatch on a 
# whole number, they will get one win added to their score.

import simplegui

# Define global variables
time = 0
wins = 0
stops = 0
running_bool = False

# Define a function that converts the timer ticks (in tenths of a second) 
# into a stopwatch format
def format(t):
    A = str(t // 600)
    B = str(((t // 10) % 60) // 10)
    C = str(((t // 10) % 60) % 10)
    D = str(t % 10)
    return A + ":" + B + C[-1] + "." + D
    
# Define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running_bool
    timer.start()
    running_bool = True

def stop():
    global stops, wins, running_bool
    if running_bool == True:
        stops += 1
        if time % 10 == 0:
            wins += 1
    timer.stop()
    running_bool = False

def reset():
    global time, wins, stops
    timer.stop()
    time = 0
    wins = 0
    stops = 0

# Define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1

# Define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(time), (72,100), 24, "White")
    canvas.draw_text(str(wins) + "/" + str(stops), (160, 20), 22, "Grey")
    
# Create frame
frame = simplegui.create_frame("Stopwatch: The Game!", 200, 200)

# Register event handlers for the timer and buttons
timer = simplegui.create_timer(100, timer_handler)
start = frame.add_button("Start", start, 50)
stop = frame.add_button("Stop", stop, 50)
reset = frame.add_button("Reset", reset, 50)

# Start frame and draw the stopwatch in the stopped position
frame.start()
frame.set_draw_handler(draw_handler)