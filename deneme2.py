from pyamaze import maze,COLOR,agent
m=maze(200,200)
m.CreateMaze(loopPercent=2,saveMaze=True)

a=agent(m)
m.run()

