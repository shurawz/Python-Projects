from tkinter import *
from pygame import mixer

mixer.init()


def play_btn():
    mixer.music.load("Laakhau Hajarau.mp3")
    mixer.music.play()
    # print("Congrats Goru, its working.")


window = Tk()  # Creates a window
window.title("Music Player")
window.iconbitmap(r'Photos\MPicon.ico')  # r stands for Random String
window.geometry('300x300')

text = Label(window, text="Let's make some noise!")
text.pack()  # pack the label so that it could be appear in the window.

photo = PhotoImage(file='Photos\play.png')
playButton = Button(window, image=photo, command=play_btn)
playButton.pack()

window.mainloop()  # Displays the window


