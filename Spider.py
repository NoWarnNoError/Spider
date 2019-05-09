import wx
from urllib.request import urlopen,Request
from html.parser import HTMLParser
from urllib.parse import urlparse
from numpy import *
from bs4 import BeautifulSoup
import re

class Myparser(HTMLParser):
    def __init__(self,url):
        HTMLParser.__init__(self)
        self.url=url
        self.Link={}
        
    def handle_starttag(self,tag,attrs):
        if tag == 'a':
            for i in attrs:
                if i[0]=='href':
                    inter=urlparse(i[1])
                    if '2019-01-05' in inter.path:
                        if inter[0]=='' and inter[1]=='':
                            link=self.url+inter[2]
                        elif inter[0]=='https' or inter[0]=='http':
                            link=inter[0]+'://'+inter[1]+inter[2]
                        else: 
                            link='http://'+inter[0]+inter[1]+inter[2]

                        if link not in self.Link:
                            self.Link[link]=1
                        else:
                            self.Link[link]+=1

def spider(url,degree):
    global spider_degree
    global array_inter1
    global array_inter2
    global Queue
    global queue
    global Url
    parser=Myparser(url)
    req=Request(url,headers={'User-agent':'Mozilla 5.10'})
    try:
        html=urlopen(req)
        parser.feed(str(html.read(), encoding='utf8'))
    except:
        return
    array_inter1=[]
    array_inter2=[]
    for i in parser.Link:
        Queue.append(i)
        if degree==1:
            array_inter1.append(i)
            array_inter2.append(parser.Link[i])
        else:
            if i in array1[Url]:
                array_inter1.append(i)
                array_inter2.append(parser.Link[i])
        if degree<spider_degree:
            queue.append(i)

def pagerank():
    global spider_degree
    global array_inter1
    global array_inter2
    global Queue
    global queue
    global degree
    global array1
    global array2
    global dic
    global Url
    queue=[Url]
    Queue=[Url]
    end_url=Queue[-1]
    degree=1
    count=0
    while(queue):
        now_url=queue.pop(0)
        spider(now_url,degree)
        array1[now_url]=array_inter1
        array2[now_url]=array_inter2
        if now_url==end_url:
            degree+=1
            end_url=Queue[-1]

    name=[]
    for i in array1[Url]:
        if array2[i]:
            name.append(i)

    N=len(name)
    S=mat(zeros((N,N)))
    for i in name:
        all_number=0
        for j in range(len(array1[i])):
            if array1[i][j] in array1 and array1[i][j]!=i:
                all_number+=array2[i][j]
        if all_number!=0:
            for j in range(len(array1[i])):
                if array1[i][j] in array1 and array1[i][j]!=i:
                    number=array2[i][j]/all_number
                    try:
                        S[name.index(array1[i][j]),name.index(i)]=number
                    except:
                        continue
        else:
            for j in range(N):
                S[j,name.index(i)]=1/N


    a=0.85
    E=mat(ones((N,N)))  
    A=a*S+(1-a)/N*E

    e=0.0000001
    p=mat(zeros((N,1)))
    p[0,0]=1
    P=A*p
    while(linalg.norm(P-p)>=e):
        p=P
        P=A*P

    for i in range(len(name)):
        dic[name[i]]=p[i,0]

def clickme(event):
    global dic
    global Url
    Url=url_text.GetValue()
    pagerank() 
    counter=0
    for i in sorted(dic,key=dic.__getitem__,reverse=True):
        try:
            a=Request(i,headers={'User-agent':'Mozilla 5.10'})
            html=urlopen(a)
            soup=BeautifulSoup(str(html.read(), encoding='utf8'),"html.parser")
            
            #for j in soup.select('title'):
                #output_text.AppendText("%s"%j)
            #for j in soup.select('p'):
                #output_text.AppendText("%s"%j)
            #for j in soup.select('p #article'):
                #output_text.AppendText("%s"%j)
            #for j in soup.select('p article'):
                #output_text.AppendText("%s"%j)

            text = soup.select('.main-title')[0].text
            output1_text.AppendText("%s\n"%text)
            
            text = ''.join([p.text.strip() for p in soup.select('#article p')[:-1]])
            output2_text.AppendText("%s\n"%text)
        except:
            continue
        counter+=1
        if counter>10:
            break
#文本框用Value,静态文本用Label

def clear(event):
    url_text.Clear()
    output1_text.Clear()
    output2_text.Clear()

Url=''
Queue=[]
queue=[]
array1={} #{当前网址:下一层网址}
array2={} #{当前网址:下一层网址出现次数}
array_inter1=[] #网址名
array_inter2=[] #网址出现次数
spider_degree=2
dic={}

app=wx.App() #实例化一个主循环
frame=wx.Frame(None,title='搜索',pos=(400,100),size=(500,400)) #实例化一个窗口

panel=wx.Panel(frame) #尺寸器

reminder_StaticText=wx.StaticText(panel,label='请输入一个网址:') #静态文本

url_text=wx.TextCtrl(panel) 
output1_text=wx.TextCtrl(panel,style=wx.TE_MULTILINE)
output2_text=wx.TextCtrl(panel,style=wx.TE_MULTILINE)#文本框
font1=wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
font2=wx.Font(10, wx.SWISS, wx.NORMAL,wx.NORMAL)
output1_text.SetFont(font1)
output2_text.SetFont(font2)

spider_button=wx.Button(panel,label='搜索') #按钮
spider_button.Bind(wx.EVT_BUTTON,clickme) #按钮事件
clear_button=wx.Button(panel,label='清空')
clear_button.Bind(wx.EVT_BUTTON,clear)

box_HORIZONTAL=wx.BoxSizer(wx.HORIZONTAL) #水平
box_HORIZONTAL.Add(reminder_StaticText,proportion=1,flag=wx.EXPAND|wx.ALL,border=2)#proprotion相对比例#flag填充样式，wx.EXPAND完整填充，wx.ALL填充方向#border:边框
box_HORIZONTAL.Add(url_text,proportion=5,flag=wx.EXPAND|wx.ALL,border=2)
box_HORIZONTAL.Add(spider_button,proportion=2,flag=wx.EXPAND|wx.ALL,border=2)
box_HORIZONTAL.Add(clear_button,proportion=2,flag=wx.EXPAND|wx.ALL,border=2)

box_VERTICAL=wx.BoxSizer(wx.VERTICAL)
box_VERTICAL.Add(box_HORIZONTAL,proportion=1,flag=wx.EXPAND|wx.ALL,border=2)
box_VERTICAL.Add(output1_text,proportion=10,flag=wx.EXPAND|wx.ALL,border=2)
box_VERTICAL.Add(output2_text,proportion=10,flag=wx.EXPAND|wx.ALL,border=2)

panel.SetSizer(box_VERTICAL) #设置主尺寸器
frame.Show() #调用窗口展示功能
app.MainLoop()#启动主循环

#http://scse.buaa.edu.cn/
#https://news.sina.com.cn/
