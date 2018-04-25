import bge


frameCount = 0


def main(cont):
	keyboard = cont.sensors['Keyboard']
	mouseOver = cont.sensors['mouseOver']
	mouseClick = cont.sensors['MouseClick']
	
	
	global frameCount
	if frameCount == 0:
		print('Main System running at frame 0')
		
	
	
	frameCount += 1
	
	