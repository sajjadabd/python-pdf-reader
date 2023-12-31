import glob
import glob

import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
from tkinter.simpledialog import askstring
from tkinter import font

import tkinter.font as fnt

from ttkthemes import ThemedStyle

from tkinterdnd2 import DND_FILES, TkinterDnD

import os

import natsort

import vlc

import subprocess

import numpy as np


import cv2

import datetime


result = []
backUpResult = []
path = ''



class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth(), master.winfo_screenheight()))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
        
        
        

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder='', cnf={}, fg='black',
                 fg_placeholder='grey50', *args, **kw):
        super().__init__(master=None, cnf={}, bg='white', *args, **kw)
        self.fg = fg
        self.fg_placeholder = fg_placeholder
        self.placeholder = placeholder
        self.bind('<FocusOut>', lambda event: self.fill_placeholder())
        self.bind('<FocusIn>', lambda event: self.clear_box())
        self.fill_placeholder()

    def clear_box(self):
        if not self.get() and super().get():
            self.config(fg=self.fg)
            self.delete(0, tk.END)

    def fill_placeholder(self):
        if not super().get():
            self.config(fg=self.fg_placeholder)
            self.insert(0, self.placeholder)
    
    def get(self):
        content = super().get()
        if content == self.placeholder:
            return ''
        return content

# create root window
root = TkinterDnD.Tk()


#root = ThemedTk(theme="awdark")
root.title('Playlist Manager')
#root.geometry('500x400')
padx = -6
pady = -5


#titlebar_height = root.winfo_rooty() - root.winfo_y()
#root.geometry( '{0}x{1}+{2}+{3}'.format( str( root.winfo_screenwidth() ) , str( root.winfo_screenheight()  - titlebar_height * 2 ) , padx , pady  ) )
#root.state('zoomed')

#print("titlebar_height : " , titlebar_height) 


# configure the grid layout
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


themeIndex = 1





hightlightBackgroundColors = [
    '#2C001E' ,
    '#212529' ,
    '#354f52' ,
    '#0d1b2a' , 
    '#2e1129' ,
    '#03071e' ,
    '#370617' ,
    '#590d22' ,
    '#10002b' ,
    '#212529' ,
    '#582f0e' ,
    '#081c15' ,
    '#0d1321' ,
    '#2e1129' ,
]


backgroundColors = [ 
    '#5E2750' , 
    '#495057' ,
    '#52796f' ,
    '#1b263b' ,
    '#502a4b' ,
    '#370617' ,
    '#6a040f' ,
    '#800f2f' ,
    '#240046' ,
    '#343a40' ,
    '#7f4f24' ,
    '#1b4332' ,
    '#1d2d44' ,
    '#502a4b' ,
]



selectedForegroundColors = [
    '#ffb703' ,
    '#fca311' ,
    '#ffb703' ,
    '#ffb703' ,
    '#fca311' ,
    '#ffb703' ,
    '#ffb703' ,
    '#fca311' ,
    '#ffb703' ,
    '#ffb703' ,
    '#fca311' ,
    '#ffb703' ,
    '#ffb703' ,
    '#fca311' ,
]

foregroundColors = [ 
    '#e9edc9' , 
    '#cad2c5' ,
    '#e9edc9' ,
    '#e9edc9' , 
    '#cad2c5' ,
    '#e9edc9' ,
    '#e9edc9' , 
    '#cad2c5' ,
    '#e9edc9' ,
    '#e9edc9' , 
    '#cad2c5' ,
    '#e9edc9' ,
    '#e9edc9' , 
    '#cad2c5' ,
]


lovedEmojies = "♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥"

fontSize = 16
rowHeight = fontSize * 2
font_properties = ( "ubuntu", fontSize )

#style = ttk.Style()

style = ThemedStyle(root)
style.set_theme("black")   

    
    
    

#print(style.theme_names())

style.configure("Treeview", font=font_properties )
style.configure('Treeview', rowheight=rowHeight)

