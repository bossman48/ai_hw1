from pyamaze import maze,agent,textLabel
from queue import PriorityQueue
import math as m1
import time


def h(cell1,cell2):
    x1,y1=cell1
    x2,y2=cell2

    return m1.sqrt(pow(x1-x2,2) + pow(y1-y2,2))


def aStar(m):
    start=(m.rows,m.cols)
    g_score={cell:float('inf') for cell in m.grid}
    g_score[start]=0
    f_score={cell:float('inf') for cell in m.grid}
    f_score[start]=h(start,(1,1))
    i=0
    open=PriorityQueue()
    open.put((h(start,(1,1)),h(start,(1,1)),start))
    aPath={}
    while not open.empty():
        currCell=open.get()[2]
        if(open.qsize()>i):
            i=open.qsize()
        i=i+1
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:

                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score=g_score[currCell]+1
                temp_f_score=temp_g_score+h(childCell,(1,1))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell]= temp_g_score
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,h(childCell,(1,1)),childCell))
                    aPath[childCell]=currCell
    fwdPath={}
    cell=(1,1)
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    print("Expanded Nodes: "  +str(i))
    return fwdPath

if __name__=='__main__':
    m=maze(200,200)
    m.CreateMaze(loadMaze="200x200_2.csv")
    time1=time.time()*1000
    path=aStar(m)
    a=agent(m,footprints=True)
    time2=time.time()*1000
    m.tracePath({a:path})
    l=textLabel(m,'Completion period:',time2-time1)
    l=textLabel(m,'Path Length',len(path))

    m.run()