import os
def convert(path):
	try:
		f=open(path,'r')
		level=1
		level_file=open(os.path.dirname(os.path.abspath(__file__))+'\\sir'+"\\level"+str(level),'w')
		for i in f:
			if 'example' in i.lower():
				level_file.close()
				level_file=open(os.path.dirname(os.path.abspath(__file__))+'\\sir'+"\\level"+str(level),'w')
				level+=1
			else:
				if i.strip()!='':
					level_file.write(i)
		f.close()
		level_file.close()
		return 'Converted'
	except Exception as e:
		print(e)
		return False