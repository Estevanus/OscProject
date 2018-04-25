'''
This osckey script is made by G. E. Oscar Toreh

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
import bge

def getKeyPressed():
	keyboard = bge.logic.keyboard
	tombol = bge.logic.keyboard.events
	
	for i in tombol:
		if keyboard.events[i] == 1:
			pilihan = bge.events.EventToCharacter(i, True)
			return pilihan

def getKeyPressed2():
	keyboard = bge.logic.keyboard
	tombol = bge.logic.keyboard.events
	
	for i in tombol:
		if keyboard.events[i] == 1:
			pilihan = bge.events.EventToString(i)
			return pilihan
			
def getModifierKeyPressed():
	keyboard = bge.logic.keyboard
	pressed = None
	if keyboard.events[bge.events.CAPSLOCKKEY] == 1:
		pressed = 'CAPSLOCKKEY'
	if keyboard.events[bge.events.LEFTCTRLKEY] == 1:
		pressed = 'LEFTCTRLKEY'
	if keyboard.events[bge.events.LEFTALTKEY] == 1:
		pressed = 'LEFTALTKEY'
	if keyboard.events[bge.events.RIGHTALTKEY] == 1:
		pressed = 'RIGHTALTKEY'
	if keyboard.events[bge.events.RIGHTCTRLKEY] == 1:
		pressed = 'RIGHTCTRLKEY'
	if keyboard.events[bge.events.RIGHTSHIFTKEY] == 1:
		pressed = 'RIGHTSHIFTKEY'
	if keyboard.events[bge.events.LEFTSHIFTKEY] == 1:
		pressed = 'LEFTSHIFTKEY'
	return pressed

def getKeyPress():
	keyboard = bge.logic.keyboard
	tombol = bge.logic.keyboard.events
	
	pressKeys = []
	
	for i in tombol:
		if keyboard.events[i] == 2:
			pilihan = bge.events.EventToCharacter(i, True)
			pressKeys.append(pilihan)
			
	return pressKeys
	
def getMouseEve(threshold):
	p = None
	
	
def getMouseEvents(threshold):
	mouse = bge.logic.mouse
	bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
	
	m = {0:[], 1:[], 2:[], 3:[]}
	
	mPos = [mouse.position[0] - 0.5, mouse.position[1] - 0.5]
	
	m[mouse.events[bge.events.LEFTMOUSE]].append('LEFTMOUSE')
	m[mouse.events[bge.events.MIDDLEMOUSE]].append('MIDDLEMOUSE')
	m[mouse.events[bge.events.RIGHTMOUSE]].append('RIGHTMOUSE')
	m[mouse.events[bge.events.WHEELUPMOUSE]].append('WHEELUPMOUSE')
	m[mouse.events[bge.events.WHEELDOWNMOUSE]].append('WHEELDOWNMOUSE')
	if mPos[0] > threshold or mPos[0] < -threshold:
		m[mouse.events[bge.events.MOUSEX]].append('MOUSEX')
	if mPos[1] > threshold or mPos[1] < -threshold:
		m[mouse.events[bge.events.MOUSEY]].append('MOUSEY')
	
	#print(m)
	return m