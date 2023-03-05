import pygame as pg
from tkinter import *
from tkinter import messagebox 
import sys
from time import sleep
from copy import deepcopy

def tuple_diff(a, b):
    return (a[0] - b[0], a[1] - b[1])

def bfs(mmap, fr, to):
    global allpaths
    visited = [fr]
    queue = [([fr],False)]
    for p in allpaths:
        if len(p) <= 2:
            continue
        delta = tuple_diff(p[1], p[0])
        for i in range(2, len(p)):
            nd = tuple_diff(p[i], p[i-1])
            if nd != delta:
                visited.append(p[i-1])
            delta = nd

    offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    while len(queue) > 0:
        path, is_onBusyLine = queue.pop(0)
        vertex = path[-1]
        if vertex==to:
            for p in range(len(path)):
                path[p] = path[p][::-1]
            return path

        for o in offsets:
            is_onBusyLine = False if not is_onBusyLine else True
            nxt = (vertex[0]+o[0], vertex[1]+o[1])
            ny, nx = nxt[1], nxt[0]
            if ny>=0 and ny<len(mmap) and nx>=0 and nx < len(mmap[0]) and mmap[ny][nx] != '#':
                if nxt not in visited:
                    fuck = nxt in allpaths
                    for a in allpaths:
                        fuck = nxt in a
                        if fuck: break
                    if fuck and is_onBusyLine:
                        continue
                    elif fuck and not is_onBusyLine:
                        is_onBusyLine=True
                    elif not fuck and is_onBusyLine:
                        is_onBusyLine=False
                    queue.append((path + [nxt], is_onBusyLine))
                    visited.append(nxt)
                    is_onBusyLine=False
                    
    return []

def razm():
    top = Tk()  
    e1 = StringVar() 
    e2 = StringVar() 
    e3 = StringVar() 
    top.title = "RuD3mon"
    top.geometry("400x250")  
    top['background']='#ffd3e1'
    entry1 = Entry(top,textvariable=e1, width=5).place(x = 82, y = 50)  
    entry2 = Entry(top,textvariable=e2,width=10).place(x = 115, y = 90)  
    entry3 = Entry(top,textvariable=e3,width=10).place(x = 70, y = 130)  
    def button_clck():
        global resp1
        global resp2
        global resp3
        resp1 = e1.get()
        resp2 = e2.get()
        resp3 = e3.get()
        top.destroy()

    name = Label(top, text = "Размер").place(x = 30,y = 50)  
    name1 = Label(top, text = "(Вид:N*M)").place(x = 125,y = 50)  
    email = Label(top, text = "Break ключи").place(x = 30, y = 90)  
    emeil1 = Label(top, text = "(Вид:1 a,2 b)").place(x = 200,y = 90)  
    password = Label(top, text = "Путь").place(x = 30, y = 130)  
    password1 = Label(top, text = "(Вид:a 1,b 2)").place(x = 155,y = 130)  
    sbmitbtn = Button(top, text = "Сгенерировать карту",activebackground = "pink", activeforeground = "blue", command=button_clck).place(x = 30, y = 170)  
    top.mainloop() 

def pole(x,y,c,v):
    mmap = [] 
    global allpaths
    n = x
    m = y
    print(c)
    break_point = deepcopy(c)
    errors = c
    for i in range(len(errors)):
        errors[i][0] = int(errors[i][0])
        errors[i][1] = ord(errors[i][1])-ord('a')
    ins = [] 
    outs = [] 
    for i in range(len(v)):
        ins.append((0,ord(v[i][0])-ord('a')))
        outs.append((int(v[i][1])-1,m))
    putya = []
    for y in range(m+1): 
        mmap.append([]) 
        for x in range(n+1): 
            if errors!= '':
                if [x, y] in errors: 
                    for e in errors: 
                        if e == [x,y]: mmap[-1].append('#') 
                else: mmap[-1].append('*')
            else:
                mmap[-1].append('*')

    starts = []
    for i in range(len(ins)): 
        line = bfs(mmap, ins[i], outs[i]) 
        if len(line)> 0:
            starts.append(line.pop(0))
            putya.append(line)
        else:
            putya.append(line)
        allpaths.append([])
        for l in line: 
            allpaths[-1].append(l[::-1]) 
    
    for p in range(len(putya)):
        if len(putya[p])> 0:
            putya[p] = [starts[p]] + putya[p]
    print(putya)
    

    mapn = 800//(n-1)
    mapm = 800//(m-1)
    pg.init()
    sc = pg.display.set_mode((1000, 1000))
    sc.fill((255,234,255))


    f1 = pg.font.Font('appetite-italic.ttf', 55) # 7*10 3 f b 3,f 4b3
    text1 = f1.render("RuD3mon", True, (254, 111,94))
    sc.blit(text1, (377, 30))

    n-=1
    m-=1
    helper = 0
    for i in range(100,901,800//m):
        pg.draw.line(sc, (0,0,0), [100,i], [900,i], width=5)
        f1 = pg.font.Font('appetite-italic.ttf', 36)
        text1 = f1.render(chr(helper + ord('a')) , True, (123, 160,91))
        sc.blit(text1, (60, i-15))
        helper+=1
    helper = 1
    for i in range(100,901,800//n):
        pg.draw.line(sc, (0,0,0), [i,100], [i,900], width=5)
        f1 = pg.font.Font('appetite-italic.ttf', 36)
        text1 = f1.render(str(helper), True, (123, 160,91))
        sc.blit(text1, (i-7, 915))
        helper+=1
    for i in range(len(break_point)):
        break_point[i][1] = ord(break_point[i][1]) - ord('a')
    for i in range(len(break_point)):
        pg.draw.rect(sc, (255,234,255), (80 + break_point[i][0]*800//n, 80 + break_point[i][1]*800//m, 40, 40))
        pg.draw.rect(sc, (180, 0, 0), (80 + break_point[i][0]*800//n, 80 + break_point[i][1]*800//m, 40, 40),8)
    pg.display.update()
    colors = [(255,20,147),(255, 255, 0),(102,255,0),(220,20,60)]
    for i in range(len(putya)):
        if len(putya[i]) > 0:
            for j in range(len(putya[i])-2):
                hela,helb = 100 + (putya[i][j][0])*mapm, 100 + (putya[i][j][1])*mapn
                hela1,helb1 = 100 + (putya[i][j+1][0])*mapm, 100 + (putya[i][j+1][1])*mapn
                print(hela,helb,hela1,helb1)
                pg.draw.line(sc, colors[i], [helb,hela], [helb1,hela1], width=15)
                pg.display.update()
                sleep(0.3)
        else:
            messagebox.showerror('Python Error', 'Error: This is an Error Message!')

    print(mmap)

if __name__ == '__main__':
    allpaths = []
    pg.init()
    resp1,resp2,resp3 = '','',''
    razm()
    a,b = [int(i) for i in resp1.split('*')]
    resp2 = [[j for j in i.split()] for i in resp2.split(',')]
    resp3 = [[j for j in i.split()] for i in resp3.split(',')]
    if resp2!= [[]]:
        spis = []
        for i in range(len(resp2)):
            resp2[i][0] = int(resp2[i][0]) - 1
        pole(a,b,resp2,resp3)
    else:
        pole(a,b,'',resp3)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()