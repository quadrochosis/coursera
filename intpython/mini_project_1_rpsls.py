# First mini project for Interactive Python. 
#This program will simulate a game of Rock, Paper, 
#Scissors, Lizard Spock using a random number generator 
#and display the results.
#
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

def name_to_number(name):
    """
    This function will take the input of the 
    player and convert it into a number, 
    allowing for a simpler calculation to determing 
    a winner
    """
    
    if name == "rock":
        name = 0
    elif name == "Spock":
        name = 1
    elif name == "paper":
        name = 2
    elif name == "lizard":
        name = 3
    elif name == "scissors":
        name = 4
    else:
        print "Error: incorrect input"

    return name

def number_to_name(number):
    """
    This function will take the number generated 
    by the computer and convert it into the 
    appropriate string.
    """
    
    if number == 0:
        number = "rock"
    elif number == 1:
        number = "Spock"
    elif number == 2:
        number = "paper"
    elif number == 3:
        number = "lizard"
    elif number == 4:
        number = "scissors"
    else:
        print "Error: number out of range"

    return number
    

def rpsls(player_choice): 
    """
    This function will actually compute 
    the winner of the RPSLS game by converting 
    the player input into a number, generating 
    a number randomly for the computer, determining 
    the winner and then returning the results
    """

    # Print the player's choice
    print ""
    print "Player chooses", player_choice

    # Convert player's choice to a number
    player_number = name_to_number(player_choice)

    # Randomly generate a number between 0 and 4 
    #for the computer
    comp_number = random.randrange(0, 5)

    # Convert computer's number into a name
    comp_choice = number_to_name(comp_number)

    # Print the computer's choice
    print "Computer chooses", comp_choice

    # Compute the difference between the player's 
    #number and the computer's
    difference = player_number - comp_number
    
    # Using conditionals, check to see who 
    #the winner is, and print out the result
    if difference % 5 == 0:
        print "Tie game!"
    elif difference % 5 == 1:
        print "Player wins!"
    elif difference % 5 == 2:
        print "Player wins!"
    elif difference % 5 == 3:
        print "Computer wins!"
    elif difference % 5 == 4:
        print "Computer wins!"
    else:
        print "Error: Problem with modular arithmetic"
   
# Calls to test and play the game!
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")