#style.map('Treeview',  background=backgroundColors[1] , foreground=foregroundColors[1])


#style.theme_use("aqua")


#style.map('Treeview',  background=[('selected', 'invalid' , '#264653')] , foreground=[('selected', 'invalid' , '#ffb703')])
style.map('Treeview',  background=[('selected', 'invalid' , '#264653')] , foreground=[('selected' , selectedForegroundColors[themeIndex])])
#('aqua', 'step', 'clam', 'alt', 'default', 'classic')

topFrame = ttk.Frame(root)

# create a treeview
tree = ttk.Treeview( root , show="tree")

vsby = ttk.Scrollbar( root , orient="vertical" ,command=tree.yview)
#vsbx = ttk.Scrollbar( root , orient="horizontal",command=tree.xview)


vsby.pack( side=tkinter.RIGHT , fill='both' )
#vsbx.pack( side=tkinter.TOP , fill='both' )


tree.configure(yscrollcommand=vsby.set)
#tree.configure(xscrollcommand=vsbx.set)



selection_index = None


def on_tree_row_click(event):
    global selection_index
    # Get the index of the clicked row
    try :
        item = tree.identify_row(event.y)
        selection_index = int(item)
    except :
        pass




def HighLightRow(event):
    global tree 
    global till
    global themeIndex

    item = tree.selection()
    index = int(item[0])
    
    addIfNotInTill(index)
    saveWatchedVideos()
    
    tree.tag_configure( index , background =hightlightBackgroundColors[themeIndex] , foreground =foregroundColors[themeIndex] )




def DeHightLightRow(event):
    global tree 
    global till
    global themeIndex

    item = tree.selection()
    index = int(item[0])
    
    removeIfInTill(index)
    saveWatchedVideos()
    
    tree.tag_configure( index , background =backgroundColors[themeIndex] , foreground =foregroundColors[themeIndex] )





def printNode(event) :
    global tree
    global till
    global themeIndex
    
    counter = 0
    while counter < len(till) :
        print(tree.item(counter)["text"])
        #tree.tag_configure( till[counter]  ,  background =hightlightBackgroundColors[themeIndex] , foreground =foregroundColors[themeIndex] )
        counter += 1



def Love(event):
    global tree 
    global till
    global themeIndex
    global lovedEmojies

    item = tree.selection()
    index = int(item[0])
    
    #addIfNotInTill(index)
    addIfNotInLove(index)
    saveLovedVideos()
    
    #print(tree.item(index)["text"] + " " + lovedEmojies)
    
    if lovedEmojies not in tree.item(index)["text"] : 
        tree.item( index , text=tree.item(index)["text"] + " " + lovedEmojies  )







def UnLove(event):
    global tree 
    global till
    global themeIndex

    item = tree.selection()
    index = int(item[0])
    
    #removeIfInTill(index)
    removeIfInLove(index)
    saveLovedVideos()
    
    tree.item( index , text=tree.item(index)["text"].replace(lovedEmojies , '' ))







till = []


def addIfNotInTill(index) :
    global till
    found = False
    for item in till:
        if index == item :
            found = True
    
    if (found == False) :
        till.append(index)


def removeIfInTill(index) :
    global till
    found = False
    counter = 0
    while counter < len(till) :
        if index == till[counter] :
            till.remove(index)
            break
        counter += 1
    


def saveWatchedVideos() :
    global path
    global till
    
    lengthOfTill = len(till)
    f = open( path.replace("/" , "\\") + "\\saved.txt" , "w")
    
    counter = 0
    while counter < len(till) :
        f.write( str(till[counter]) + "\n" )
        counter += 1
    
    f.close()





love = []


def addIfNotInLove(index) :
    global love
    found = False
    for item in love:
        if index == item :
            found = True
    
    if (found == False) :
        love.append(index)


def removeIfInLove(index) :
    global love
    found = False
    counter = 0
    while counter < len(love) :
        if index == love[counter] :
            love.remove(index)
            break
        counter += 1


