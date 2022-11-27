import os

with open(,'r') as f:
	
	level = 0
	
	for line in f:
		if line.strip() == "":
			level += 1
			print("Level " + str(level))
			level_file = open('/level' + str(level),'w')
		else :
			level_file.write(line)