import requests
from lxml import etree
from urllib.parse import quote
import string
import tkinter as tk
import os
from tkinter import ttk

exist_film = {}
exist_choice = []
video_name = ''
channel = 'player1'
channel_dic = []
for i in range(1,12):channel_dic.append('player'+str(i))

def get_video(url):
    video = ''
    r = requests.get(url.replace(' ',''))
    html = etree.HTML(r.text)
    res = html.xpath('//*[@id="player-left"]/div/div/script[1]/text()')
    for d in res[0].replace('"','').replace('\\/','/').split(','):
        if d[:4] == 'url:':
            video = d[4:]
    return video

def search(q):
    global exist_film
    url = 'https://gmtv3.xyz/search/-------------.html?wd='+q+'&submit='
    url = quote(url, safe = string.printable)
    r = requests.get(url)
    html = etree.HTML(r.text)
    res_name = html.xpath('//*[@id="searchList"]/li[*]/div[2]/h4/a/text()')
    res_url = html.xpath('//*[@id="searchList"]/li[*]/div[2]/p[5]/a[1]/@href')
    exist_film = {}
    result.delete(0,tk.END)
    for n,u in zip(res_name[::-1],res_url[::-1]):
        exist_film[n]='https://gmtv3.xyz'+u
        result.insert(0,n)
    return exist_film

def get_video_list(name):
    global exist_choice,video_name,channel,channel_dic
    url = exist_film[name]
    video_name = name
    r = requests.get(url.replace(' ',''))
    html = etree.HTML(r.text)
    res_half = html.xpath('//*[@id="'+channel+'"]/*[@id="playlist"]/li[*]/a/@href')
    res_txt = html.xpath('//*[@id="'+channel+'"]/*[@id="playlist"]/li[*]/a/text()')
    channel_dic = html.xpath('//*[@id="player-sidebar"]/div/div/div[2]/div[*]/@id')
    cbx.config(values=channel_dic)
    root.update()
    exist_choice = []
    more_data.delete(0,tk.END)
    for r,t in zip(res_half[::-1],res_txt[::-1]):
        exist_choice.insert(0,'https://gmtv3.xyz'+r)
        more_data.insert(0,t.replace('\n','').replace(' ','').replace('	',''))
    return exist_choice

def download(index):
    global exist_choice,video_name
    grand = open('./download.bat','w',encoding='gbk')
    dl_list = []
    for i in index:
        video_url = get_video(exist_choice[i])
        dl_list.append(video_name+'_'+str(i)+'.mp4')
        grand.write('.\\m3u8DL\\m3u8DL.exe '+video_url+' --saveName '+video_name+'_'+more_data.get(i).replace('\n','').replace(' ','').replace('	','')+' --enableDelAfterDone --disableIntegrityCheck\n')
    grand.close()
    os.system('start download.bat')

def set_channel(a):
    global channel,channel_dic,value,video_name
    channel = value.get()
    if video_name != '':get_video_list(video_name)

#print(search('环太平洋'))
#print(get_video_list('https://gmtv3.xyz/ep-FiEab-1-2.html'))
#url = 'https://gmtv3.xyz/ep-YCnab-1-1.html'

root = tk.Tk() 
root.title("电影下载")
root.geometry("960x560+10+10")
try:root.iconbitmap('favicon.ico')
except:pass
root["bg"] = "#66ccff"
tk.Label(root, text="电影,电视剧,动漫三合一下载",bg="#66ccff",font=('Simhei',25)).place(x = 280, y = 5)
entry = tk.Entry(root, width=40 ,bd = 2,font=('Simhei',30))
entry.place(x = 0, y = 50)
tk.Button(root, text = "搜索", command = lambda: search(entry.get()), width=15 ,height=2,activeforeground='#66ccff',font=('Simhei',14)).place(x = 805, y = 48)
#result = tk.Text(root, width=95,height=21,bd = 2,font=('Simhei',15))
#result.place(x = 2, y = 100)
result = tk.Listbox(root,width=34,height=16,font=('Simhei',20),relief='sunken',selectmode=tk.SINGLE,selectforeground='#19A59B',selectbackground='#CCEEFF',activestyle='none')
result.place(x = 0, y = 100)
more_data = tk.Listbox(root,width=34,height=14,font=('Simhei',20),relief='sunken',selectmode=tk.EXTENDED,selectforeground='#19A59B',selectbackground='#CCEEFF',activestyle='none')
more_data.place(x = 484, y = 100)
tk.Button(root, text = "查看分集", command = lambda: get_video_list(result.get(0,tk.END)[result.curselection()[0]]), width=10 ,height=2,activeforeground='#66ccff',font=('Simhei',14)).place(x = 484, y = 500)
tk.Button(root, text = "下载", command = lambda: download(more_data.curselection()), width=6 ,height=2,activeforeground='#66ccff',font=('Simhei',14)).place(x = 599, y = 500)
tk.Button(root, text = "下载全部", command = lambda: download(range(len(more_data.get(0,tk.END)))), width=10 ,height=2,activeforeground='#66ccff',font=('Simhei',14)).place(x = 674, y = 500)
tk.Label(root, text="线\n路",bg="#66ccff",font=('Simhei',15)).place(x = 785, y = 503)
value = tk.StringVar()
value.set(channel)
cbx = ttk.Combobox(root, width = 12, height = 2, textvariable=value,values=channel_dic,font=('Simhei',14))
cbx.bind('<<ComboboxSelected>>', set_channel)
cbx.place(x = 812, y = 500)
tk.Label(root, text="分集消失代表无该线路",bg="#66ccff",font=('Simhei',10)).place(x = 810, y = 530)
root.mainloop()