def saveLovedVideos() :
    global path
    global love
    
    lengthOfTill = len(love)
    f = open( path.replace("/" , "\\") + "\\loved.txt" , "w")
    
    counter = 0
    while counter < len(love) :
        f.write( str(love[counter]) + "\n" )
        counter += 1
    
    f.close()



def OnDoubleClick(event):
    global searchString
    global result
    global filteredResult
    global backUpResult
    global tree 
    global till
    global themeIndex

    result = backUpResult
    
    try :

        item = tree.selection()
        #print(item)
        index = int(item[0])
        
        
        addIfNotInTill(index)
        saveWatchedVideos()
        
        
        tree.tag_configure( index , background =hightlightBackgroundColors[themeIndex] , foreground =foregroundColors[themeIndex] )
        #print(index)
        #searchString = index
        #path = searchTheTable()
        #path = path[0].replace("/" , "\\")
        path = result[index].replace("/" , "\\")
        #print(path)
        
        
        subprocess.Popen(f"SumatraPDF -view \"single page\" -zoom \"fit page\" -bg-color #1c1a1b -set-color-range #242222 #cfcccc  \"{path}\"")
        
        """
        #bdbdbd
        #b5b5b5
        #cfcccc
        #242222 
        #bdbdbd 
        """
        """
        if player_index == 0 :
            subprocess.Popen(f"vlc \"{path}\"")
        elif player_index == 1 :
            subprocess.Popen(f"gom \"{path}\"")
        elif player_index == 2 : 
            subprocess.Popen(f"PotPlayerMini64 \"{path}\"")
        elif player_index == 3 : 
            subprocess.Popen(f"mpv \"{path}\"")
        elif player_index == 4 : 
            subprocess.Popen(f"KMPlayer64 \"{path}\"")
        """ 
    except : 
        pass
    #vlc_instance = vlc.Instance()
    # creating a media player
    #player = vlc_instance.media_player_new()
    # creating a media
    #media = vlc_instance.media_new(path)
    # setting media to the player
    #player.set_media(media)
    # play the video
    #player.play()
    
    #print("you clicked on", tree.item(i, "values"))


"""
backgroundColors = [ 'blue' , 'black' , 
    '#03045e' , 
    '#023e8a' , 
    '#0077b6' , 
    '#0096c7' ,
    '#00b4d8' ,
    '#48cae4' ,
    '#90e0ef' ,
    '#ade8f4' ,
    ]
"""




def checkToSeeIfThereIsParents(parentArray , theIndex , currentIndex , parrantIndex) :
    global result
    global tree
    global backgroundColors
    global foregroundColors
    global themeIndex
    
    if ( currentIndex == 0 ) :
        return
    else :
        #print('try : ' , f'{parentArray[parrantIndex]}' , parentArray[currentIndex] , currentIndex , parrantIndex )
        checkToSeeIfThereIsParents(parentArray , theIndex - 1 , currentIndex - 1 , parrantIndex - 1 )
        tree.insert( parentArray[parrantIndex], tk.END, iid = parentArray[currentIndex] , text=parentArray[currentIndex], open=False , tags = (currentIndex) )
        tree.tag_configure( theIndex-1 , background =backgroundColors[themeIndex] , foreground = foregroundColors[theIndex-1])
        
    """
    try :
        print('try : ' , f'{parentArray[parrantIndex]}' , parentArray[currentIndex] , currentIndex , parrantIndex )
        if ( currentIndex == 0 ) :
            return
        else :
            tree.insert( parentArray[parrantIndex], tk.END, iid = parentArray[currentIndex] , text=parentArray[currentIndex], open=False , tags = (currentIndex) )
            tree.tag_configure( theIndex-1 , background = backgroundColors[theIndex-1] , foreground = foregroundColors[theIndex-1])
    except : 
        #tree.insert(parentArray[theIndex-1-2], tk.END, iid = parentArray[len(parentArray)-1-1] , text=parentArray[theIndex-1-1], open=False , tags = (theIndex) )
        #counter-=1
        print('error : ' , parentArray[parrantIndex] , parentArray[currentIndex] , currentIndex , parrantIndex )
        if ( currentIndex == 0 ) :
            return
        else :
            checkToSeeIfThereIsParents(parentArray , theIndex - 1 , currentIndex - 1 , parrantIndex - 1 )
    """

