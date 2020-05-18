from tkinter import *
from pygame import mixer

mixer.init()


def play_btn():
    mixer.music.load("Laakhau Hajarau.mp3")
    mixer.music.play()
    # print("Congrats Goru, its working.")


def stop_btn():
    mixer.music.stop()


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)


window = Tk()  # Creates a window
window.title("Music Player")
window.iconbitmap(r'Photos\MPicon.ico')  # r stands for Random String
window.geometry('300x300')

text = Label(window, text="Let's make some noise!")
text.pack()  # pack the label so that it could be appear in the window.

photo = PhotoImage(file='Photos\play.png')
playButton = Button(window, image=photo, command=play_btn)
playButton.pack()

photo1 = PhotoImage(file='Photos\stop.png')
stopButton = Button(window, image=photo1, command=stop_btn)
stopButton.pack()

vol_scale = Scale(window, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
vol_scale.set(4)
vol_scale.pack()

window.mainloop()  # Displays the window


