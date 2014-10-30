# Interactive Python Coursera Mini Project 6: Blackjack

# Implementation of casino card game, Blackjack. In this implementation, After a player "stands" the dealer draws
# cards until his hand is equal to or greater than 17. Additionally, all ties are counted as wins for the dealer.

import simplegui
import random

# Load playing cards sprite, and playing card back - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# Definitions of global variables.
in_play = False
outcome = ""
wins = 0
losses = 0

# Definitions of card values and their suits.
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# Card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        # Figure out which card to draw from the sprite sheet depending on the card's rank and suit
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# Hand class
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        s = ""
        for item in self.cards:
            s += str(item) + " "
        return "Hand contains: " + s

    def add_card(self, card):
        self.cards.append(card)        

    def get_value(self):
        # Obtain the value of a hand, including Ace rules
        value = 0
        aces = 0
        for i in self.cards:
            if i.get_rank() == "A":
                aces+=1
            value += VALUES[i.get_rank()]

        if aces == 0:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value
   
    def draw(self, canvas, pos):
        # Draw hands on the canvas
        for i in self.cards:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(i.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(i.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0] + CARD_SIZE[0] * self.cards.index(i), pos[1] + CARD_CENTER[1]], CARD_SIZE)
 
# Deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(0, 4):
            rank = 0
            for rank in range(0, 13):
                self.cards.append(Card(SUITS[suit], RANKS[rank]))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        s = ""
        for item in self.cards:
            s += str(item) + " "
        return "Deck contains: " + s

# Button event handlers
def deal():
    global outcome, in_play, deck, p_hand, d_hand

    # Initialize a new Deck for new game
    deck = Deck()
    deck.shuffle()

    # Create hands for the player and the dealer
    p_hand = Hand()
    d_hand = Hand()

    # Deal two cards to both participants, in proper order
    p_hand.add_card(deck.deal_card())
    d_hand.add_card(deck.deal_card())
    p_hand.add_card(deck.deal_card())
    d_hand.add_card(deck.deal_card())

    # Change outcome prompt message
    outcome = "Would you like to Hit or Stand?"

    # Change player's status to 'in play'
    in_play = True

def hit():
    global outcome, losses, in_play

    # This button will only work if a hand is in play
    if in_play == True:
        # Deal player a card
        p_hand.add_card(deck.deal_card())

        # Determine if the player has busted
        if p_hand.get_value() > 21:
            outcome = "Bust! Dealer wins. Deal again?"
            in_play = False
            losses+=1
       
def stand():
    global outcome, wins, losses, in_play

    # This button will only work if a hand is in play
    if in_play == True:
        if p_hand.get_value() > 21:
            outcome = "Bust! Dealer wins. Deal again?"
            in_play = False
            losses+=1

        # Hit the dealer until he is at or above 17, and then determine winner
        else:
            while d_hand.get_value() <= 17:
                d_hand.add_card(deck.deal_card())

            else:
                if d_hand.get_value() > 21:
                    outcome = "Dealer has Busted! You win! Deal again?"
                    in_play = False
                    wins+=1

                elif p_hand.get_value() <= d_hand.get_value():
                    outcome = "Dealer wins. Deal again?"
                    in_play = False
                    losses+=1
                    
                else:
                    outcome = "You win! Deal again?"
                    in_play = False
                    wins+=1

# Draw handler    
def draw(canvas):
    d_hand.draw(canvas, [0, 250])
    p_hand.draw(canvas, [0, 475])
    canvas.draw_text("Blackjack", [200, 75], 50, "Black")
    canvas.draw_text("Wins: " + str(wins), [500,150], 24, "Black")
    canvas.draw_text("Losses: " + str(losses), [475, 170], 24, "Black")
    canvas.draw_text("Dealer:", [0, 225], 24, "Black")
    canvas.draw_text("Player:", [0, 450], 24, "Black")
    canvas.draw_text(outcome, [0,150], 24, "Black")

    # Display dealer's 'hole' card if the hand is over
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [0 + CARD_BACK_CENTER[0], 250 + CARD_BACK_CENTER[1]], CARD_SIZE)

# Frame initialization
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# Button creation and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# Begin game as soon as program is run
deal()
frame.start()