def add_data() :
    global result
    global path
    global tree
    global backgroundColors
    global foregroundColors
    global selection_index
    global themeIndex
    global video_duration_array
    global reversePlaylist
    global numbering

    length = len(result)

    for i in tree.get_children():
        tree.delete(i)


    """
    tree.insert('', 'end', 'item1',text ='GeeksforGeeks')
 
    # Inserting child
    tree.insert('', 'end', 'item2',text ='Computer Science')
    tree.insert('', 'end', 'item3',text ='GATE papers')
    tree.insert('', 'end', 'item4',text ='Programming Languages')

    # Inserting more than one attribute of an item
    tree.insert('item2', 'end', 'Algorithm',text ='Algorithm') 
    tree.insert('item2', 'end', 'Data structure',text ='Data structure')
    tree.insert('item3', 'end', '2018 paper',text ='2018 paper') 
    tree.insert('item3', 'end', '2019 paper',text ='2019 paper')
    tree.insert('item4', 'end', 'Python',text ='Python')
    tree.insert('item4', 'end', 'Java',text ='Java')

    # Placing each child items in parent widget
    tree.move('item2', 'item1', 'end')
    tree.move('item3', 'item1', 'end')
    tree.move('item4', 'item1', 'end')
    """
    

    counter = 0
    while counter < length :
    
        if reversePlaylist == False :
            thePath = result[counter].replace( path , '' )
            precedence = '0' * ( abs(len(str(counter+1)) - len(str(len(result)))) )
        else : 
            thePath = result[length-counter-1].replace( path , '' )
            precedence = '0' * ( abs(len(str(length-counter-1+1)) - len(str(len(result)))) )
        
        parentArray = thePath.split('\\')
        theIndex = len(parentArray)
        currentIndex = theIndex - 1
        parrantIndex = theIndex - 1 - 1
        #print(result[counter])
        
        
        
        if treeCompleteString == True : 
            pass 
        else : 
            arr = np.array(parentArray)
            arr = arr[2:len(arr)]
            thePath = " \\ ".join(arr)
        
        #print(thePath)
        
        if reversePlaylist == False :
            if os.path.isfile(result[counter]) :
                if numbering == True :
                    eachTextString = precedence + str(counter+1) + thePath[-4:]
                    # + " - " + thePath[1:]
                else :
                    eachTextString = thePath[1:]
                tree.insert('', tk.END, text=eachTextString.replace( "\\" , "  \\  " ) , iid=counter, open=False , tags = counter )
                tree.tag_configure( counter , background =backgroundColors[themeIndex] , foreground =foregroundColors[themeIndex] )
        else : 
            if os.path.isfile(result[length-counter-1]) :
                if numbering == True :
                    eachTextString = precedence + str(length-counter-1+1) + thePath[-4:]
                    # + " - " + thePath[1:]
                else :
                    eachTextString = thePath[1:]
                tree.insert('', tk.END, text=eachTextString.replace( "\\" , "  \\  " ) , iid=length-counter-1, open=False , tags = length-counter-1 )
                tree.tag_configure( length-counter-1 , background =backgroundColors[themeIndex] , foreground =foregroundColors[themeIndex] )
        #checkToSeeIfThereIsParents(parentArray , theIndex , currentIndex , parrantIndex)
        counter += 1
    
    style.map('Treeview',  background=[('selected', 'invalid' , '#264653')] , foreground=[('selected' , selectedForegroundColors[themeIndex])])
    
    if selection_index != None and selection_index < length :
        tree.selection_set(selection_index)
    # adding children of first node
    # tree.insert('', tk.END, text='John Doe', iid=5, open=False)
    # tree.insert('', tk.END, text='Jane Doe', iid=6, open=False)
    # tree.move(5, 0, 0)
    # tree.move(6, 0, 1)













