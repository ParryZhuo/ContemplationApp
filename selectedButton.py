import tkinter as tk
import operator
import json
# import pdb
#from settings import storeObject
from textBox import AutoResizedText
import copy
import sys
from tkinter import filedialog
# https://tkdocs.com/tutorial/text.html <- good for learning tk.;
#text.see() is helpful for future

class object:# so our bug exists on the first nodes siblings.
    def __init__(self, master,height,width,word= "",child= None,parent = None, sibling= None):
        self.master = master
        self.child = child 
        self.parent = parent
        self.sibling = sibling
        self.width=width
        self.height=height	
        self.txtBox(word)
        print(self.txt.grid_info())
    def txtBox(self,word):
        self.word = word.strip("\r\n") 
        nlines = word.count('\n')
        nlines = (nlines * 25)+25
        nWidth = word.split("\n")
        maxLineLength = findMaxLine(nWidth)
        self.txt = AutoResizedText(self.master, family="Arial",size=8, width = maxLineLength , height = nlines,background = "black",foreground = "white") #how to make int go by characters or something similar
        self.txt.grid(row = self.height, column = self.width,columnspan=2)
        self.txt._fit_to_size_of_text(word)
        self.txt.bind("<Shift-Insert>",self.deleteSelf)
        self.txt.bind('<Shift-Up>',self.moveUp)
        self.txt.bind('<Shift-Down>',self.insertSibling)
        self.txt.bind('<Shift-Right>',self.insertChild)
    def insertText(self):#insert word into Text
        self.txt = tk.AutoResizedText(self.master, family="Arial",size=12, width = maxLineLength , height = nlines,background = "gray40")
        self.txt.grid(row = self.height, column = self.width)

    def moveUp(self,cow):
        if(self.parent):
            self.parent.txt.focus()
    	
    def moveDown(self):
        curr = self
        while curr.parent is not None:
            curr = curr.parent
        sortButtons(curr,0,0)

    def insertSibling(self,cow):
        if(self.sibling):
            #self=self.sibling
            print("sibling")
            self.sibling.txt.focus()
            return
        bob = object(self.master,self.height+1,self.width,parent = self)
        self.sibling = bob
        mainCanvas.yview_scroll(100, "units")
        sortButtons(head,0,0)
    def insertChild(self,cow):
        if (self.child):
            print("I llove my child")
            self.child.txt.focus() 
            return
        nextNode = object(self.master,self.height+1,self.width+1,parent = self)
        self.child = nextNode
        sortButtons(head,0,0)#what's the purpose of this? Well looks through all the buttons EVERY SINGLE ONE. Determines the num of descendents then can you  you know.
		
    def deleteSelf(self,cow):#deletes itself as well as all descendents of self
        deleteThis = []
        findParent = self
        curr = self
        self.txt.destroy()
# a bug we have is that the roots sibling cannot be deleted if it has children. Why is this the case? Because it's relation
# to the root is different than normel. So what needs to happen when we delete the node?
	
        if(self.child is not None):#here we are seeing if it has children so we can delete it and the rest of it's descendents using dfs
            deleteThis.append(self.child)
        self.parent.child = None

        if(self.sibling is not None):#here we replace the link between the parent and the self with either none or it's sibling.
            self.parent.child = self.sibling
        else:		
            self.parent.sibling =None
        while deleteThis:
            curr = deleteThis.pop(0)
            curr.txt.destroy()
            if(curr.child is not None):
                deleteThis.append(curr.child)
            if(curr.sibling is not None):
                deleteThis.append(curr.sibling)
            curr = None # DELETES REFERENCE To child
            sortButtons(head,0,0)
    def bob(self,cow):
        print("bob")
        print(self.child.txt)
        self.child.txt.focus_set()
        self = self.child
	

def insertNode(height,width):#inserts node into correct spot on tree given height and width
    global head
    #bfs search
    stack.append(head)
    while stack:
        curr = stack.pop(0) 

        if((curr.child is not None) and (curr.child.height <=height) and (curr.child.width <=width)):
            stack.append(curr.child)
        if((curr.sibling is not None) and (curr.sibling.height <=height) and (curr.sibling.width <=width)):
            stack.append(curr.sibling)

