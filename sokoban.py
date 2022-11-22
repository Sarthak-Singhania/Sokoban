f=open('E:/Programming/Sokoban/sampleCSD311.xsb','r')
a=f.read()

b=[i.split('\n')[1:-2] for i in a.split(';')[1:]]
# c=[]
# for i in b:
wall=[]
# player=[]
box=[]
goal=[]
ind=b[0]
for j in range(len(ind)):
    w=[]
    for x in range(len(ind[j])):
        if ind[j][x]=='#':
            w.append(1)
        else:
            w.append(0)
        if ind[j][x]=='@':
            player=(x+1,j+1)
        if ind[j][x]=='$':
            box.append((x+1,j+1))
        if ind[j][x]=='.':
            goal.append((x+1,j+1))
    wall.append(w)
f.close()
'''
' '-> floor
@->player
# -> wall
$ -> box
. -> goal
'''