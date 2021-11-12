from pyamaze import maze,agent,COLOR,textLabel
import time
def BFS(m):
    i=0
    start=(m.rows,m.cols)
    frontier=[start]
    explored=[start]
    bfsPath={}
    while len(frontier)>0:
        currCell=frontier.pop(0)
        i=i+1
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                if childCell in explored:
                    continue
                frontier.append(childCell)
                explored.append(childCell)
                bfsPath[childCell]=currCell
    fwdPath={}
    cell=(1,1)
    while cell!=start:
        fwdPath[bfsPath[cell]]=cell
        cell=bfsPath[cell]
    print("Expanded Nodes: "+str(i))
    return fwdPath

if __name__=='__main__':
    size=200
    m=maze(size,size)
    m.CreateMaze(loadMaze="200x200_2.csv")
    time1=time.time()*1000
    path=BFS(m)
    a=agent(m,footprints=True,filled=True)
    time2=time.time()*1000
    m.tracePath({a:path})
    l=textLabel(m,'Completion period:',time2-time1)
    l=textLabel(m,'Path Length',len(path))

    m.run()