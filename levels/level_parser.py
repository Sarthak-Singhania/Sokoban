import os

f=open("C:/Users/Sarthak/Downloads/projectTest.xsb",'r')
level=1
level_file=open(os.path.dirname(os.path.abspath(__file__))+'\\sir'+"\\level"+str(level),'w')
for i in f:
	if 'Example' in i:
		level_file.close()
		level_file=open(os.path.dirname(os.path.abspath(__file__))+'\\sir'+"\\level"+str(level),'w')
		level+=1
	else:
		if i.strip()!='':
			level_file.write(i)
f.close()