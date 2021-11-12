from pyamaze import maze,agent,COLOR,textLabel
import time

def DFS(m):
    i=0
    start=(m.rows,m.cols)
    explored=[start]
    frontier=[start]
    dfsPath={}
    while len(frontier)>0:
        currCell=frontier.pop()
        i=i+1
        if currCell==(1,1):
            break
        
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in explored:
                    continue
                explored.append(childCell)
                frontier.append(childCell)
                dfsPath[childCell]=currCell
    fwdPath={}
    cell=(1,1)
    while cell!=start:
        fwdPath[dfsPath[cell]]=cell
        cell=dfsPath[cell]
    print("Expanded Nodes: " +str(i))
    return fwdPath


if __name__=='__main__':
    m=maze(10,10)
    m.CreateMaze(loadMaze="10x10.csv")
    time1=time.time()*1000
    path=DFS(m)
  
    a=agent(m,footprints=True)
    time2=time.time()*1000
    m.tracePath({a:path})
    l=textLabel(m,'Completion period:',time2-time1)
    l=textLabel(m,'Path Length',len(path))


    m.run()