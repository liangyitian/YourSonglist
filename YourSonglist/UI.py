from tkinter import *
import PIL
from PIL import Image,ImageTk
import tkinter.scrolledtext
import tkinter.font as tkFont
import requests
import json
import tkinter.messagebox as msg
import time
import pygame
import os
import threading
from tkinter import simpledialog

def thread_download(id):
    url = 'http://music.163.com/song/media/outer/url?id=' + id + '.mp3'
    r = requests.get(url)
    with open(id + '.mp3', 'wb') as f:
        f.write(r.content)
        f.close()
    play(id)
def thread_download1(id,path):
    url = 'http://music.163.com/song/media/outer/url?id=' + id + '.mp3'
    r = requests.get(url)
    with open(path+id + '.mp3', 'wb') as f:
        f.write(r.content)
        f.close()

#region Listbox Sync
def yscroll1(*args):
    if artistList.yview() != songList.yview() :
        artistList.yview_moveto(args[0])
    if albumList.yview() != songList.yview() :
        albumList.yview_moveto(args[0])
    if durationList.yview() != songList.yview() :
        durationList.yview_moveto(args[0])
    scroll.set(*args)
def yscroll2(*args):
    if songList.yview() != artistList.yview():
        songList.yview_moveto(args[0])
    if albumList.yview() != artistList.yview() :
        albumList.yview_moveto(args[0])
    if durationList.yview() != artistList.yview() :
        durationList.yview_moveto(args[0])
    scroll.set(*args)
def yscroll3(*args):
    if artistList.yview() != albumList.yview() :
        artistList.yview_moveto(args[0])
    if songList.yview() != albumList.yview() :
        songList.yview_moveto(args[0])
    if durationList.yview() != albumList.yview() :
        durationList.yview_moveto(args[0])
def yscroll4(*args):
    if artistList.yview() != durationList.yview():
        artistList.yview_moveto(args[0])
    if songList.yview() != durationList.yview():
        songList.yview_moveto(args[0])
    if albumList.yview() != durationList.yview():
        albumList.yview_moveto(args[0])

def yview(*args):
    songList.yview(*args)
    artistList.yview(*args)
    albumList.yview(*args)
    durationList.yview(*args)
#使多个列表之间互相同步

def songListListener(*args):
    index=songList.curselection()[0]
    te = songList.get(songList.curselection()[0])
    artistList.select_clear(0,END)
    artistList.select_set(index)
    albumList.select_clear(0, END)
    albumList.select_set(index)
    durationList.select_clear(0, END)
    durationList.select_set(index)
    if index!=currentIndex:
        playButton.config(image=playBg)
    else:
        playButton.config(image=pauseBg)
def artistListListener(*args):
    index=artistList.curselection()[0]
    te = artistList.get(artistList.curselection()[0])
    songList.select_clear(0,END)
    songList.select_set(index)
    albumList.select_clear(0, END)
    albumList.select_set(index)
    durationList.select_clear(0, END)
    durationList.select_set(index)
    if index!=currentIndex:
        playButton.config(image=playBg)
    else:
        playButton.config(image=pauseBg)
def albumListListener(*args):
    index=albumList.curselection()[0]
    te = albumList.get(albumList.curselection()[0])
    artistList.select_clear(0,END)
    artistList.select_set(index)
    songList.select_clear(0, END)
    songList.select_set(index)
    durationList.select_clear(0, END)
    durationList.select_set(index)
    if index!=currentIndex:
        playButton.config(image=playBg)
    else:
        playButton.config(image=pauseBg)
def durationListListener(*args):
    index=durationList.curselection()[0]
    te = durationList.get(durationList.curselection()[0])
    artistList.select_clear(0,END)
    artistList.select_set(index)
    albumList.select_clear(0, END)
    albumList.select_set(index)
    songList.select_clear(0, END)
    songList.select_set(index)
    if index!=currentIndex:
        playButton.config(image=playBg)
    else:
        playButton.config(image=pauseBg)
