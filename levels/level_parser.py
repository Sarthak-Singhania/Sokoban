import os

f=open("C:/Users/Sarthak/Downloads/projectTest.xsb",'r')
level=1
level_file=open("level"+str(level),'w')
for i in f:
	if 'Example' in i:
		level_file.close()
		level_file=open("level"+str(level),'w')
		level+=1
	else:
		if i.strip()!='':
			level_file.write(i)
f.close()
	


# with open("C:/Users/Sarthak/Downloads/projectTest.xsb",'r') as f:
	
# 	level = 0
	
# 	for line in f:
# 		print("Level " + str(level))
# 		level_file = open('/level' + str(level),'w')
# 		if 'Example' not in line:
# 			if line.strip() == "":
# 				level += 1
# 				level_file.close()
# 			else :
# 				level_file.write(line)