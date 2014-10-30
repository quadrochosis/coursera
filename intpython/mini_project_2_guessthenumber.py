# Interactive Python Coursera Mini Project 2: Guess the Number

# All input will be entered in a Simple GUI frame
# All output will be in the CodeSkulptor console

# This game will take guesses from a player until the 
# player correctly chooses the number randomly chosen by the computer
# Additionally, players will have a limited number of 
# guesses based on which game mode they are playing

# Import modules
import simplegui
import random
import math

# Default Global Variables
game_range = 100
tot_guesses = 7

# Helper function to start and restart the game
def new_game():
    global secret_number
    secret_number = random.randrange(0, game_range)
    print "New Game with a Range of [0 - " + str(game_range) + ")" 
    print "You will have", tot_guesses, "chances to guess correctly!"
    print ""

# Define event handlers for control panel
def range100():
    global game_range
    global tot_guesses
    game_range = 100
    tot_guesses = 7
    new_game()

def range1000():
    global game_range
    global tot_guesses
    game_range = 1000
    tot_guesses = 10
    new_game()
    
def input_guess(guess):
    global tot_guesses
    guess = int(guess)
    tot_guesses-=1

    print "Guess was", guess

    if tot_guesses == 1:
        print "You have 1 guess left"
    elif tot_guesses > 1:
        print "You have", tot_guesses, "guesses remaining"
        
    if tot_guesses >= 1:
        if guess == secret_number:
            print "Correct!"
            print ""
            if game_range == 100:
                range100()
            elif game_range == 1000:
                range1000()
        elif guess > secret_number:
            print "Lower!"
        elif guess < secret_number:
            print "Higher!"
        print ""
    elif tot_guesses < 1:
        if guess == secret_number:
            print "You have", tot_guesses, "guesses remaining"
            print "Correct!"
            print ""
            if game_range == 100:
                range100()
            elif game_range == 1000:
                range1000()
        else:
            print "You have run out of guesses. The number was", secret_number
            print ""
            if game_range == 100:
                range100()
            elif game_range == 1000:
                range1000()
        
# Create a frame where the player will input their 
# numbers and change other game options
frame = simplegui.create_frame("Guess the Number!", 200, 200)

# Register event handlers for control elements and start frame
frame.add_button("New Game, Range of 0-100", range100, 200)
frame.add_button("New Game, Range of 0-1000", range1000, 200)
frame.add_input("Guess a number:", input_guess, 200)

# As soon as program is initiated, begin new game 
new_game()