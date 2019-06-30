from tkinter import *
import tkinter.scrolledtext
import tkinter.font as tkFont
import tkinter.messagebox as msg
from tkinter import simpledialog

class mainPage:
    '''def __init__(self,master):
        #region 1

        #贴背景图片
        photo = PhotoImage(file=r"bg.gif")
        master = w
        label = Label(master, image=photo)  # 图片
        label.pack()
        #定义字体
        font = tkFont.Font(family=r'SourceHanSansCN-Regular', size=12)
        fontBig = tkFont.Font(family=r'SourceHanSansCN-Regular', size=23)
        fontSongBig = tkFont.Font(family=r'SourceHanSerifCN-Regular', size=24)
        fontSong = tkFont.Font(family=r'SourceHanSerifCN-Regular', size=12)

        songListIDPrompt = StringVar()
        songListIDPrompt.set('请输入您要查询的歌单ID')
        songListID = Entry(master, font=fontBig, textvariable=songListIDPrompt, fg='grey', bg='white')
        songListID.bind('<FocusIn>', entryFocusIn)
        songListID.bind('<FocusOut>', entryFocusOut)
        songListID.place(x=400, y=10, width=500, height=60)

        queryButton = Button(master, font=fontBig, text='查询', command=query, bg='white')
        queryButton.place(x=920, y=10, width=100, height=60)

        title = Label(master, text='', font=fontSongBig, bg='white', justify='left')
        title.place(x=20, y=82)
        creator = Label(master, text='', font=font, bg='white', justify='left')
        creator.place(x=20, y=300)
        # description=Label(w,text='',font=fontSong,bg='white',justify='left',yscrollcommand=desScr.set)
        description = tkinter.scrolledtext.ScrolledText(master, height=8, font=font)
        description.bind('<KeyPress>', lambda b: 'break')
        description.place(x=20, y=130, width=600, height=170)

        Label(master, text='歌曲名称', font=font, bg='white').place(x=20, y=330)
        Label(master, text='艺术家', font=font, bg='white').place(x=340, y=330)
        Label(master, text='专辑', font=font, bg='white').place(x=490, y=330)
        Label(master, text='时长', font=font, bg='white').place(x=810, y=330)

        songList = Listbox(master, yscrollcommand=yscroll1, height=20, width=40, font=font, selectmode='single',
                           exportselection=False)
        artistList = Listbox(master, yscrollcommand=yscroll2, height=20, width=20, font=font, selectmode='single',
                             exportselection=False)
        albumList = Listbox(master, yscrollcommand=yscroll3, height=20, width=40, font=font, selectmode='single',
                            exportselection=False)
        durationList = Listbox(master, yscrollcommand=yscroll4, height=20, width=7, font=font, selectmode='single',
                               exportselection=False)
        songListXScr = Scrollbar(master, command=songList.xview, orient=HORIZONTAL)
        songListXScr.place(x=20, y=790, width=320)
        songList.config(xscrollcommand=songListXScr.set)
        artistListXScr = Scrollbar(master, command=artistList.xview, orient=HORIZONTAL)
        artistListXScr.place(x=340, y=790, width=150)
        artistList.config(xscrollcommand=artistListXScr.set)
        albumListXScr = Scrollbar(master, command=albumList.xview, orient=HORIZONTAL)
        albumListXScr.place(x=490, y=790, width=320)
        albumList.config(xscrollcommand=albumListXScr.set)

        songList.place(x=20, y=355, anchor=NW, width=320, height=430)
        artistList.place(x=340, y=355, anchor=NW, width=150, height=430)
        albumList.place(x=490, y=355, anchor=NW, width=320, height=430)
        durationList.place(x=810, y=355, anchor=NW, width=50, height=430)
        scroll = Scrollbar(master)
        scroll.place(x=860, y=355, width=17, height=430)

        songList.bind('<<ListboxSelect>>', songListListener)
        artistList.bind('<<ListboxSelect>>', artistListListener)
        albumList.bind('<<ListboxSelect>>', albumListListener)
        durationList.bind('<<ListboxSelect>>', durationListListener)
        scroll.config(command=yview)

        playBg = PhotoImage(file=r"play.gif")
        pauseBg = PhotoImage(file=r"pause.gif")
        lastBg = PhotoImage(file=r"last.gif")
        nextBg = PhotoImage(file=r"next.gif")
        downloadBg = PhotoImage(file=r'download.gif')
        settingsBg = PhotoImage(file=r'settings.gif')
        defaultSongBg = PhotoImage(file=r"defaultSong.gif")
        defaultSongListBg = PhotoImage(file=r"defaultSongList.gif")

        lastButton = Button(master, text='播放', bg='white', font=fontBig, image=lastBg, command=clickLast)
        playButton = Button(master, text='播放', bg='white', command=clickPlay, font=fontBig, image=playBg)
        nextButton = Button(master, text='播放', bg='white', font=fontBig, image=nextBg, command=clickNext)

        lastButton.place(x=10, y=820, width=60, height=60)
        playButton.place(x=80, y=820, width=60, height=60)
        nextButton.place(x=150, y=820, width=60, height=60)

        progress = 0

        scaleProgress = Scale(master, from_=0, to=1, resolution=0.0001, orient=HORIZONTAL, bg='#fa789f', bd=0,
                              relief='groove', \
                              showvalue=False, troughcolor='white', label='0:00/0:00', font=font, foreground='white',
                              variable=progress)
        scaleVolume = Scale(master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, bg='#fa789f', bd=0, relief='groove',
                            showvalue=False, \
                            troughcolor='white', label='音量', font=font, command=setVolume, repeatinterval=20,
                            foreground='white')
        scaleVolume.set(0.5)
        scaleProgress.place(x=220, y=820, height=60, width=700)
        scaleVolume.place(x=1015, y=820, height=60, width=300)

        songName = Label(master, text='', font=fontSongBig, bg='white')
        songName.place(x=880, y=170)
        albumName = Label(master, text='', font=fontSongBig, bg='white')
        albumName.place(x=880, y=220)
        artistName = Label(master, text='', font=fontSongBig, bg='white')
        artistName.place(x=880, y=270, )

        downloadButton = Button(master, text='播放', bg='white', command=clickDownload, font=fontBig, image=downloadBg)
        downloadButton.place(x=1330, y=820, width=60, height=60)
        settingsButton = Button(master, text='播放', bg='white', command=clickSettings, font=fontBig, image=settingsBg)
        settingsButton.place(x=1400, y=820, width=60, height=60)

        lyricScr = Scrollbar(master, command=songList.yview, orient=VERTICAL)
        lyricScr.place(x=1580, y=440, width=17, height=350)
        lyric = Listbox(master, font=fontSong, justify='center', yscrollcommand=lyricScr.set, selectmode='single')
        lyric.place(x=900, y=440, width=680, height=350)
        lyricScr.config(command=lyric.yview)

        songPhoto = Label(master, image=defaultSongBg)
        songPhoto.place(x=1240, y=90)
        songListPhoto = Label(master, image=defaultSongListBg)
        songListPhoto.place(x=630, y=90)
        scaleProgress.set(0)
        #endregion'''

    def __init__(self, master):
        self.__master=master
        self.initMaterial()
        self.createWidget()

    def createWidget(self):
        self.title = Label(self.__master, text='default', font=self.fontSongBig, bg='white', justify='left')
        self.title.place(x=20, y=82)
        self.creator = Label(self.__master, text='default', font=self.font, bg='white', justify='left')
        self.creator.place(x=20, y=300)

    def initMaterial(self):
        # 定义字体
        self.font = tkFont.Font(family=r'SourceHanSansCN-Regular', size=12)
        self.fontBig = tkFont.Font(family=r'SourceHanSansCN-Regular', size=23)
        self.fontSongBig = tkFont.Font(family=r'SourceHanSerifCN-Regular', size=24)
        self.fontSong = tkFont.Font(family=r'SourceHanSerifCN-Regular', size=12)

        # 定义图片
        self.playBg = PhotoImage(file=r"play.gif")
        self.pauseBg = PhotoImage(file=r"pause.gif")
        self.lastBg = PhotoImage(file=r"last.gif")
        self.nextBg = PhotoImage(file=r"next.gif")
        self.downloadBg = PhotoImage(file=r'download.gif')
        self.settingsBg = PhotoImage(file=r'settings.gif')
        self.defaultSongBg = PhotoImage(file=r"defaultSong.gif")
        self.defaultSongListBg = PhotoImage(file=r"defaultSongList.gif")


if __name__=='__main__':

    #创建窗口
    w = Tk()
    #定义窗口
    w.title('')
    w.geometry('1600x900')
    w.resizable(0, 0)
    w.iconbitmap(default='favicon.ico')
    #放置页面
    mainPage(w)
    w.mainloop()