def ancestor(curr,width):#traverses up until curr.width = width
    while(curr.width !=width):
        curr = curr.parent
    return curr


			# else: # if the next node not a direct family member of curr
	# printLinked(head)
				
		#we need to determine if it's a child, a sibling, or someone elses direct family.
def traverse(curr,diction):#sorts in preorder
	# if((curr.child is None) and (curr.sibling is None) and (curr is not None)):#deals with the end of a tree branch
	# 	diction.append({"height": curr.height,"width": curr.width, "word": curr.word})
    if(curr.child is not None):
        word= curr.child.txt.get("1.0",tk.END)
        diction.append({"height": curr.child.height,"width": curr.child.width, "word": word.strip("\r\n")})
        traverse(curr.child,diction)
    if(curr.sibling is not None):
        word= curr.sibling.txt.get("1.0",tk.END)
        diction.append({"height": curr.sibling.height,"width": curr.sibling.width, "word": word.strip("\r\n")})
        traverse(curr.sibling,diction)
    return diction
	
def sortButtons(curr,height,width):#this sorts out bobs starting from curr(usually head)
	if curr.child is not None:
		sortButtons(curr.child,height+1,width+1)#for each bob created from this child temp will increase by
	if curr.sibling is not None:
		temp1=countChildren(curr)+1
		sortButtons(curr.sibling,height+temp1,width)

	curr.height = height
	curr.width = width
	curr.txt.grid_configure(row = height, column = width)


def conversion(converting):#this method converts string to int, or int to string
    try:
	#if it is a string with a number it will run this, changing it to an int
        converted = converting + ""
        converted = int(converting)
    except :# if it is a int, it'll convert to a string
        converted = str(converting)
    return converted

def findMaxLine(myList):
    try:
        for x in range(1,len(myList)):
            if myList[0] < myList[x]:
                myList[0] = myList[x]
        return int(myList[0])
    except ValueError:
        return 100

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def _on_mousewheel(event):
    mainCanvas.yview_scroll(-1*(int)(event.delta/40), "units")

def initializeScollbar(master):
    mainCanvas.grid(row = 1,column = 0,sticky = "ew")
    mainCanvas.bind_all("<MouseWheel>", _on_mousewheel)
    vsb.grid(column = 1,row = 1,sticky = "news")	
    hsb.grid(column=0,row = 2,sticky = "ew")
    vsb.rowconfigure(0, weight=1)
    hsb.columnconfigure(0, weight=1)
    mainCanvas.configure(yscrollcommand=vsb.set,xscrollcommand = hsb.set,height = master.winfo_screenheight()-120,width = master.winfo_screenwidth()-20,yscrollincrement = '2',xscrollincrement = '2')	
    mainCanvas.create_window((12,12), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=mainCanvas: onFrameConfigure(mainCanvas))
	# mainCanvas.configure(yscrollincrement='2')
	
def moveFocus(curr):
    curr.txt.focus_set()

def printLinked(head):
    print(str(head.height) + " " + str(head.width) + " " + head.word)
    if head.child is not None:
        printLinked(head.child)
    if head.sibling is not None:
        printLinked(head.sibling)

def countChildren(curr):#counts number of descendents 
	count = 0
	stack = []
	if curr.child is not None:
		count+=1
		stack.append(curr.child)
	while stack:#uses dfs
		noder = stack.pop(0)
		if noder.child is not None:
			stack.append(noder.child)
			count+=1
		if noder.sibling is not None:
			stack.append(noder.sibling)
			count+=1
	return count

def NodeExists(height,width,start,Frame):#searches if the Node exists within the tree
    curr = start
    stack  = []
    while curr:
        if(curr.height == height) and (curr.width == width):
            return curr
        if curr.child is not None:
            stack.append(curr.child)
        if curr.sibling is not None:
            stack.append(curr.sibling)
    return object(Frame,self.height+1,self.width+1,parent = self)



# @@@@@@@@@@@@@@@@@ THIS IS WHERE MENU METHODS START@@@@@@@@@@@@@@@@


