import bge
import mathutils
from math import *

count = 0

#Untuk mengganti ukuran gambar pake perintah ini bge.render.setWindowSize(width, height)
#untuk menggambar garis maka pake bge.render.drawLine(fromVec, toVec, color)

def mouseMovement(own):
	global count
	ww = bge.render.getWindowWidth()
	wh = bge.render.getWindowHeight()
	mouse = bge.logic.mouse
	own['mousePos'] = str(mouse.position)
	
	bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
	
	
	if count > 30:
		
		#bge.render.drawLine(own.position, [0,0,0], [255,0,0])
		
		pos = [0,0]
		pos[0] = mouse.position[0] - 0.5
		pos[1] = -(mouse.position[1] - 0.5)
		
		
		maxRotasi = 40
		sensitivitas = 10
		
		
		maxRotasi = radians(maxRotasi)
		sensitivitas = radians(sensitivitas)
		
		rotasi = own.localAngularVelocity.x
		rotasi2 = own.localAngularVelocity.y
		
		if rotasi > -maxRotasi or rotasi < maxRotasi:
			rotasi += pos[1] * sensitivitas
			
		if rotasi2 > - -maxRotasi or rotasi2 < maxRotasi:
			rotasi2 += pos[0] * sensitivitas
			
		own.localAngularVelocity.x = rotasi
		own.localAngularVelocity.y = rotasi2
	else:
		count += 1
	

def f01(cont):
	own = cont.owner
	
	sen = cont.sensors
	
	nosMaju = 5
	nosVertikal = 3
	mouseMovement(own)
	force = 0
	maxForward = 277
	maxBackward = 30
	forwardSpeed = 0.1
	backwardSpeed = 0.05
	forwardForce = 500
	backwardForce = 200
	maxVM = 200
	verticalMove = 0.05
	vm = 0
	
	rotasi = own.localAngularVelocity.z#inRadians
	maxRotasi = 20
	changeRot = 1
	
	
	maxRotasi = radians(maxRotasi)
	changeRot = radians(changeRot)
	firstSpeed = own.worldLinearVelocity
	fsForward = firstSpeed.length
	
	own['firstSpeed'] = str(fsForward)
	own['forwardSpeed'] = str(own.localLinearVelocity.y)
	
	
	keyW = sen['w'].positive
	keyS = sen['s'].positive
	keyA = sen['a'].positive
	keyD = sen['d'].positive
	naik = sen['Naik'].positive
	turun = sen['Turun'].positive
	nos = sen['NOS'].positive
	
	if keyW:
		force = forwardForce
		if own.localLinearVelocity.y < maxForward:
			if nos:
				own.localLinearVelocity.y += nosMaju
			else:
				own.localLinearVelocity.y += forwardSpeed
			pass
	if keyS:
		force = -backwardForce
		if own.localLinearVelocity.y > -maxBackward:
			if nos:
				own.localLinearVelocity.y -= nosMaju
			else:
				own.localLinearVelocity.y -= backwardSpeed
			pass
	if naik:
		vm = verticalMove
		if own.localLinearVelocity.z < maxVM:
			if nos:
				own.localLinearVelocity.z += nosVertikal
			else:
				own.localLinearVelocity.z += verticalMove
			pass
	if turun:
		if own.localLinearVelocity.z > -maxVM:
			if nos:
				own.localLinearVelocity.z -= nosVertikal
			else:
				own.localLinearVelocity.z -= verticalMove
			pass
			
	if keyA == 1 and keyD == 0:
		if rotasi < maxRotasi:
			rotasi += changeRot
	elif keyA == 0 and keyD == 1:
		if rotasi > -maxRotasi:
			rotasi -= changeRot
	
	
	
	own.localAngularVelocity.z = rotasi
	own.applyForce([0,force,0], True)
	finalSpeed = own.worldLinearVelocity
	
	own['finalRotZ'] = str(degrees(rotasi))
	own['finalSpeed'] = str(finalSpeed.length)