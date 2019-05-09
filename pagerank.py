from urllib.request import urlopen,Request
from html.parser import HTMLParser
from urllib.parse import urlparse
from numpy import *

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
    
array1={} #{当前网址:下一层网址}
array2={} #{当前网址:下一层网址出现次数}
array_inter1=[] #网址名
array_inter2=[] #网址出现次数
Url=input('''Please input the first url:\n''')
spider_degree=2
degree=1
queue=[Url]
Queue=[Url]
end_url=Queue[-1]
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
                S[name.index(array1[i][j]),name.index(i)]=number
    else:
        for j in range(N):
            S[j,name.index(i)]=1/N

        
a=0.85
E=mat(ones((N,N)))  
A=a*S+(1-a)/N*E

print(A)

e=0.0000001
p=mat(zeros((N,1)))
p[0,0]=1
P=A*p
while(linalg.norm(P-p)>=e):
    p=P
    P=A*P

dic={}
for i in range(len(name)):
    dic[name[i]]=p[i,0]

for i in sorted(dic,key=dic.__getitem__,reverse=True):
    print(i,dic[i])

#http://scse.buaa.edu.cn/
#https://news.sina.com.cn/
