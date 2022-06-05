import tkinter as tk
from tkinter import PhotoImage
from tkinter import filedialog
import os
import pickle
from pygame import mixer

class Player(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("550x380")
        self.title("Kansal's MP3 Player")
        self.maxsize(550, 380)
        self.minsize(550, 380)
        self.config(bg="sky blue")
        mixer.init()

        self.current = 0
        self.paused = True
        self.played = False
        self.mute = False



        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []
        self.create_frames()
        self.backFrame()
        self.playlistFrame()
        self.commandboxFrame()

    def create_frames(self):
        self.back = tk.LabelFrame(self, text="Track", font=("new time romans", 9, "bold"), bg="blue", fg="purple",borderwidth=5, relief=tk.GROOVE)
        self.back.config(width=300, height=250)
        self.back.grid(row=0, column=0, padx=5, pady=5)

        self.playlistbox = tk.LabelFrame(self, text="PLAYLIST", font=("times new romans", 9, "bold"), bg="blue",fg="purple", borderwidth=5, relief=tk.GROOVE)
        self.playlistbox.config(width=130, height=265)
        self.playlistbox.grid_propagate(False)
        self.playlistbox.grid(row=0, column=1)

        self.commandbox = tk.Frame(self, bg="blue", borderwidth=5, relief=tk.GROOVE)
        self.commandbox.config(width=540, height=80)
        self.commandbox.grid_propagate(False)
        self.commandbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def backFrame(self):
        self.background = PhotoImage(file="background.png")
        self.label = tk.Label(self.back, image=self.background)
        self.label.config(width=390, height=220)
        self.label.grid(row=0, column=0)

        self.songtrack=tk.Label(self.back, text=" DJ PRANAV", font="comicsansms 9 bold", bg="blue", fg="dark blue")
        self.songtrack.grid(row=1,column=0)

    def playlistFrame(self):
        self.scrollbar = tk.Scrollbar(self.playlistbox, orient=tk.VERTICAL, bg="blue")
        self.scrollbar.grid(row=0, column=1, rowspan=1, sticky='ns')

        self.list = tk.Listbox(self.playlistbox, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set, selectbackground="blue")
        self.list.config(height=15, width=16)
        self.enumeratesongs()
        self.list.bind('<Double-1>', self.play_song)

        self.scrollbar.config(command="list.yview")
        self.list.grid(row=0, column=0)

    def commandboxFrame(self):

        self.loadimage = tk.PhotoImage(file="load.png")
        self.loadbutton = tk.Button(self.commandbox, image=self.loadimage, command=self.retrieve_songs)
        self.loadbutton.config(width=55, height=55)
        self.loadbutton.grid(row=0, column=1)

        self.previmage = tk.PhotoImage(file="pr.png")
        self.prevbutton = tk.Button(self.commandbox, image=self.previmage,command= self.prev_song)
        self.prevbutton.config(width=55, height=55)
        self.prevbutton.grid(row=0, column=2)

        self.pauseimage = tk.PhotoImage(file="pa.png")
        self.pausebutton = tk.Button(self.commandbox, image=self.pauseimage)
        self.pausebutton['command'] = self.pause_song
        self.pausebutton.config(width=60, height=55)
        self.pausebutton.grid(row=0, column=3, pady=5)

        self.nextimage = tk.PhotoImage(file="ne.png")
        self.nextbutton = tk.Button(self.commandbox, image=self.nextimage, command= self.next_song)
        self.nextbutton.config(width=55, height=55)
        self.nextbutton.grid(row=0, column=4, pady=5)

        self.muteimage = tk.PhotoImage(file="mute.png")
        self.mutebutton = tk.Button(self.commandbox, image=self.muteimage,command=self.mute_song)
        self.mutebutton.config(width=55, height=55)
        self.mutebutton.grid(row=0, column=5, pady=5)

        self.v=tk.DoubleVar(self)
        self.volume = tk.Scale(self.commandbox, from_=0, to=10, orient=tk.HORIZONTAL, tickinterval=5, bg="blue",troughcolor="dark blue")
        self.volume['variable']=self.v
        self.volume.set(8)
        mixer.music.set_volume(0.8)
        self.volume['command'] = self.change_volume
        self.volume.grid(row=0, column=6)


    def retrieve_songs(self):
        self.songlist = []
        self.directory = tk.filedialog.askdirectory()
        for root_, dirs, files in os.walk(self.directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\', '/')
                    self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)
        self.playlist = self.songlist
        self.list.delete(0, tk.END)
        self.enumeratesongs()

    def enumeratesongs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def play_pause_song(self, event):
        if self.paused:
            self.play_song()
        else:
            self.pause_song()
    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="white")

        print(self.playlist[self.current])
        mixer.music.load(self.playlist[self.current])
        self.songtrack['anchor'] = 'w'
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])

        self.playimage = PhotoImage(file = "pl.png")
        self.pausebutton['image'] = self.playimage
        self.paused = False
        self.played = True
        #self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg='sky blue')

        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pausebutton['image'] = self.pauseimage
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pausebutton['image'] = self.playimage
    def mute_song(self):
        if not self.mute:
            self.unmuteimage = tk.PhotoImage(file="unmute.png")
            self.mutebutton['image']=self.unmuteimage
            self.mute=True
            self.v=0.0
            self.volume.set(0)
            mixer.music.set_volume(self.v / 10)
        else:
            self.mutebutton['image'] = self.muteimage
            self.mute=False
            self.volume.set(8)
            self.v=self.volume.get()
            mixer.music.set_volume(self.v/10)

    def change_volume(self, event=None):
            self.v = self.volume.get()
            mixer.music.set_volume(self.v / 10)

    def prev_song(self,event = None):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current+1, bg='white')
        self.play_song()

    def next_song(self):
        if self.current < len(self.playlist)-1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current-1,bg='white')
        self.play_song()

if __name__ == '__main__':
    app = Player()
    app.mainloop()