def get_length(filename):
    video_time = '----'
    try :
        video = cv2.VideoCapture(filename)

        #duration = video.get(cv2.CAP_PROP_POS_MSEC)
        #frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

        # count the number of frames
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)
          
        # calculate duration of the video
        seconds = round(frames / fps)
        video_time = datetime.timedelta(seconds=seconds)
    except : 
        pass
    
    return video_time
    



video_duration_array = []




def fetchAllFilesFromPath(calculateVideoDuration = True) :
    global search
    global result
    global path
    global backUpResult
    global video_duration_array
    
    
    

    #print(path)

    if( path.strip() == '') :
        return

    search.delete(0,tkinter.END)
    result = glob.glob(path + '/**/*.pdf', recursive=True)
    
    result = natsort.natsorted(result)
    
    """
    if calculateVideoDuration == True : 
        video_duration_array = []
        for item in result :
            video_length = get_length(item)
            video_duration_array.append(video_length)
        #print(video_length)
    """
    
    
    add_data()
    highlightWatchedVideos()
    ShowLovedVideos()
    backUpResult = result
    label.config(text=(path + f" ({len(result)} files)"))
    
    tree.focus(selection_index)







untill = ''




def fetchSavedHistory() : 
    global untill
    global path
    global till
    
    till = []
    #print(path.replace("/" , "\\") + "\\saved.txt")
    try :
        f = open( path.replace("/" , "\\") + "\\saved.txt" , "r")
        #line = f.readline()
        for line in f:
            # All lines and strip last line which is newline
            till.append(int(line.strip()))
        f.close()
    except :
        pass





def fetchLovedHistory() : 
    global untill
    global path
    global love
    
    love = []
    #print(path.replace("/" , "\\") + "\\loved.txt")
    try :
        f = open( path.replace("/" , "\\") + "\\loved.txt" , "r")
        #line = f.readline()
        for line in f:
            # All lines and strip last line which is newline
            love.append(int(line.strip()))
        f.close()
    except :
        pass




def highlightWatchedVideos() :
    global tree
    global till
    global themeIndex
    
    counter = 0
    while counter < len(till) :
        tree.tag_configure( till[counter] , background =hightlightBackgroundColors[themeIndex] , foreground =foregroundColors[themeIndex] )
        counter += 1
                
            


def ShowLovedVideos() :
    global tree
    global love
    global themeIndex
    global lovedEmojies
    
    
    
    counter = 0
    while counter < len(love) :
        tree.item( love[counter] , text=tree.item(love[counter])["text"] + " " + lovedEmojies  )
        counter += 1
                


    



def openfile():
    global result
    global path
    
    try :
        temp_path = filedialog.askdirectory()
        
        #print(f"#{path}#")
        if( temp_path.strip() == '' ) :
            pass
        else :
            path = temp_path
            #print(path)
            result = []
            fetchSavedHistory()
            fetchLovedHistory()
            fetchAllFilesFromPath()
            #return filedialog.askopenfilename()
    except : 
        pass
    


def sanitizeString(str) :
    for ch in ['{','}']:
        if ch in str:
            str = str.replace(ch,"")
    return str


def dropDirectory(e) :
    global result
    global path
    
    try : 
        path = sanitizeString(e.data)
        #print(path)
        result = []
        fetchSavedHistory()
        fetchLovedHistory()
        fetchAllFilesFromPath()
        #return filedialog.askopenfilename()
    except : 
        pass
    
    #messagebox.showinfo(f"information",f"{e.data}")
    


buttonFont = fnt.Font(family='ubuntu', size=36, weight='bold')

