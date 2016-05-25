import win32api,sys,win32con,math
from Tkinter import * ### (1)
from threading import Timer
from win32api import GetSystemMetrics
width = GetSystemMetrics (0)
height = GetSystemMetrics (1)

root = Tk()
#root.iconbitmap(None)
myContainer1 = Frame(root,height=100,width=100)
myContainer1.pack_propagate(0) # don't shrink
myContainer1.pack()
button1 = Button(myContainer1) 

enabled = True

def move_mouse(x,y):
	nx = int(math.ceil(x*65535.0/win32api.GetSystemMetrics(0)))
	ny = int(math.ceil(y*65535.0/win32api.GetSystemMetrics(1)))
	win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx,ny)

def move():
	val = win32api.GetCursorPos()
	move_mouse(0,0)
	print(val[0],val[1])
	move_mouse(val[0],val[1])
	#win32api.SetCursorPos(val)

def test_move():
	print "test move called"
	move()
	if enabled:
		keep_moving()
	
def keep_moving():	
	print "keep moving called"
	t = Timer(10,test_move)
	t.setDaemon(True)
	t.start()
		
		
def onClick(event):
	global enabled
	if enabled:
		enabled = False
	else:
		enabled = True
		test_move()
	mod_button()

def mod_button():
	if enabled:
		button1["text"]="Enabled"
		button1["background"]="green"
	else:
		button1["text"]="Disabled"
		button1["background"]="red"

def quitfunc():
	print "enabled is set as false"
	enabled = False
	root.destroy()
	sys.exit(0)
		
def main_stub():
	keep_moving()
	button1["text"]= "Enabled"    ### (2)
	button1["background"] = "green"     ### (3)
	button1.bind("<Button-1>", onClick)
	root.geometry('+'+str(width-150)+ '+'+ str(height-200))
	root.resizable(width=FALSE, height=FALSE)	
	root.minsize(100,100)
	button1.pack(fill=BOTH, expand=1)
	root.protocol("WM_DELETE_WINDOW", quitfunc)
	root.wm_title("mouse mover")
	root.mainloop()
	

main_stub()
	