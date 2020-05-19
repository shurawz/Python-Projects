import os
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from pygame import mixer

mixer.init()


def browse_file():
    global filename
    filename = filedialog.askopenfile()


def play_btn():
    try:
        paused
    except NameError:
        try:
            mixer.music.load('Laakhau Hajarau.mp3')
            mixer.music.play()
            statusBar['text'] = "Playing Music" + ' - ' + os.path.basename('Laakhau Hajarau.mp3')
        except:
            tkinter.messagebox.showerror('File not found', 'Please select the music first to make me play')
    else:
        mixer.music.unpause()
        statusBar['text'] = "Music Resumed"


def stop_btn():
    mixer.music.stop()
    statusBar['text'] = "Music Stopped"


def pause_btn():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text'] = "Music Paused"


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)


def about_us():
    tkinter.messagebox.showinfo('About Us', 'This is the simple Media Player using Python Tkinter made by @surajgotamey')


window = Tk()  # Creates a window
window.title("Music Player")
window.iconbitmap(r'Photos\MPicon.ico')  # r stands for Random String
window.geometry('400x400')

menubar = Menu(window)
window.config(menu=menubar)

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=window.destroy)

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=about_us)

text = Label(window, text="Let's make some noise!")
text.pack()  # pack the label so that it could be appear in the window.

photo = PhotoImage(file='Photos\play.png')
playButton = Button(window, image=photo, command=play_btn)
playButton.pack()

photo1 = PhotoImage(file='Photos\stop.png')
stopButton = Button(window, image=photo1, command=stop_btn)
stopButton.pack()

photo2 = PhotoImage(file='Photos\pause.png')
pauseButton = Button(window, image=photo2, command=pause_btn)
pauseButton.pack()


vol_scale = Scale(window, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
vol_scale.set(4)
set_vol(4)
vol_scale.pack()

statusBar = Label(window, text="Welcome to My Music Player", relief=SUNKEN, anchor=W)
statusBar.pack(side=BOTTOM, fill=X)

window.mainloop()  # Displays the window


