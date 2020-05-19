import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from mutagen.mp3 import MP3
from pygame import mixer

window = Tk()  # Creates a window


mixer.init()

menubar = Menu(window)
window.config(menu=menubar)

submenu = Menu(menubar, tearoff=0)


def browse_file():
    global filename
    filename = filedialog.askopenfilename()


menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=window.destroy)


def show_details():
    file_label['text'] = "Playing " + os.path.basename(filename)

    file_data = os.path.splitext(filename)

    if file_data[1] == '.mp3':
        audio = MP3(filename)
        total_length = audio.info.length
    else:
        a = mixer.Sound(filename)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = '{:02d}:{:02d}'.format(mins, secs)
    time_label['text'] = "Total time: {}".format(time_format)

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): Returns FALSE when we press the stop button (music stop playing)
    ct = 0  # ct stands for current time
    while ct <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(ct, 60)
            mins = round(mins)
            secs = round(secs)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            current_label['text'] = "Current time: {}".format(time_format)
            time.sleep(1)
            ct += 1


def play_btn():
    global paused, stopped

    if paused:
        mixer.music.unpause()
        statusBar['text'] = "Music Resumed"
        paused = FALSE
    elif stopped:
        mixer.music.play()
        statusBar['text'] = "Playing Music" + ' - ' + os.path.basename(filename)
        stopped = FALSE
    else:
        try:
            mixer.music.load(filename)
            mixer.music.play()
            statusBar['text'] = "Playing Music" + ' - ' + os.path.basename(filename)
            show_details()
        except:
            tkinter.messagebox.showerror('File not found', 'Please select the music first to make me play')


stopped = FALSE


def stop_btn():
    global stopped
    mixer.music.stop()
    statusBar['text'] = "Music Stopped"
    stopped = TRUE


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


window.title("Music Player")
window.iconbitmap(r'')  # r stands for Random String
window.geometry('400x400')

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=about_us)

file_label = Label(window, text="Let's make some noise!")
file_label.pack()  # pack the label so that it could be appear in the window.

time_label = Label(window, text="Total Time: --:--")
time_label.pack()

current_label = Label(window, text="Current Time: --:--", relief=GROOVE)
current_label.pack()


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


def on_closing():
    stop_btn()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()  # Displays the window
