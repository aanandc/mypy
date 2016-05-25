import win32api,sys,win32con,math
from Tkinter import * ### (1)
from threading import Timer
from win32api import GetSystemMetrics
width = GetSystemMetrics (0)
height = GetSystemMetrics (1)
root = Tk()

DEBUG=True

root.iconbitmap('money.ico')
#root.iconbitmap(None)

def printlog(msg):
        if DEBUG:
                print msg

class UI:
	def __init__(self, myParent):
                self.myContainer1 = Frame(myParent,height=200,width=200)
                self.amountlabel = Label(self.myContainer1, text="Amount")
                self.yearslabel = Label(self.myContainer1, text="Years")
                self.amount = Entry(self.myContainer1)#myContainer1.pack_propagate(0) # don't shrink
                self.myContainer1.grid(row=0)
                self.amountlabel.grid(row=0,column=1)
                self.amount.grid(row=0,column=2)
                self.yearslabel.grid(row=1,column=1)
                self.years = Entry(self.myContainer1)
                self.years.grid(row=1,column=2)
                self.interestlabel = Label(self.myContainer1, text="Interest")
                self.interestlabel.grid(row=2,column=1)
                self.interest = Entry(self.myContainer1)
                self.interest.grid(row=2,column=2)
                self.cilabel = Label(self.myContainer1, text="CI")
                self.cilabel.grid(row=3,column=1)
                self.ci = Entry(self.myContainer1)
                self.ci.grid(row=3,column=2)
                self.ycilabel = Label(self.myContainer1, text="YCI")
                self.ycilabel.grid(row=4,column=1)
                self.yci = Entry(self.myContainer1)
                self.yci.grid(row=4,column=2)
                self.profitlabel = Label(self.myContainer1, text="Profit")
                self.profitlabel.grid(row=5,column=1)
                self.profit = Entry(self.myContainer1)
                self.profit.grid(row=5,column=2)
                button1 = Button(self.myContainer1)
                button1["text"]= "CALC"    ### (2)
                button1.bind("<Button-1>", self.onClick)
                #root.geometry('+'+str(width-150)+ '+'+ str(height-200))
                button1.grid(row=6,column=1)

        def extractYears(self,inpYears):
                if "days" in inpYears or "day" in inpYears:
                        pos = inpYears.find("day")
                        days = float(inpYears[0:pos])
                        inpYears = str(days/365)#Atleast most years have 365
                printlog("years is " + inpYears)
		return inpYears

        def onClick(self,event):
                amt = float(self.amount.get())
                y = float(self.extractYears(self.years.get()))
                i = float(self.interest.get())
                compInt = amt * pow(( 1 + (i/100)),y)
                self.ci.delete(0, END)
                self.ci.insert(0, str(round(compInt)))
                self.yci.delete(0,END)
                cumiCompInt = 0
                for year in range(int(y),0,-1):
                        myint = amt * pow(( 1 + (i/100)),year)
                        cumiCompInt = cumiCompInt + myint
                self.yci.insert(0,str(round(cumiCompInt)))
		profitStr = "ci:" + str(round(compInt-amt))
                if y>1:
                        profitStr = profitStr + " yci:"+str(round(cumiCompInt - (y*amt)))
                self.profit.delete(0,END)
                self.profit.insert(0,profitStr)
                
	

def quitfunc():
	root.destroy()
	sys.exit(0)
		
def main_stub():
	ui = UI(root)
	root.resizable(width=FALSE, height=FALSE)
	#root.minsize(100,100)
	root.protocol("WM_DELETE_WINDOW", quitfunc)
	root.wm_title("Interest")
	root.mainloop()
	

main_stub()
	
