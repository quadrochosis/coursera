# Interactive Python Coursera Mini Project 4: Pong

# Implementation of the classic arcade game, Pong. This game is designed for two players
# competing locally (ie. next to each other). The left paddle is controlled by player 1 using 
# the 'w' and 's' keys, and the right paddle is controlled by player 2 using the up and
# down arrow keys

import simplegui
import random

# Definitions
WIDTH = 600.0
HEIGHT = 400.0       
BALL_RADIUS = 8
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [WIDTH / 2.0, HEIGHT / 2.0]
ball_vel = [random.randrange(-4.0, 0.0), random.randrange(-3.0, 0.0)]
pad1_pos = [HEIGHT / 2 - HALF_PAD_HEIGHT, HEIGHT / 2 + HALF_PAD_HEIGHT]
pad2_pos = [HEIGHT / 2 - HALF_PAD_HEIGHT, HEIGHT / 2 + HALF_PAD_HEIGHT]
pad1_vel = 0
pad2_vel = 0
score1 = 0
score2 = 0

# Definition for function to spawn the ball at the beginning of a new round
# Boolean 'direction' passed into spawn_ball determines which direction
# the ball travels first for the next round. 'True' means that player 1 has won and 
# that the ball will travel to the left next round, and vice versa
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2.0, HEIGHT / 2.0]
    if direction:
        ball_vel = [random.randrange(-4.0, 0.0), random.randrange(-3.0, 0.0)]
    else:
        ball_vel = [random.randrange(1.0, 4.0), random.randrange(-3.0, 0.0)]

# Definitions for event handlers

# New game is called when the program is initiated and when the 'Reset' button
# is pressed
def new_game():
    global pad1_pos, pad2_pos, pad1_vel, pad2_vel
    global score1, score2
    score1 = 0
    score2 = 0
    pad1_pos = [HEIGHT / 2 - HALF_PAD_HEIGHT, HEIGHT / 2 + HALF_PAD_HEIGHT]
    pad2_pos = [HEIGHT / 2 - HALF_PAD_HEIGHT, HEIGHT / 2 + HALF_PAD_HEIGHT]
    pad1_vel = 0
    pad2_vel = 0
    
# The draw handler is the meat of this project, it moves all the component around and 
# continuously draws them at 60 FPS. 
def draw(canvas):
    global score1, score2, pad1_pos, pad2_pos, ball_pos, ball_vel
        
    # Mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # Update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # Draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # Bounce off top wall
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    # Bounce off bottom wall
    if ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
        
    # Test to see if hits sides, and reset if it does, or bounce (and speed up by 15%) when it hits paddle
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= pad1_pos[0] and ball_pos[1] <= pad1_pos[1]:
            ball_vel[0] = (- ball_vel[0]) * 1.15
            ball_vel[1] = ball_vel[1] * 1.15            
        else:
            spawn_ball(False)
            score2+=1
            
    if ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        if ball_pos[1] >= pad2_pos[0] and ball_pos[1] <= pad2_pos[1]:
            ball_vel[0] = (- ball_vel[0]) * 1.15
            ball_vel[1] = ball_vel[1] * 1.15
        else:
            spawn_ball(True)
            score1+=1
    
    # Update paddles vertical positions while keeping paddles on the screen
    if pad1_pos[0] + pad1_vel >= 0 and pad1_pos[1] + pad1_vel <= HEIGHT:
        pad1_pos[0] += pad1_vel
        pad1_pos[1] += pad1_vel
    
    if pad2_pos[0] + pad2_vel >= 0 and pad2_pos[1] + pad2_vel <= HEIGHT:
        pad2_pos[0] += pad2_vel
        pad2_pos[1] += pad2_vel
        
    # Draw paddles
    canvas.draw_line((HALF_PAD_WIDTH, pad1_pos[0]), (HALF_PAD_WIDTH, pad1_pos[1]), PAD_WIDTH, "White")
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, pad2_pos[0]), (WIDTH - HALF_PAD_WIDTH, pad2_pos[1]), PAD_WIDTH, "White")
        
    # Draw scores
    canvas.draw_text(str(score1), (150, 50), 40, "White")
    canvas.draw_text(str(score2), (450, 50), 40, "White")
        
# Handler for when buttons which move paddles are pressed down
def keydown(key):
    global pad1_vel, pad2_vel
    acc = 4
    if key == simplegui.KEY_MAP["w"]:
        pad1_vel -= acc
    elif key == simplegui.KEY_MAP["s"]:
        pad1_vel += acc
    elif key == simplegui.KEY_MAP["up"]:
        pad2_vel -= acc
    elif key == simplegui.KEY_MAP["down"]:
        pad2_vel += acc
    
# Handler for when buttons which move paddles are released   
def keyup(key):
    global pad1_vel, pad2_vel
    if key == simplegui.KEY_MAP["w"]:
        pad1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        pad1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        pad2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        pad2_vel = 0

# Handler for button which resets the game
def reset():
    new_game()
    spawn_ball(True)

# Frame creation with drawn canvas and event handlers
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset = frame.add_button("Reset", reset, 50)

# Begin game
new_game()
frame.start()