def initializeBorderButtons(master,frame):
    menu = tk.Menu(master)
    master.config(menu = menu) 

    subMenu = tk.Menu(menu,tearoff = 0) # creating a menu item within the menu
    transparentMenu = tk.Menu(menu,tearoff = 0)

    menu.add_cascade(label = "Edit", menu = subMenu) #Name of drop down menu
    menu.add_cascade(label = "Transparancy",  menu = transparentMenu)

    subMenu.add_command(label = "save", command = save)
    subMenu.add_command(label = "Open", command = lambda: openTheFile(frame))
    subMenu.add_separator()
    subMenu.add_command(label = "Exit", command =lambda: sys.exit(1))

    transparentMenu.add_command(label = "30%",command = lambda: changeRootTransparency(master,0.3))
    transparentMenu.add_command(label = "50%",command =lambda: changeRootTransparency(master,0.5) )
    transparentMenu.add_command(label = "60%",command = lambda: changeRootTransparency(master,0.6))
    transparentMenu.add_command(label = "70%",command = lambda: changeRootTransparency(master,0.7))
    transparentMenu.add_command(label = "80%",command = lambda: changeRootTransparency(master,0.8))
    transparentMenu.add_command(label = "100%",command = lambda: changeRootTransparency(master,1.0))
	
def changeRootTransparency(master,percentage):
    root.attributes("-alpha",percentage)

def save():
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    global head
    copyOfT = copy.copy(head)#copies the entire tree onto copyOfT
    curr = copyOfT
    diction = {}
    diction["bob"]= []
    curr.word = head.txt.get("1.0",tk.END)
    diction["bob"].append({"height": curr.height,"width": curr.width, "word": curr.word.strip("\r\n")})
    hold = traverse(curr,diction["bob"])
    json.dump(hold,file,indent = 4)
    file.close()	

def openTheFile(master):
	filePath =  filedialog.askopenfilename()
	if filePath == '':
		return
	with open(filePath) as json_file:  
		data = json.load(json_file)
		global head
		head = object(master,data[0]["height"],data[0]["width"],data[0]["word"])
		curr = head
		descendentCounter = 0
		for index in range(1,len(data)):
			if((curr.height+1 == data[index]["height"]) and (curr.width+1==data[index]["width"])):#if the next node is a child to curr
				bob = object(master,data[index]["height"],data[index]["width"],data[index]["word"],parent = curr)
				curr.child = bob
				curr = curr.child
				print("child found")
			elif(curr.width+1 != data[index]["width"]):#it's a sibling to someone therefore width between curr and next node are the same
				curr = ancestor(curr,data[index]["width"])
				bob = object(master,data[index]["height"],data[index]["width"],data[index]["word"],parent = curr)
				bob.parent.sibling = bob
				curr = curr.sibling
				print("sibling found")
			else:
				print("ERROR IN   " + str(data[index]["height"]) + " " + str(data[index]["width"]) +" " + str(data[index]["word"]) )

# @@@@@@@@@@@@@@@@@ THIS IS WHERE MENU METHODS END@@@@@@@@@@@@@@@@
def createToolBar(master):
    toolbar = tk.Frame(master, bg = "yellow")
    insertButt= tk.Button(toolbar,text="button")
    insertButt.pack(side = tk.LEFT)
    toolbar.grid(row=0,column=0)
######METHOD
root = tk.Tk() 
root.geometry('%sx%s' % (root.winfo_screenwidth(),root.winfo_screenwidth()))

mainCanvas = tk.Canvas(root, background = 'black')
# onFrameConfigure(mainCanvas)# my guess is that rather than using "All", we look for the location of where our widget currently is
frame = tk.Frame(mainCanvas, background="black")

vsb = tk.Scrollbar(root, orient="vertical",command=mainCanvas.yview)
hsb = tk.Scrollbar(root, orient="horizontal",command=mainCanvas.xview)
mainCanvas.configure(scrollregion=mainCanvas.bbox("all"))
root.attributes("-alpha",0.8)
createToolBar(root)
initializeScollbar(root)
head  = object(frame,0,0)

initializeBorderButtons(root,frame)
# addOpenFile(frame,head)
root.mainloop()