style.configure( 'my.TButton', font=font_properties , anchor='c' )
label = ttk.Label(topFrame , text='select folder to load directories ...' , font=font_properties )

label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', dropDirectory )

button = ttk.Button(topFrame , text = 'browse' , command=openfile , style='my.TButton'  )


#label.place( relx=0.5 , rely=0.5 )
#button.place( relx=0.5 , rely=0.5 )

label.pack( expand=True , fill='both'  , side=tkinter.LEFT , anchor=tkinter.NW)
button.pack( expand=False  , fill='none'  , side=tkinter.RIGHT  , anchor=tkinter.NE)

topFrame.pack( fill='both' )

sv = tkinter.StringVar()

searchString = ''


def searchTree():
    global searchString
    global tree
    query = searchString
    selections = []
    for child in tree.get_children():
        if query.lower() in tree.item(child)['text'].lower():   # compare strings in  lower cases.
            #print(tree.item(child)['text'])
            selections.append(child)
    #print(selections)
    tree.selection_set(selections)


def searchTheTable() :
    global result
    global filteredResult
    global searchString
    global path

    length = len(result)
    
    filteredResult = []
    counter = 0

    #print('----------------------------------')
    while counter < length : 
        #print(result[counter].find(searchString))
        if( (result[counter].replace(path , '').lower()).find(searchString.lower()) != -1 ) :
            #print(result[counter])
            filteredResult.append(result[counter])
        else :
            pass
        counter += 1
    #print('----------------------------------')
    

    #result = filteredResult
    return filteredResult




def return_pressed(event):
    global result
    global backUpResult
    global searchString

    if ( len(searchString) > len( str(search.get()) ) ) :
        result = backUpResult

    searchString = str(search.get())

    #print(searchString)

    if( searchString.strip() == '' ) :
        result = backUpResult
        add_data()
        return
    

    result = searchTheTable()

    #searchTree()
    
    #print(result)
    add_data()
     

#sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
#create search bar
search = ttk.Entry( root  , font=font_properties )
#search.bind('<Return>', return_pressed)
search.bind('<KeyRelease>', return_pressed)

search.pack(fill="both")


#tree.heading('#0', text='', anchor=tk.W)
#tree.bind("<Double-1>", OnDoubleClick)
tree.bind("<Double-1>", OnDoubleClick)
tree.bind("<Return>", OnDoubleClick)
tree.bind("<Button-1>", on_tree_row_click)


tree.bind("<A>", HighLightRow)
tree.bind("<a>", HighLightRow)
tree.bind("<R>", DeHightLightRow)
tree.bind("<r>", DeHightLightRow)

tree.bind("<L>", Love)
tree.bind("<l>", Love)

tree.bind("<X>", UnLove)
tree.bind("<x>", UnLove)



tree.bind("<p>", printNode)



def arrowUpKeyHandler(event) :
    global selection_index
    if selection_index > 0 :
        selection_index = selection_index - 1




def arrowDownKeyHandler(event) :
    global selection_index
    if selection_index < len(result) - 1 :
        selection_index = selection_index + 1
    

tree.bind("<Up>" , arrowUpKeyHandler)
tree.bind("<Down>" , arrowDownKeyHandler)



def changeFontSize( value ) :
    global fontSize
    global rowHeight
    
    fontSize += value
    rowHeight = (fontSize * 2) 
    font_properties = ( "ubuntu", fontSize )

    style.configure("Treeview", font=font_properties )
    style.configure('Treeview', rowheight=rowHeight)

def decreaseFontSize(event) :
    if event.keysym == "minus" :
        changeFontSize(-1)

def increaseFontSize(event) :
    changeFontSize(1)


root.bind("<KeyPress-+>" , increaseFontSize)
root.bind("<KeyPress-->" , decreaseFontSize)


def mousewheel(event) :
    global fontSize
    global rowHeight
    
    if event.delta > 0:
        changeFontSize(1)
    elif event.delta < 0:
        changeFontSize(-1)

root.bind("<Control-MouseWheel>", mousewheel)


