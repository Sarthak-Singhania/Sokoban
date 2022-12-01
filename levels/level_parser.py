"""
Group 10: ENTHIRAN

Group Members: 
Sarthak Singhania: 2010110898
Srikant Tripathi: 2010110770
Siddharth Sahu: 2010110623
Tushar Mishra: 2010110688
Devanshi Goel: 2010110218
"""



import os
def convert(path,directory):
	try:
		f=open(path,'r')
		level=1
		level_file=open(os.path.dirname(os.path.abspath(__file__))+f'\\{directory}'+"\\level"+str(level),'w')
		for i in f:
			if 'example' in i.lower():
				level_file.close()
				level_file=open(os.path.dirname(os.path.abspath(__file__))+f'\\{directory}'+"\\level"+str(level),'w')
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