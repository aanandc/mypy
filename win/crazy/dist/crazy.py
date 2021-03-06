#! /usr/bin/python

#an implmentation of the crazy eight game with AI

from random import choice
from datetime import datetime
import logging

suites=["C","S","D","H"]
faces=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
carddeck=[]
human_cards=[]
completed_pile=[]
comp_cards=[]
completed=[]
topcard=None

logenabled = False

if logenabled:
    logging.basicConfig(filename='crazy.log',level=logging.DEBUG)

def log(msg):
    if logenabled:
        logging.info(msg)

def build_default():
    deck=[]
    for f in faces:
        for s in suites:
            deck.append(f+s)
    return deck

def print_human_cards():
    print "human cards:",
    #TODO convert below print along to display method
    for h in human_cards:
        print h,
    print

def print_intro():
    for i in range(1,81):
        print "*",
    helpstr="""\nCRAZY EIGHTS
type the card value to drop it
f      - fetch a card from the pile
CTRL+c - To quit inbetween the game
h      - Rules of the game
a      - About the game
    """
    print helpstr

def print_line():
    for i in range(1,81):
        print "_",
    print

def main_stub():
    global human_cards,comp_cards,carddeck,topcard
    print_intro()
    log("new game started at " + str(datetime.now()))
    carddeck = build_default()
    carddeck = shuffledeck(carddeck)
    human_cards = getcards(carddeck,5)
    log("human cards")
    log(human_cards)
    comp_cards = getcards(carddeck,5)
    log("Computer cards")
    log(comp_cards)
    log("card pile")
    log(carddeck)
    win=False
    ourturn = is_computer_to_begin()
    #randomly assign who has to start the game
    topcard=getcard(carddeck) # start with the open card
    display("Open card is " + topcard)
    try:
        while win==False:
            if ourturn:
                play_computer(topcard)
                ourturn=False
            else:
                play_human(topcard)
                ourturn=True
            if len(human_cards)==0:
                display("You have won!!!")
                win=True
            elif len(comp_cards)==0:
                display("You have lost :-(")
                win=True
            print_line()
    except KeyboardInterrupt:
        display("\nQuit")
    finally:
        raw_input("Press Enter to exit...")
    


def reorder_completed():
    global carddeck,completed
    carddeck = [x for x in completed]
    carddeck = shuffledeck(carddeck)
    display("pile completed,shuffling deck from played pile")
    completed=[]
    
def play_human(topcard):
    global carddeck,completed,human_cards
    display("\nComputer has " + str(len(comp_cards)) + " cards left")
    print_human_cards()
    display("top : " + topcard)
    valid = False
    while not valid:
        play = raw_input("Your turn >>> ")
        play = play.upper() # so that the player can enter 9c or 9C
        if "a" == play or "A" == play:
          display("Created by Aanand Deepak C\nBeta version - 16/6/2014")
          continue
        elif "h" == play or "H" == play: 
          display("""
           Rules:
           Each player is distributed an equal number of cards in the beginning of the play.(Usually 5)
           The aim of the game is to dispose off all the cards you have.
           A valid card to dispose during your turn is a card with the same suite or same face of the top card.
           For example if the current top card is Jack of Hearts , then you can play any heart or any jack.
           Eight is special and can be played anytime.
           With an eight you also choose which suite the opponent must play the next card.
           If you can't play a valid card,then you need to fetch a card from the pile during your turn
           """)
          continue
        elif "f" == play or "F" == play:
            log("length of carddeck is " + str(len(carddeck)))
            if len(carddeck) == 0:
                #TODO reshuffle completed and put them
                reorder_completed()
            card = getcard(carddeck)
            human_cards.append(card)
            valid = True
            return
        elif play not in human_cards:
            display("You do not have that card..try again")
        elif not valid_play(topcard,play):
            display("Does not obey game rule..try again")
        else:
            valid = True
    if valid:
        if isEight(play):
            valid_input=False
            val=None
            while not valid_input:
                if len(human_cards)==1:
                    #as eight is the last card,
                    #its our turn and we have won.
                    #so lets clear the human cards instead of asking for suites.
                    human_cards=[]
                    return # if we play 8 as the last card
                val = raw_input("Diamond (D),Hearts (H),Spade (S),Clubs (C),What suite ?")
                if val in ["D","d","H","h","c","C","s","S"]:
                    valid_input=True
                else:
                    display("You played a eight.So select a suite..")
            if valid_input:
                val = "*" + val.upper()
                play_card(human_cards,play,val)
                    
        else:
            play_card(human_cards,play)
            
                
