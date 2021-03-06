#! /usr/bin/python
# -*- coding: utf-8 -*-

#an implmentation of the crazy eight game with AI


import win32api,sys,win32con,math
from Tkinter import * ### (1)
from threading import Timer
from win32api import GetSystemMetrics
mywidth = GetSystemMetrics (0)
myheight = GetSystemMetrics (1)
from random import choice
from datetime import datetime
import logging
import tkMessageBox
from ScrolledText import *


root = None
ui = None

DEBUG=True
from PIL import Image, ImageTk

#root.iconbitmap(None)

def printlog(msg):
        if DEBUG:
                print msg

class UI:
        def print_message(self,msg):
                msg = msg + "\n"
                self.scrollview["state"] = NORMAL
                self.scrollview.mark_set("insert", "1.0")# 1 is line number , 0 is coloumn
                self.scrollview.insert(INSERT,msg) # or END can be used
                self.scrollview["state"] = DISABLED
                #self.scrollview.see(END)
                
	def __init__(self, myParent):
                self.mylist = [i for i in range(1,53)]
                self.display_cards(human_cards)
                self.button1 = Button(root)
                self.button1["text"]= "Fetch"    ### (2)
                self.button1.bind("<Button-1>", self.onFetchClick)
                self.button1.grid(row=1,column=10)
                self.scrollview = ScrolledText(root,width=10,height = 10,state = DISABLED)
                self.scrollview.grid(row=200,column=5)
                #self.scrollbar = Scrollbar(root) 
                #self.scrollbar.pack(side=RIGHT, fill=Y)
    

        def display_top_card(self,topc):
            self.image = Image.open("classic-cards/"+topc+".png")
            #self.image = self.image.rotate(45)
            #self.image = self.image.resize((100,200))
            self.photo = ImageTk.PhotoImage(self.image)
            self.label = Label(image=self.photo)
            self.label.image = self.photo # keep a reference!
            self.label.filename = topc
            self.label.grid(row=0,column=10)
            print "length of cards is " + str(len(comp_cards))
            self.leftlabel = Label(root,text= "PC has " + str(len(comp_cards)) + " cards",font = "Verdana 10 bold")
            self.leftlabel.grid(row=2,column=10)


        def display_cards(self,newlist):
                r = 0
                c = -1
                counter = 0 
                self.mywidgets=[]
                for i in newlist:
                        if counter%10 == 0:
                                r = r + 1
                                c = 0
                        else:
                                c = c + 1
                        counter = counter + 1
                        self.image = Image.open("classic-cards/"+str(i)+".png")
                        #self.image = self.image.rotate(45)
                        #self.image = self.image.resize((100,200))
                        self.photo = ImageTk.PhotoImage(self.image)
                        self.label = Label(image=self.photo)
                        self.label.image = self.photo # keep a reference!
                        self.label.filename = i
                        self.label.grid(row=r,column=c)
                        self.label.bind("<Button-1>", self.onClick)
                        self.mywidgets.append(self.label)

        def onFetchClick(self,event):
            global human_cards
            if len(carddeck) == 0:
                #TODO reshuffle completed and put them
                reorder_completed()
            card = getcard(carddeck)
            human_cards.append(card)
            self.destroyAll()
            self.display_cards(human_cards)
            play_computer(topcard)
            if len(comp_cards) == 0:
                    tkMessageBox.showinfo("Boooo", "You have lost :-( ")
                    quitfunc()
            self.display_top_card(topcard)

        def onClick(self,event):
                global human_cards,comp_cards,carddeck,topcard
                #self.mylist.remove(event.widget.filename)
                if(play_human(topcard,event.widget.filename)):
                    self.destroyAll()
                    self.display_cards(human_cards)
                    if len(human_cards) == 0:
                        tkMessageBox.showinfo("Crazy", "You have won!!!")
                        quitfunc()
                    play_computer(topcard)
                    print str(len(comp_cards)) + " before modify"
                    if len(comp_cards) == 0:
                        tkMessageBox.showinfo("Boooo", "You have lost :-( ")
                        quitfunc()
                    self.display_top_card(topcard)
                
                

        def destroyAll(self):
                for i in self.mywidgets:
                        i.destroy()

                
def quitfunc():
	root.destroy()
	sys.exit(0)
		

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

USER_SELECTED_SUITE="ZC"

def hello():
        rulesstr="""Rules:

Each player is distributed an equal number of cards in the beginning of the play.(Usually 5)
The aim of the game is to dispose off all the cards you have.
A valid card to dispose during your turn is a card with the same suite or same face of the top card.
For example if the current top card is Jack of Hearts , then you can play any heart or any jack.
Eight is special and can be played anytime.
With an eight you also choose which suite the opponent must play the next card.
If you can't play a valid card,then you need to fetch a card from the pile during your turn








© 2015, Aanand Deepak C 
""" 
        tkMessageBox.showinfo("Rules", rulesstr)


class MyDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        #top.protocol("WM_DELETE_WINDOW", hello)
        Label(top, text="What suite do you want ?").pack()
        self.heartButton  = Button(top,text="Heart",command=self.heart)
        self.heartButton.pack()
        self.spadeButton  = Button(top,text="Spade",command=self.spade)
        self.spadeButton.pack()
        self.cloverButton  = Button(top,text="Clover",command=self.clover)
        self.cloverButton.pack()
        self.diamondButton  = Button(top,text="Diamond",command=self.diamond)
        self.diamondButton.pack()
        #b = Button(top, text="OK", command=self.ok)
        #b.pack(pady=5)
    def heart(self):
        global USER_SELECTED_SUITE
        print "hearts"
        USER_SELECTED_SUITE = "ZH"
        self.top.destroy()
    def spade(self):
        global USER_SELECTED_SUITE
        print "spades"
        USER_SELECTED_SUITE = "ZS"
        self.top.destroy()
    def clover(self):
        global USER_SELECTED_SUITE
        print "clovers"
        USER_SELECTED_SUITE = "ZC"
        self.top.destroy()
    def diamond(self):
        global USER_SELECTED_SUITE
        print "diamonds"
        USER_SELECTED_SUITE = "ZD"
        self.top.destroy()

def main_stub():
    global root,ui
    UI_MODE = True
    root = Tk()
    root.iconbitmap('game.ico')
    ui = UI(root)
    menubar = Menu(root)
    menubar.add_command(label="Help", command=hello)
    root.config(menu=menubar)

    #root.resizable(width=FALSE, height=FALSE)
    root.minsize(mywidth-100,myheight-100)
    root.protocol("WM_DELETE_WINDOW", quitfunc)
    root.wm_title("Crazy Eights")
    #root.mainloop()
    global human_cards,comp_cards,carddeck,topcard
    #print_intro()
    log("new game started at " + str(datetime.now()))
    carddeck = build_default()
    carddeck = shuffledeck(carddeck)
    human_cards = getcards(carddeck,5)
    ui.display_cards(human_cards)
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
    if not ourturn:
            play_computer(topcard)
    ui.display_top_card(topcard)
    display("Open card is " + topcard)
    root.mainloop()


def reorder_completed():
    global carddeck,completed
    carddeck = [x for x in completed]
    carddeck = shuffledeck(carddeck)
    ui.print_message("reshuffling..")
    completed=[]

    
def play_human(topcard,play):
    global carddeck,completed,human_cards
    display("\nComputer has " + str(len(comp_cards)) + " cards left")
    print_human_cards()
    valid = False
    if not valid_play(topcard,play):
        ui.print_message("invalid")
        return False
    else:
        valid = True
    if valid:
        if isEight(play):
            if len(human_cards)==1:
                    #as eight is the last card,
                    #its our turn and we have won.
                    #so lets clear the human cards instead of asking for suites.
                    human_cards=[]
                    #TODO Print Winning Dialog
                    tkMessageBox.showinfo("Crazy", "You have won!!!")
                    quitfunc()
                    return # if we play 8 as the last card
                # val = raw_input("Diamond (D),Hearts (H),Spade (S),Clubs (C),What suite ?")
                # if val in ["D","d","H","h","c","C","s","S"]:
                #     valid_input=True
                # else:
                #     display("You played a eight.So select a suite..")
            #val = "ZC" # hard code that we have selected claver for now
            d = MyDialog(root)
            root.wait_window(d.top)
            val = USER_SELECTED_SUITE
            play_card(human_cards,play,val)
        else:
            play_card(human_cards,play)
        return True # we played a valid thing, so return True
            
                
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
            ui.print_message("PC -> " + play)
            play_card(comp_cards,play)
            break
    if play == None:
        # no matching suite, so lets see if we have a eight
        for card in comp_cards:
            if isEight(card):
                play = card
                choiceSuite="Z" + find_max_suite(comp_cards)
                ui.print_message("PC -> " +  play)
                ui.print_message("PC chooses " + disp_computer_choice(choiceSuite))
                #disp_computer_choice(choiceSuite)
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
        ui.print_message("PC draws")

def display(string):
    print string
    log(string)

def disp_computer_choice(choicesuite):
    mapping={"ZD":"Diamond","ZH":"Heart","ZS":"Spade","ZC":"Club"}
    return mapping[choicesuite]

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
    print x
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


    

