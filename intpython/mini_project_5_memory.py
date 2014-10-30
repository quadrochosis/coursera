# Interactive Python Coursera Mini Project 5: Memory

# Implementation of Memory card game. In this version, players will be dealt 16 "cards", consisting of the numbers one 
# through eight, with each repeating twice. 

import simplegui
import random

# Global Definitions
last = 0
lastlast = 0
pos_index = 0
first = 0
second = 0
turns = 0
hand = [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7]
exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
CARD_COORD = [(20, 60), (70, 60), (120, 60), (170, 60), (220, 60), (270, 60), (320, 60), (370, 60), (420, 60), (470, 60), (520, 60), (570, 60), (620, 60), (670, 60), (720, 60), (770, 60)]
RECT_COORD = [[(20, 5), (20, 95)], [(70, 5), (70, 95)], [(120, 5), (120, 95)], [(170, 5), (170, 95)], [(220, 5), (220, 95)], [(270, 5), (270, 95)], [(320, 5), (320, 95)], [(370, 5), (370, 95)], [(420, 5), (420, 95)], [(470, 5), (470, 95)], [(520, 5), (520, 95)], [(570, 5), (570, 95)], [(620, 5), (620, 95)], [(670, 5), (670, 95)], [(720, 5), (720, 95)], [(770, 5), (770, 95)]]

# New Game function to initialize global variables
def new_game():
    global state, exposed, turns
    state = 0
    turns = 0
    random.shuffle(hand)
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

# Mouse click handler, game logic is written here
def mouseclick(pos):
    global state, turns, pos_index, exposed, first, second, last, lastlast, label
    if pos[0] in range(0,45):
        pos_index = 0
    elif pos[0] in range(45, 95):
        pos_index = 1
    elif pos[0] in range(95, 145):
        pos_index = 2
    elif pos[0] in range(145, 195):
        pos_index = 3
    elif pos[0] in range(195, 245):
        pos_index = 4
    elif pos[0] in range(245, 295):
        pos_index = 5
    elif pos[0] in range(295, 345):
        pos_index = 6
    elif pos[0] in range(345, 395):
        pos_index = 7
    elif pos[0] in range(395, 445):
        pos_index = 8
    elif pos[0] in range(445, 495):
        pos_index = 9
    elif pos[0] in range(495, 545):
        pos_index = 10
    elif pos[0] in range(545, 595):
        pos_index = 11
    elif pos[0] in range(595, 645):
        pos_index = 12
    elif pos[0] in range(645, 695):
        pos_index = 13
    elif pos[0] in range(695, 745):
        pos_index = 14
    elif pos[0] in range(745, 800):
        pos_index = 15

    if state == 0:
        exposed[pos_index] = True
        first = hand[pos_index]
        state = 1
        lastlast = pos_index
        
    elif state == 1:
        if exposed[pos_index] == False:
            exposed[pos_index] = True
            second = hand[pos_index]
            state = 2
            last = pos_index

    else:
        if exposed[pos_index] == False:
            if first != second:
                exposed[lastlast] = False
                exposed[last] = False

            exposed[pos_index] = True
            first = hand[pos_index]
            state = 1
            lastlast = pos_index
            turns += 1
            label.set_text("Turns: %s" % (turns))
                    
# Draw canvas and cards, face down and face up
def draw(canvas):
    for i in range(0, 16):
        canvas.draw_text(str(hand[i]), CARD_COORD[i], 24, 'White')
    for i in range(0, 16):
        if exposed[i] == False:
            canvas.draw_line((RECT_COORD[i][0]), (RECT_COORD[i][1]), 45, 'Green')
 
# Frame creation with buttons and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns: %s" % (turns))

# Event Handler registration
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# Begin game immediately upon running program
new_game()
frame.start() 