#使多个列表的选中项同步

#endregion
data=None
def lrcTime(str):
    for i in range(len(str)):
        if str[i]==':':
            index1=i
        if str[i]=='.':
            index2=i
    min=int(str[0:index1])
    sec=int(str[index1+1:index2])
    ms=int(str[index2+1:])
    return min*60*1000+sec*1000+ms

def getLyric(songID):
    url='http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1'.format(songID)
    data=json.loads(requests.get(url).content)
    lyric={}
    if 'nolyric' in data:
        lyric['time'] = [0]
        lyric['sentence'] = ['纯音乐，无歌词']
    if 'lrc' in data:
        lyric['isPureMusic']=False
        lyric['text']=data['lrc']['lyric']
        lrcList=data['lrc']['lyric'].split('\n')
        lyric['time']=[]
        lyric['sentence']=[]
        lyric['list']=lrcList
        for i in lrcList:
            for j in range(len(i)):
                if i[j]==']':
                    endIndex=j
                    if i[1:3].isdigit() and i[j+1:]!='':
                        lyric['time'].append(lrcTime(i[1:j]))
                        lyric['sentence'].append(i[j+1:])
                    break
        print(lyric['time'])
        print(lyric['sentence'])
        print(lyric['text'])
        return lyric
    lyric['time'] = [0]
    lyric['sentence'] = ['纯音乐，无歌词']
    return lyric

def getData(songlistID,*type):
    url='http://music.163.com/api/playlist/detail?id='
    data=json.loads(requests.get(url+songlistID).content)
    if data['code']==404 or data['code']==400:
        return False
    if data['code']==200:
        if data['result']['trackCount']==0:
            return False
    return data

def entryFocusIn(*args):
    if songListID.get()=='请输入您要查询的歌单ID':
        songListIDPrompt.set('')
        songListID.config(fg='black')

def entryFocusOut(*args):
    if songListID.get()=='':
        songListIDPrompt.set('请输入您要查询的歌单ID')
        songListID.config(fg='grey')