def play_card(hand,card,suiteForEight=None):
    global topcard
    topcard = card if suiteForEight == None else suiteForEight # for setting in case of eight
    log("Top card is now " + topcard)
    hand.remove(card)
    completed.append(card)
    log("completed")
    log(completed)

def play_computer(topcard):
    global comp_cards
    draw = False
    play = None
    for card in comp_cards:
        if is_sameSuite(topcard,card) or is_sameFace(topcard,card):
            if isEight(card):
                continue
            play = card
            print "Computer plays " + play
            play_card(comp_cards,play)
            break
    if play == None:
        # no matching suite, so lets see if we have a eight
        for card in comp_cards:
            if isEight(card):
                play = card
                choiceSuite="*" + find_max_suite(comp_cards)
                display("Computer plays " + play)
                disp_computer_choice(choiceSuite)
                play_card(comp_cards,play,choiceSuite)
                break
    #Can't find a match or a eight, so we have to draw
    if play == None:
        draw = True
    if draw == True:
        log("in play_computer length of carddeck is " + str(len(carddeck)))
        if len(carddeck) == 0:
                #TODO reshuffle completed and put them
                reorder_completed()
        card = getcard(carddeck)
        comp_cards.append(card)
        print "computer draws a card from the pile..."

def display(string):
    print string
    log(string)

def disp_computer_choice(choicesuite):
    mapping={"*D":"Diamond","*H":"Heart","*S":"Spade","*C":"Club"}
    return "Computer chooses " + mapping[choicesuite] + " suite"

def find_max_suite(pile):
    newpile = filter(notEight,pile)
    d,h,s,c=0,0,0,0
    val = []
    for card in newpile:
        if "D" == getSuite(card):
            d = d + 1
        elif "S" == getSuite(card):
            s = s + 1
        elif "H" == getSuite(card):
            h = h + 1
        else:
            c = c + 1
    max_val = max(d,h,s,c)
    suite=None
    if d == max_val:
        suite = "D"
    elif h == max_val:
        suite = "H"
    elif s == max_val:
        suite = "S"
    else:
        suite = "C"
    log("d is " + str(d) + " h is " + str(h) + " s is " + str(s) + " c is " + str(c))
    return suite

def valid_play(topcard,curr):
    if is_sameSuite(topcard,curr) or is_sameFace(topcard,curr) or isEight(curr):
        return True
    else:
        return False

def notEight(card):
    return not isEight(card)

def isEight(card):
    if getFace(card) == "8":
        return True
    else:
        return False

def getSuite(card):
    if len(card) == 3 : # special handling for 10
        return card[2]
    else:
        return card[1]

def getFace(card):
    if len(card) == 3: # special handling for 10
        return card[0:2]
    else:
        return card[0]

def is_sameSuite(card1,card2):
    if getSuite(card1) == getSuite(card2):
        return True
    else:
        return False

def is_sameFace(card1,card2):
    if getFace(card1) == getFace(card2):
        return True
    else:
        return False
        
def is_computer_to_begin():
    val=[x for x in range(1,1000)]
    x = choice(val)
    if x%2==0:
        return True
    else:
        return False

def fetch_card(deck,player_hand):
    return None

def getcards(deck,num_of_cards=1):
    cards=[]
    for i in range(0,num_of_cards):
        cards.append(deck.pop())
    return cards

def getcard(deck):
    card = deck.pop()
    return card
        

def shuffledeck(deck):
    shuffled=[]
    while len(deck)>0:
        pos = choice(range(0,len(deck)))
        shuffled.append(deck.pop(pos))
    return shuffled


main_stub()


    