# place the Searchbar widget on the root window
# search.grid(row=0, column=0 , sticky=tk.W , ipady = 2  )

# place the Treeview widget on the root window
#tree.grid(row=1, column=0, sticky=tk.NSEW )
#tree.pack( anchor=tk.NW , fill="y" , expand=True)
tree.pack( fill="both" , expand=True )


treeCompleteString = True


def toggle_check():
    global treeCompleteString
    # Get the current state of the checkbox
    treeCompleteString = check_var.get()
    fetchAllFilesFromPath(calculateVideoDuration = False)




reversePlaylist = False


def reverse_check() :
    global reversePlaylist 
    if reversePlaylist == True :
        reversePlaylist = False 
    else :
        reversePlaylist = True
    fetchAllFilesFromPath(calculateVideoDuration = False)



numbering = True 

def numbering_check() :
    global numbering
    if numbering == True :
        numbering = False 
    else :
        numbering = True
    fetchAllFilesFromPath(calculateVideoDuration = False)




menubar = tkinter.Menu(root)

menubar.configure(background=backgroundColors[1], foreground=foregroundColors[1])

root.config(menu=menubar)

file_menu = tkinter.Menu(menubar , tearoff=0)

#file_menu.configure(background=backgroundColors[1], foreground=foregroundColors[1])

file_menu.add_command(
    label='Exit',
    command=root.destroy,
)

options_menu = tkinter.Menu(menubar , tearoff=0)


#options_menu.configure(background=backgroundColors[1], foreground=foregroundColors[1])


numbering_var = tk.BooleanVar(value=True)  # Variable to store the checkbox state
options_menu.add_checkbutton(label="Numbering", variable=numbering_var, command=numbering_check)



reverse_var = tk.BooleanVar(value=False)  # Variable to store the checkbox state
options_menu.add_checkbutton(label="Reverse", variable=reverse_var, command=reverse_check)




options_menu.add_command(
    label='Refresh',
    command=fetchAllFilesFromPath(calculateVideoDuration = False),
)




def rewriteWatchedVideos(number) :
    global path
    
    
    f = open( path.replace("/" , "\\") + "\\saved.txt" , "w")
    
    counter = 0
    while counter < number :
        f.write( str(counter) + "\n" )
        counter += 1
    
    f.close()
    
    fetchSavedHistory()
    fetchAllFilesFromPath(calculateVideoDuration = False)




def syncWatchHistory() :
    try :
        number = askstring('Watch Untill', 'How Many Videos You Watched?')
        number = int(number)
        rewriteWatchedVideos(number)
    except :
        pass
    




options_menu.add_command(
    label='Sync Watch history',
    command=syncWatchHistory,
)



check_var = tk.BooleanVar(value=True)  # Variable to store the checkbox state
options_menu.add_checkbutton(label="Complete Path", variable=check_var, command=toggle_check)





player_index = 0



vlcplayer = tk.BooleanVar(value=True)
gomplayer = tk.BooleanVar(value=False)
potplayer = tk.BooleanVar(value=False)
mpvplayer = tk.BooleanVar(value=False)
kmpplayer = tk.BooleanVar(value=False)


playerNames = [ "vlc" , "gom" , "pot" , "mpv" , "kmp" ]
listOfplayers = [ vlcplayer , gomplayer , potplayer , mpvplayer , kmpplayer ]


def deSelectAllPlayers() :
    for item in listOfplayers : 
        item.set(False)


  
def applyPlayer(playerItemIndex) :
    global player_index
    deSelectAllPlayers()
    listOfplayers[playerItemIndex].set(True)
    player_index = playerItemIndex
    return

   



player_menu = tkinter.Menu(menubar , tearoff=0)

