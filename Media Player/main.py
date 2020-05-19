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
    global paused

    if paused:
        mixer.music.unpause()
        statusBar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            mixer.music.load('Laakhau Hajarau.mp3')
            mixer.music.play()
            statusBar['text'] = "Playing Music" + ' - ' + os.path.basename('Laakhau Hajarau.mp3')
        except:
            tkinter.messagebox.showerror('File not found', 'Please select the music first to make me play')


def stop_btn():
    mixer.music.stop()
    statusBar['text'] = "Music Stopped"


paused = FALSE


def pause_btn():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text'] = "Music Paused"


def set_vol(val):
    # global volume
    volume = int(val) / 100
    new_volume = mixer.music.set_volume(volume)
    return new_volume


def rewind_btn():
    play_btn()
    statusBar['text'] = "Music Rewinded"


muted = FALSE


def mute_btn():
    global muted
    if muted:
        volume_button.configure(image=photo5)
        set_vol(0.04)
        vol_scale.set(4)
        muted = FALSE

    else:
        volume_button.configure(image=photo4)
        set_vol(0)
        vol_scale.set(0)
        muted = TRUE


def about_us():
    tkinter.messagebox.showinfo('About Us', 'This is the simple Media Player using Python Tkinter made by @surajgotamey')


window = Tk()  # Creates a window
window.title("Music Player")
window.iconbitmap(r'')  # r stands for Random String
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

mFrame = Frame(window)
mFrame.pack(padx=10, pady=10)

photo = PhotoImage(file='Photos/play.png')
playButton = Button(mFrame, image=photo, command=play_btn)
playButton.grid(row=0, column=0, padx=10)

photo1 = PhotoImage(file='Photos/stop.png')
stopButton = Button(mFrame, image=photo1, command=stop_btn)
stopButton.grid(row=0, column=1, padx=10)

photo2 = PhotoImage(file='Photos/pause.png')
pauseButton = Button(mFrame, image=photo2, command=pause_btn)
pauseButton.grid(row=0, column=2, padx=10)

bFrame = Frame(window)
bFrame.pack(padx=10, pady=10)

photo3 = PhotoImage(file='Photos/playagain.png')
rewindButton = Button(bFrame, image=photo3, command=rewind_btn)
rewindButton.grid(row=0, column=0, padx=20)

photo4 = PhotoImage(file='Photos/mute.png')
# muteButton = Button(bFrame, image=photo4, command=rewind_btn)
# muteButton.grid(row=0, column=0)

photo5 = PhotoImage(file='Photos/loud.png')
volume_button = Button(bFrame, image=photo5, command=mute_btn)
volume_button.grid(row=0, column=1)

vol_scale = Scale(bFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
vol_scale.set(4)
set_vol(4)
vol_scale.grid(row=0, column=2)

statusBar = Label(window, text="Welcome to My Music Player", relief=SUNKEN, anchor=W)
statusBar.pack(side=BOTTOM, fill=X)

window.mainloop()  # Displays the window
