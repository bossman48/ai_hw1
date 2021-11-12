from pyamaze import maze,agent,COLOR,textLabel
import time
def dijkstra(m,*h,start=None):
    if start is None:
        start=(m.rows,m.cols)

    hurdles=[(i.position,i.cost) for i in h]
    i=0

    unvisited={n:float('inf') for n in m.grid}
    unvisited[start]=0
    visited={}
    revPath={}
    while unvisited:
        currCell=min(unvisited,key=unvisited.get)
        visited[currCell]=unvisited[currCell]
        i=i+1
        if currCell==m._goal:
            break
        for d in 'EWNS':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in visited:
                    continue
                tempDist= unvisited[currCell]+1
                for hurdle in hurdles:
                    if hurdle[0]==currCell:
                        tempDist+=hurdle[1]

                if tempDist < unvisited[childCell]:
                    unvisited[childCell]=tempDist
                    revPath[childCell]=currCell
        unvisited.pop(currCell)
    
    fwdPath={}
    cell=m._goal
    while cell!=start:
        fwdPath[revPath[cell]]=cell
        cell=revPath[cell]
    print("Path Cost: "+str(i))
    return fwdPath,visited[m._goal]
            



if __name__=='__main__':
    myMaze=maze(200,200)
    #myMaze.CreateMaze(1,4,loopPercent=100)
    myMaze.CreateMaze(loadMaze='200x200_2.csv')

    h1=agent(myMaze,4,4)
    h2=agent(myMaze,4,6)
    h3=agent(myMaze,4,1)
    h4=agent(myMaze,4,2)
    h5=agent(myMaze,4,3)

    h1.cost=0
    h2.cost=0
    h3.cost=0
    h4.cost=0
    h5.cost=0
    time1=time.time()*1000

    path,c=dijkstra(myMaze,h1,h2,h2,h3,h4,h5)
    #path=dijkstra(myMaze)

    # a=agent(myMaze,color=COLOR.cyan,filled=True,footprints=True)
    #a=agent(myMaze,6,1,color=COLOR.cyan,filled=True,footprints=True)
    a=agent(myMaze,color=COLOR.cyan,filled=True,footprints=True)
    time2=time.time()*1000
    
    l=textLabel(myMaze,'Completion period:',time2-time1)
    l=textLabel(myMaze,'Path Length',len(path))

    myMaze.tracePath({a:path})


    myMaze.run()