player_menu.add_checkbutton(label=playerNames[0] , variable=listOfplayers[0] , command=lambda:applyPlayer(0) )
player_menu.add_checkbutton(label=playerNames[1] , variable=listOfplayers[1] , command=lambda:applyPlayer(1) )
player_menu.add_checkbutton(label=playerNames[2] , variable=listOfplayers[2] , command=lambda:applyPlayer(2) )
player_menu.add_checkbutton(label=playerNames[3] , variable=listOfplayers[3] , command=lambda:applyPlayer(3) )
player_menu.add_checkbutton(label=playerNames[4] , variable=listOfplayers[4] , command=lambda:applyPlayer(4) )








theme_menu = tkinter.Menu(menubar , tearoff=0)

#theme_menu.configure(background=backgroundColors[1], foreground=foregroundColors[1])


firstTheme =  tk.BooleanVar(value=False)
secondTheme = tk.BooleanVar(value=True)
thirdTheme = tk.BooleanVar(value=False)
fourthTheme = tk.BooleanVar(value=False)
fifthTheme = tk.BooleanVar(value=False)
sixTheme = tk.BooleanVar(value=False)
sevenTheme = tk.BooleanVar(value=False)
eightTheme = tk.BooleanVar(value=False)
nineTheme = tk.BooleanVar(value=False)

themeNames = [ "one" , "two" , "three" , "four" , "five" , "six" , "seven" , "eight" , "nine" ]
listOfThemes = [ firstTheme , secondTheme , thirdTheme , fourthTheme , fifthTheme , sixTheme , sevenTheme , eightTheme , nineTheme ]


def deSelectAllTheme() :
    for item in listOfThemes :
        item.set(False)


def applyTheme(themeItemIndex) :
    global tree
    global themeIndex
    deSelectAllTheme()
    listOfThemes[themeItemIndex].set(True)
    themeIndex = themeItemIndex
    fetchAllFilesFromPath(calculateVideoDuration = False)
    tree.focus(selection_index)




theme_menu.add_checkbutton(label=themeNames[0] , variable=listOfThemes[0] , command=lambda:applyTheme(0) )
theme_menu.add_checkbutton(label=themeNames[1] , variable=listOfThemes[1] , command=lambda:applyTheme(1) )
theme_menu.add_checkbutton(label=themeNames[2] , variable=listOfThemes[2] , command=lambda:applyTheme(2) )
theme_menu.add_checkbutton(label=themeNames[3] , variable=listOfThemes[3] , command=lambda:applyTheme(3) )
theme_menu.add_checkbutton(label=themeNames[4] , variable=listOfThemes[4] , command=lambda:applyTheme(4) )
theme_menu.add_checkbutton(label=themeNames[5] , variable=listOfThemes[5] , command=lambda:applyTheme(5) )
theme_menu.add_checkbutton(label=themeNames[6] , variable=listOfThemes[6] , command=lambda:applyTheme(6) )
theme_menu.add_checkbutton(label=themeNames[7] , variable=listOfThemes[7] , command=lambda:applyTheme(7) )
theme_menu.add_checkbutton(label=themeNames[8] , variable=listOfThemes[8] , command=lambda:applyTheme(8) )


keyboardShortcutsMessage = """
    a -> add video to watched videos
    r -> remove video from watched videos
    l -> add video to loved videos
    x -> remove video from loved videos
    Enter -> play selected video
    """

def showKeyboardShortcuts() :
    showinfo(title="Keyboard Shortcuts", message=keyboardShortcutsMessage)



about_menu = tkinter.Menu(menubar , tearoff=0)


about_menu.add_command(
    label='Keyboard Shortcuts',
    command=showKeyboardShortcuts,
)






menubar.add_cascade(
    label="File",
    menu=file_menu,
)


menubar.add_cascade(
    label="Options",
    menu=options_menu,
)


menubar.add_cascade(
    label="Theme",
    menu=theme_menu,
)


menubar.add_cascade(
    label="Player",
    menu=player_menu,
)

menubar.add_cascade(
    label="About",
    menu=about_menu,
)

#app=FullScreenApp(root)
# run the app

#root.attributes("-fullscreen", True) 
root.mainloop()



