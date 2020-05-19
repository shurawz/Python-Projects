import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from tkinter import filedialog

from mutagen.mp3 import MP3
from pygame import mixer

# To know and use different themes of ttkthemes in tkinter, go and click the link below:
# https://www.github.com/RedFantom/ttkthemes/wiki/Usage

window = tk.ThemedTk()  # Creates a window
window.get_themes()
window.set_theme('breeze')

statusBar = Label(window, text="Welcome to My Music Player", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusBar.pack(side=BOTTOM, fill=X)

mixer.init()

menubar = Menu(window)
window.config(menu=menubar)

submenu = Menu(menubar, tearoff=0)


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


playlist = []

# playlist - contains the full path with filename
# playlistbox - contains only filename
# Full path + filename is required to play the music inside play_music load function


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    list_box1.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=window.destroy)


def show_details(play_music):
    # file_label['text'] = "Playing " + os.path.basename(filename)

    file_data = os.path.splitext(play_music)

    if file_data[1] == '.mp3':
        audio = MP3(play_music)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_music)
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


def stop_btn():
    mixer.music.stop()
    statusBar['text'] = "Music Stopped"


paused = FALSE


def pause_btn():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text'] = "Music Paused"


def play_btn():
    global paused

    if paused:
        mixer.music.unpause()
        statusBar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_btn()
            time.sleep(1)
            selected_song = list_box1.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusBar['text'] = "Playing Music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Please select the music first to make me play')


def set_vol(val):
    # global volume
    volume = float(val) / 100
    mixer.music.set_volume(volume)


def del_btn():
    selected_song = list_box1.curselection()
    selected_song = int(selected_song[0])
    list_box1.delete(selected_song)
    playlist.pop(selected_song)


def rewind_btn():
    play_btn()
    statusBar['text'] = "Music Rewinded"


muted = FALSE


def mute_btn():
    global muted
    if muted:
        volume_button.configure(image=photo5)
        set_vol(0.1)
        vol_scale.set(10)
        muted = FALSE

    else:
        volume_button.configure(image=photo4)
        set_vol(0)
        vol_scale.set(0)
        muted = TRUE


def about_us():
    tkinter.messagebox.showinfo('About Us', 'This is the simple Media Player using Python Tkinter made by '
                                            '@surajgotamey')


window.title("Music Player")
window.iconbitmap(r'Photos/MPicon.ico')  # r stands for Random String
# window.geometry('400x400')

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=about_us)

left_frame = Frame(window)
left_frame.pack(side=LEFT, padx=30, pady=20)

list_box1 = Listbox(left_frame)
list_box1.pack()

add = ttk.Button(left_frame, text="+ Add", command=browse_file)
add.pack(side=LEFT)
delete = ttk.Button(left_frame, text="- Del", command=del_btn)
delete.pack(side=LEFT)

right_frame = Frame(window)
right_frame.pack()

top_frame = Frame(right_frame)
top_frame.pack(pady=10)

time_label = ttk.Label(top_frame, text="Total Time: --:--")
time_label.pack()

current_label = ttk.Label(top_frame, text="Current Time: --:--", relief=GROOVE)
current_label.pack(pady=10)

mFrame = Frame(right_frame)
mFrame.pack(pady=30)

photo = PhotoImage(file='Photos/play.png')
playButton = ttk.Button(mFrame, image=photo, command=play_btn)
playButton.grid(row=0, column=0, padx=10)

photo1 = PhotoImage(file='Photos/stop.png')
stopButton = ttk.Button(mFrame, image=photo1, command=stop_btn)
stopButton.grid(row=0, column=1, padx=10)

photo2 = PhotoImage(file='Photos/pause.png')
pauseButton = ttk.Button(mFrame, image=photo2, command=pause_btn)
pauseButton.grid(row=0, column=2, padx=10)

bFrame = Frame(right_frame)
bFrame.pack(padx=10, pady=10)

photo3 = PhotoImage(file='Photos/playagain.png')
rewindButton = ttk.Button(bFrame, image=photo3, command=rewind_btn)
rewindButton.grid(row=0, column=0, padx=20)

photo4 = PhotoImage(file='Photos/mute.png')
# muteButton = Button(bFrame, image=photo4, command=rewind_btn)
# muteButton.grid(row=0, column=0)

photo5 = PhotoImage(file='Photos/loud.png')
volume_button = ttk.Button(bFrame, image=photo5, command=mute_btn)
volume_button.grid(row=0, column=1)

vol_scale = ttk.Scale(bFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
vol_scale.set(10)
set_vol(10)
vol_scale.grid(row=0, column=2)


def on_closing():
    stop_btn()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()  # Displays the window