def transimg(img_path,px):
    """
    转换图片格式
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    try:
        str = img_path.rsplit(".", 1)
        output_img_path = str[0] + ".gif"
        print(output_img_path)
        im = Image.open(img_path)
        im=im.resize((px,px))
        im.save(output_img_path)
        return True
    except:
        return False

def query():
    threadQuery = threading.Thread(target=thread_query, args=())
    threadQuery.start()

def thread_query():
    global data,songListPhoto
    id=songListID.get()
    result=getData(id)
    if result==False:
        msg.showerror(title='错误',message='找不到这个歌单')
    else:
        data=result
        title.config(text=data['result']['name'])
        description.delete(0.0, END)
        if  data['result']['description']!=None:
            description.insert(END, data['result']['description'])
        else:
            description.insert(END, '无描述')
        info = '创建者：' + data['result']['creator']['nickname'] + '     歌单播放次数:' + str(
            data['result']['playCount']) + '     标签：'
        for i in data['result']['tags']:
            info += str(i) + '；'
        creator.config(text=info)
        url =data['result']['coverImgUrl']
        r = requests.get(url)
        with open(id+'.jpg', 'wb') as p:
            p.write(r.content)
            p.close()
        transimg(id+'.jpg',240)
        global imgif
        imgif= PhotoImage(file=id+".gif")
        songListPhoto = Label(w,image=imgif)
        songListPhoto.place(x=630, y=90)
        songList.delete(0, END)
        artistList.delete(0, END)
        albumList.delete(0, END)
        durationList.delete(0, END)
        for i in data['result']['tracks']:
            songList.insert(END, str(i['name']))
            artist = []
            for j in i['artists']:
                artist.append(j['name'])
            artistList.insert(END, '/'.join(artist))
            albumList.insert(END, i['album']['name'])
            duration = i['duration'] // 1000
            min = str(duration // 60)
            sec = str(duration % 60)
            if len(sec) == 1:
                sec = '0' + sec
            durationList.insert(END, min + ':' + sec)
        print('displayed')

        # 表中添加数据

def displaySongImage(songId):

    url = data['result']['tracks'][currentIndex]['album']['picUrl']
    print(url)
    r = requests.get(url)
    with open(songId +'img'+'.jpg', 'wb') as p:
        p.write(r.content)
        p.close()
    transimg(songId +'img' + '.jpg',330)
    global songImg
    songImg = PhotoImage(file=songId +'img'+ ".gif")
    songPhoto = Label(w, image=songImg)
    songPhoto.place(x=1240, y=90)

def play(id):
    pygame.mixer.music.load(id + '.mp3')
    pygame.mixer.music.play()
    playButton.config(image=pauseBg)
    songName.config(text=data['result']['tracks'][currentIndex]['name'])
    albumName.config(text=data['result']['tracks'][currentIndex]['album']['name'])
    artist = []
    for j in data['result']['tracks'][currentIndex]['artists']:
        artist.append(j['name'])
    artistName.config(text='/'.join(artist))
    lyric.delete(0,END)
    global lrc
    lrc=getLyric(id)

    for i in lrc['sentence']:
        lyric.insert(END,i)
    displaySongImage(songId=id)
    print(lrc['time'])




    isPlaying = True
    isPaused=False

def clickLast():
    global data, isPlaying, isPaused
    global currentDuration, currentSong, currentIndex
    if currentIndex>0:
        index = currentIndex-1
        id = str(data['result']['tracks'][index]['id'])


        currentDuration = data['result']['tracks'][index]['duration']
        currentIndex = index
        currentSong = id
        url = 'http://music.163.com/song/media/outer/url?id=' + id + '.mp3'
        if not os.path.exists(id + '.mp3'):
            download = threading.Thread(target=thread_download, args=(id,))
            download.start()
        else:
            play(id)

def clickNext():
    global data, isPlaying, isPaused
    global currentDuration, currentSong, currentIndex
    if currentIndex < songList.size()-1:
        index = currentIndex + 1
        id = str(data['result']['tracks'][index]['id'])

        currentDuration = data['result']['tracks'][index]['duration']
        currentIndex = index
        currentSong = id
        url = 'http://music.163.com/song/media/outer/url?id=' + id + '.mp3'
        if not os.path.exists(id + '.mp3'):
            download = threading.Thread(target=thread_download, args=(id,))
            download.start()
        else:
            play(id)

def clickPlay():
    global data,isPlaying,isPaused
    global currentDuration, currentSong,currentIndex
    index = songList.curselection()[0]
    id = str(data['result']['tracks'][index]['id'])

    if (not pygame.mixer.music.get_busy()) or currentSong!=id:
        #如果没在播放(刚打开)，或者播放新的曲目，则播放文件
        currentDuration=data['result']['tracks'][index]['duration']
        currentIndex=index
        currentSong=id
        url = 'http://music.163.com/song/media/outer/url?id=' + id + '.mp3'
        if not os.path.exists(id + '.mp3'):
            download = threading.Thread(target=thread_download, args=(id,))
            download.start()
        else:
            play(id)
    else:
        if not isPaused:
            pygame.mixer.music.pause()
            isPaused=True
            playButton.config(image=playBg)
            print(pygame.mixer.music.get_busy())
        else:
            pygame.mixer.music.unpause()
            isPaused=False
            playButton.config(image=pauseBg)

def clickSettings():
    downloadPath=simpledialog.askstring('设置','请输入歌曲的下载路径')

def clickDownload():

    global data, isPlaying, isPaused
    global currentDuration, currentSong, currentIndex

    index = songList.curselection()[0]
    id = str(data['result']['tracks'][index]['id'])
    download = threading.Thread(target=thread_download1, args=(id,))
    download.start()

def setVolume(pos):
    pygame.mixer.music.set_volume(float(pos))

def stop():
    pygame.mixer.music.stop()

def updateProgressBar():
    global currentLyric
    if pygame.mixer.music.get_busy() and not isPaused:
        if not isPressed:
            pos=pygame.mixer.music.get_pos()
            scaleProgress.set(pos/currentDuration)

        min1=str(pos//1000//60)
        sec1=str((pos//1000)%60)
        min2=str(currentDuration//1000//60)
        sec2=str((currentDuration//1000)%60)
        if len(sec1)==1:
            sec1='0'+sec1
        if len(sec2) == 1:
            sec2 = '0' + sec2
        scaleProgress.config(label=min1+':'+sec1+'/'+min2+':'+sec2)
        last=0
        for i in range(lyric.size()):
            if lrc['time'][i]<pos:
                last=i
            else:
                lyric.selection_clear(0,END)
                lyric.select_set(last)
                lyric.see(last)

    w.after(20, updateProgressBar)


#region draw
w = Tk()
w.title('')
w.geometry('1600x900')
w.resizable(0,0)
w.iconbitmap(default='favicon.ico')

photo=PhotoImage(file=r"bg.gif")
label=Label(w,image=photo)  #图片
label.pack()




font=tkFont.Font(family=r'SourceHanSansCN-Regular',size=12)


fontBig=tkFont.Font(family=r'SourceHanSansCN-Regular',size=23)
fontSongBig=tkFont.Font(family=r'SourceHanSerifCN-Regular',size=24)
fontSong=tkFont.Font(family=r'SourceHanSerifCN-Regular',size=12)

songListIDPrompt=StringVar()
songListIDPrompt.set('请输入您要查询的歌单ID')
songListID=Entry(w,font=fontBig,textvariable=songListIDPrompt,fg='grey',bg='white')
songListID.bind('<FocusIn>',entryFocusIn)
songListID.bind('<FocusOut>',entryFocusOut)
songListID.place(x=400,y=10,width=500,height=60)

queryButton=Button(w,font=fontBig,text='查询',command=query,bg='white')
queryButton.place(x=920,y=10,width=100,height=60)


title=Label(w,text='',font=fontSongBig,bg='white',justify='left')
title.place(x=20,y=82)
creator=Label(w,text='',font=font,bg='white',justify='left')
creator.place(x=20,y=300)
#description=Label(w,text='',font=fontSong,bg='white',justify='left',yscrollcommand=desScr.set)
description=tkinter.scrolledtext.ScrolledText(w,height=8,font=font)
description.bind('<KeyPress>',lambda b:'break')
description.place(x=20,y=130,width=600,height=170)



Label(w,text='歌曲名称',font=font,bg='white').place(x=20,y=330)
Label(w,text='艺术家',font=font,bg='white').place(x=340,y=330)
Label(w,text='专辑',font=font,bg='white').place(x=490,y=330)
Label(w,text='时长',font=font,bg='white').place(x=810,y=330)


songList= Listbox(w,yscrollcommand=yscroll1,height=20,width=40,font=font,selectmode='single',exportselection=False)
artistList= Listbox(w,yscrollcommand=yscroll2,height=20,width=20,font=font,selectmode='single',exportselection=False)
albumList= Listbox(w,yscrollcommand=yscroll3,height=20,width=40,font=font,selectmode='single',exportselection=False)
durationList= Listbox(w,yscrollcommand=yscroll4,height=20,width=7,font=font,selectmode='single',exportselection=False)
songListXScr=Scrollbar(w,command=songList.xview,orient=HORIZONTAL)
songListXScr.place(x=20,y=790,width=320)
songList.config(xscrollcommand=songListXScr.set)
artistListXScr=Scrollbar(w,command=artistList.xview,orient=HORIZONTAL)
artistListXScr.place(x=340,y=790,width=150)
artistList.config(xscrollcommand=artistListXScr.set)
albumListXScr=Scrollbar(w,command=albumList.xview,orient=HORIZONTAL)
albumListXScr.place(x=490,y=790,width=320)
albumList.config(xscrollcommand=albumListXScr.set)

songList.place(x=20,y=355,anchor=NW,width=320,height=430)
artistList.place(x=340,y=355,anchor=NW,width=150,height=430)
albumList.place(x=490,y=355,anchor=NW,width=320,height=430)
durationList.place(x=810,y=355,anchor=NW,width=50,height=430)
scroll = Scrollbar(w)
scroll.place(x=860,y=355,width=17, height=430)

songList.bind('<<ListboxSelect>>',songListListener)
artistList.bind('<<ListboxSelect>>',artistListListener)
albumList.bind('<<ListboxSelect>>',albumListListener)
durationList.bind('<<ListboxSelect>>',durationListListener)
scroll.config(command=yview)

playBg=PhotoImage(file=r"play.gif")
pauseBg=PhotoImage(file=r"pause.gif")
lastBg=PhotoImage(file=r"last.gif")
nextBg=PhotoImage(file=r"next.gif")
downloadBg=PhotoImage(file=r'download.gif')
settingsBg=PhotoImage(file=r'settings.gif')
defaultSongBg=PhotoImage(file=r"defaultSong.gif")
defaultSongListBg=PhotoImage(file=r"defaultSongList.gif")

lastButton=Button(w,text='播放',bg='white',font=fontBig,image=lastBg,command=clickLast)
playButton=Button(w,text='播放',bg='white',command=clickPlay,font=fontBig,image=playBg)
nextButton=Button(w,text='播放',bg='white',font=fontBig,image=nextBg,command=clickNext)

lastButton.place(x=10,y=820,width=60,height=60)
playButton.place(x=80,y=820,width=60,height=60)
nextButton.place(x=150,y=820,width=60,height=60)

progress=0


scaleProgress=Scale(w,from_=0,to=1,resolution=0.0001,orient=HORIZONTAL,bg='#fa789f',bd=0,relief='groove',\
                    showvalue=False,troughcolor='white',label='0:00/0:00',font=font,foreground='white',variable=progress)
scaleVolume=Scale(w,from_=0,to=1,resolution=0.01,orient=HORIZONTAL,bg='#fa789f',bd=0,relief='groove',showvalue=False,\
            troughcolor='white',label='音量',font=font,command=setVolume,repeatinterval=20,foreground='white')
scaleVolume.set(0.5)
scaleProgress.place(x=220,y=820,height=60,width=700)
scaleVolume.place(x=1015,y=820,height=60,width=300)


songName=Label(w,text='',font=fontSongBig,bg='white')
songName.place(x=880,y=170)
albumName=Label(w,text='',font=fontSongBig,bg='white')
albumName.place(x=880,y=220)
artistName=Label(w,text='',font=fontSongBig,bg='white')
artistName.place(x=880,y=270,)

downloadButton=Button(w,text='播放',bg='white',command=clickDownload,font=fontBig,image=downloadBg)
downloadButton.place(x=1330,y=820,width=60,height=60)
settingsButton=Button(w,text='播放',bg='white',command=clickSettings,font=fontBig,image=settingsBg)
settingsButton.place(x=1400,y=820,width=60,height=60)

lyricScr=Scrollbar(w,command=songList.yview,orient=VERTICAL)
lyricScr.place(x=1580,y=440,width=17,height=350)
lyric=Listbox(w,font=fontSong,justify='center',yscrollcommand=lyricScr.set,selectmode='single')
lyric.place(x=900,y=440,width=680,height=350)
lyricScr.config(command=lyric.yview)

songPhoto = Label(w, image=defaultSongBg)
songPhoto.place(x=1240, y=90)
songListPhoto = Label(w,image=defaultSongListBg)
songListPhoto.place(x=630, y=90)

#endregion


downloadPath=''

isPlaying=False
isPaused=False
isPressed=False

currentLyric=0
currentSong=None
currentDuration=None
currentIndex=None

pygame.mixer.init(frequency=44100)
pygame.mixer.music.set_volume(0.5)

scaleProgress.set(0)

w.after(20,updateProgressBar)

w.mainloop()