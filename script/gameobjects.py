'''
This is gameobjects script made by G. E. Oscar Toreh.
This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.


This script is playing critical role in this game.
'''

import bge
import sys
import var
import triggerList
import mainscript
import videoPlayer
import checker
import datetime
from json import loads as muat
import json
from mathutils import Vector, Euler
from math import hypot, radians, degrees, cos, sin, atan, asin, acos, sqrt
import HUD
from weapons import rTimeLeft, setWeapons, weapons
import datetime
import osckey
import oscmath
import db
import random

Look = 'Look'
interceptPoint = 'interceptPoint'

nope = bge.logic.KX_INPUT_NONE
jaktif = bge.logic.KX_INPUT_JUST_ACTIVATED
aktif = bge.logic.KX_INPUT_ACTIVE
lepas = bge.logic.KX_INPUT_JUST_RELEASED

keyboard = bge.logic.keyboard
keyev = keyboard.events
mouse = bge.logic.mouse
moev = mouse.events
'''
keymap = var.globalDict['control']['control_tank']

changeCamera = keyev[bge.events.CKEY]

n0 = keyev[bge.events.ZEROKEY]
n1 = keyev[bge.events.ONEKEY]
n2 = keyev[bge.events.TWOKEY]
n3 = keyev[bge.events.THREEKEY]
n4 = keyev[bge.events.FOURKEY]
n5 = keyev[bge.events.FIVEKEY]
n6 = keyev[bge.events.SIXKEY]
n7 = keyev[bge.events.SEVENKEY]
n8 = keyev[bge.events.EIGHTKEY]
n9 = keyev[bge.events.NINEKEY]

def deltaTimeToSeconds(dt):
	s = float(dt.days) * 24 * 60 * 60 + float(dt.seconds) + (dt.microseconds / 1000000)
	return s
	
def rTimeLeft(jarak, reloadTime):
	s = deltaTimeToSeconds(jarak)
	return reloadTime - s
'''

# ----------------------------------------- Comander Section -----------------------------------------
class KX_Commander(bge.types.KX_GameObject):
	def __init__(self):
		self.useBy = 'bot'
		self.team = 1
			
	useBy = 'bot'
	team = 1
	
	def run(self):
		if self.useBy == 'bot':
			if self.team == 1:
				if var.botCommanderTeamA != None:
					var.botCommanderTeamA.run()
			if self.team == 2:
				if var.botCommanderTeamB != None:
					var.botCommanderTeamB.run()
		else:
			pass
			#script for player if player reach a commander rank already
			
#commanderControllerObject
def runCommanderController(cont):
	cont.owner.run()
# ----------------------------------------------------------------------------------------------------

def setCamPos(cont):
	var.player.setCamPos()
	print("pros cam has been set")
	for i in cont.actuators:
		cont.activate(i)

def event(keymap, keyev, moev, e):
	key = keymap[e]
	if key in keyev:
		return keyev[key]
	if key in moev:
		mouse = bge.logic.mouse
		if key == bge.events.MOUSEX:
			return (mouse.position[0] - 0.5) * 2
		elif key == bge.events.MOUSEY:
			return (mouse.position[1] - 0.5) * 2
		else:
			return moev[key]
		
def cek(keymap, e):
	keyev = keyboard.events
	moev = mouse.events
	print("the key is {0} neh".format(str(keymap[e])))
	#print(keyev)
	if keymap[e] in keyev:
		return keyev[keymap[e]]
	if keymap[e] in moev:
		return moev[keymap[e]]

class KX_ControlPoints(bge.types.KX_GameObject):
	defBy = 0
	type = "captureable"
	timeToLoseControl = 180#dipakai saat pemain menghilangkan control dari team lain
	timeToGainControl = 180#dipakai saat pemain meng gain control terhadap cp tersebut
	balance = 0
	def __init__(self, old_owner):
		self.defBy = self['defBy']
		
	
	#karena ini game mo beking ta optimize di low speck pc maka qt nda mo pake tuh run() dulu
	#jadi nda mo pake tuh auto regain control lagi sehingga dp regain controlnya manual
	def playerInsideCap(self, anyone):
		#nanti dulu qt taruh tare dp script, mo utamakan ka bot dulu
		pass

def resetAntrian(withUserToo = True):
	if withUserToo == False:
		for t in var.spawnLocByTeam:
			for sp in t:
				if var.PCO in sp.antrian:
					sp.antrian = []
					sp.antrian.append(var.PCO)
				else:
					sp.antrian = []

class KX_SpawnPoint(bge.types.KX_GameObject):
	antrian = []
	inUse = False
	team = 1
	def __init__(self, old_owner):
		self.antrian = []
		self.inUse = False
		self.team = 1
		self["daftar antri"] = str(self.antrian)
		self.addDebugProperty("daftar antri")
		if 'tim' in self:
			self.team = self['tim']
			
	def onPlayerLeavingSpawnRadius(self):
		#script pake bersama2 deng sensor near
		pass
	def onUpdateAntrian(self):
		pass
	
	def updateAntrian(self, player):
		if player not in self.antrian:
			self.antrian.append(player)
			self["daftar antri"] = str(self.antrian)
			self.onUpdateAntrian()
			
	def delAntrian(self, player):
		if player in self.antrian:
			del self.antrian[self.antrian.index(player)]
			self["daftar antri"] = str(self.antrian)
			
	def resetAntrian(self, withUserToo = True):
		if withUserToo == False:
			if var.PCO in self.antrian:
				self.antrian = []
				self.antrian.append(var.PCO)
				self.inUse = True
			else:
				self.antrian = []
				self.inUse = False
		else:
			self.antrian = []
		self["daftar antri"] = str(self.antrian)
		
			
	def setInUse(self):
		self.inUse = True
	def setNotUse(self):
		self.inUse = False
		self.onPlayerLeavingSpawnRadius()
		
def rotateL(obj):
	if 'rot_speed' in obj:
		obj.applyRotation([obj['rot_speed'], 0, 0], True)
	else:
		obj.applyRotation([0.2, 0, 0], True)
def rotateR(obj):
	if 'rot_speed' in obj:
		obj.applyRotation([-obj['rot_speed'], 0, 0], True)
	else:
		obj.applyRotation([-0.2, 0, 0], True)
		
class mouseLook(bge.types.KX_GameObject):
	resetTime = 1.0
	isLocalX = False
	isResetCam = False
	resetStats = 'waiting'
	xCount = 0
	zCount = 0
	spX = 0.0
	spZ = 0.0
	tickRate = bge.logic.getLogicTicRate()
	def __init__(self, old_owner):
		self.enableAxisX = True
		if 'enableAxisX' in self:
			self.enableAxisX = self['enableAxisX']
		self.isLocalX = False
		if 'isLocalX' in self:
			self.isLocalX = self['isLocalX']
		self.enableAxisY = True
		if 'enableAxisY' in self:
			self.enableAxisY = self['enableAxisY']
		if 'resetTime' in self:
			self.resetTime = self['resetTime']
		self.isEnable = True
		if 'isEnable' in self:
			self.isEnable = self['isEnable']
		if 'isResetCam' in self:
			self.isResetCam = self['isResetCam']
		self.lastPos = [bge.logic.mouse.position[0], bge.logic.mouse.position[1]]
		#self.lastPos = [0,0]
		self.tiksBeforeReset = 3
		self.tiksForReset = 0
		self.rotX = 0.0
		self.rotZ = 0.0
		#self.sensitivity = 0.2
		self.maxRotX = 90
		if 'maxRotX' in self:
			self.maxRotX = self['maxRotX']
		self.minRotX = -90
		if 'minRotX' in self:
			self.minRotX = self['minRotX']
		self.maxRotZ = 180
		if 'maxRotZ' in self:
			self.maxRotZ = self['maxRotZ']
		self.minRotZ = -180
		if 'minRotZ' in self:
			self.minRotZ = self['minRotZ']
		self.resetX = False
		self.resetY = False
		if 'resetX' in self:
			self.resetX = self['resetX']
		if 'resetY' in self:
			self.resetY = self['resetY']
			
		#testSowMouse
		#bge.logic.mouse.visible = True
			
	def run(self):
		if self.isEnable == True:
			mo = bge.logic.mouse
			mousePos = [mo.position[0], mo.position[1]]
			#this should be linked to global settings
			sensitivity = var.soldierLookSensitivity
			'''
			jx = mousePos[0] - self.lastPos[0]
			jy = mousePos[1] - self.lastPos[1]
			jarak = (jx, jy)
			'''
			assign = (mo.position[0], mo.position[1])
			jarak = (mousePos[0] - self.lastPos[0], mousePos[1] - self.lastPos[1])
			if mousePos[0] + jarak[0] > 0.95:
				assign = (0.06, mousePos[1])
			if mousePos[0] + jarak[0] < 0.05:
				assign = (0.94, mousePos[1])
				
			mo.position = assign
			
			mPos = Vector(mousePos) - Vector((0.5, 0.5))
		
			#print([jarak, mPos])
			if self.enableAxisX == True:
				if self.isLocalX == True:
					self.applyRotation([0.0, 0.0, -mPos[0]*sensitivity], True)
				else:
					self.applyRotation([0.0, 0.0, -mPos[0]*sensitivity], False)
				self.rotZ -= degrees(-mPos[0]*sensitivity)
				#cek = self.rotZ
				#print(cek)
			if self.enableAxisY == True:
				if self.rotX + degrees(mPos[1]*sensitivity) > self.minRotX and self.rotX + degrees(mPos[1]*sensitivity) < self.maxRotX:
					self.applyRotation([-mPos[1]*sensitivity, 0.0, 0.0], True)
					#print("a --> " + str(self.rotX + degrees(mPos[1]*sensitivity)))
					self.rotX += degrees(mPos[1]*sensitivity)
					#print("b --> " + str(self.rotX))
			
			self.lastPos = [mo.position[0], mo.position[1]]
			
			#bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
			#that statement is moving to var.PCO.setMouseToCenterPerFrame
		else:
			if self.isResetCam == True:
				#algoritma untuk mengembalikan posisi kamera ke posisi semula
				#cek = self.resetStats, self.rotZ, self.rotX, self.spX, self.spZ, self.xCount, self.zCount
				#print(cek)
				#if self.parent == None:
				if 1 == 1:
					if self.resetStats == 'waiting':
						self.resetStats = 'memulai'
						try:
							self.spX = self.rotX / self.resetTime / self.tickRate
							self.xCount = self.rotX / self.spX
						except ZeroDivisionError:
							self.spX = 0.0
							cek = self.resetTime, self.tickRate, self.rotX
							#print('zero division error occur in spX info ' + str(cek))
							
						sisah = self.rotZ
						if self.rotZ > 360 or self.rotZ < -360:
							sisah = self.rotZ % 360
						self.rotZ = sisah
						try:
							self.spZ = sisah / self.resetTime / self.tickRate
							self.zCount = self.rotZ / self.spZ
						except ZeroDivisionError:
							cek = sisah, self.resetTime, self.tickRate, self.rotZ
							#print('zero division error occur in spZ info ' + str(cek))
					elif self.resetStats == 'memulai':
						xDone = False
						zDone = False
						if self.xCount > 0:
							self.applyRotation([radians(self.spX), 0.0, 0.0], True)
							self.rotX -= self.spX
							self.xCount -= 1
						else:
							xDone = True
						if self.zCount > 0:
							if self.isLocalX == True:
								self.applyRotation([0.0, 0.0, radians(self.spZ)], True)
							else:
								self.applyRotation([0.0, 0.0, radians(self.spZ)], False)
							self.rotZ -= self.spZ
							self.zCount -= 1
						else:
							zDone = True
							
						if xDone == True and zDone == True:
							self.resetStats = 'selesai'
						#cek = xDone, zDone
						#print('status xDone dan zDone ialah ' + str(cek))
						'''
						if self.xCount > 0 and self.zCount > 0:
							self.applyRotation([0.0, 0.0, radians(self.spZ)], False)
							self.applyRotation([radians(self.spX), 0.0, 0.0], True)
							self.rotX -= self.spX
							self.rotZ -= self.spZ
							self.xCount -= 1
							self.zCount -= 1
						else:
							self.resetStats = 'selesai'
						'''
					elif self.resetStats == 'selesai':
						if self.parent == None:
							#self.isResetCam = False
							#self.resetStats = 'waiting'
							pass
				else:
					#algoritma jika ada parent camnya
					#sdt = self.parent.worldOrientation.to_euler()
					sdt = self.localOrientation.to_euler()
					#self.applyRotation(sdt)
					self.resetStats = 'selesai'
		#rencananya mo beking rupa tu gun rot deng turret rot pe script noh
		
#script get_dimesion credits from https://blenderartists.org/forum/showthread.php?338711-How-to-get-an-Object-s-dimensions-in-the-BGE
def get_dimensions(obj):
    mesh = obj.meshes[0]
    collection = [[], [], []]
    for mat_index in range(mesh.numMaterials):
        for vert_index in range(mesh.getVertexArrayLength(mat_index)):
            vert_XYZ = mesh.getVertex(mat_index, vert_index).XYZ
            [collection[i].append(vert_XYZ[i]) for i in range(3)]
    return Vector([abs(max(axis)) + abs(min(axis)) for axis in collection])
	
def setUpVehicle(cont):
	own = cont.owner
	newVehicle = KX_VehicleObject(own)
	kamus = var.globalDict
	newVehicle.setCont(cont)
	newVehicle['vehicle'] = True
	setWeapons(newVehicle)
	return newVehicle
	'''
	for i in cont.actuators:
		#if i.name != "bot state":
		#	cont.activate(i)
		cont.activate(i)
	'''
		
def setPlayerVehicle(own):
	cont = own.controllers['Python']
	if 'type' in own:
		if own['type'] == 'airplane':
			#newVehicle = KX_AirPlaneObject(own)
			newVehicle = KX_VehicleObject(own)
	else:
		newVehicle = KX_VehicleObject(own)
	kamus = var.globalDict
	#newVehicle.setCont(cont)
	newVehicle['vehicle'] = True
	setWeapons(newVehicle)
	'''
	for i in cont.actuators:
		#if i.name != "bot state":
		#	cont.activate(i)
		cont.activate(i)
	'''
	return newVehicle
	
def jetControl(self):
	if "initializeMouseControl" not in self:
		self['initializeMouseControl'] = True
		
		'''
		if 'maxRotX' not in self:
			self['maxRotX'] = radians(40)
		if 'maxRotY' not in self:
			self['maxRotY'] = radians(40)
		if 'maxRotZ' not in self:
			self['maxRotZ'] = radians(15)
		'''
		
		self.lastPos = [bge.logic.mouse.position[0], bge.logic.mouse.position[1]]
		
	else:
		mo = bge.logic.mouse
		mousePos = [mo.position[0], mo.position[1]]
		assign = (mo.position[0], mo.position[1])
		jarak = (mousePos[0] - self.lastPos[0], mousePos[1] - self.lastPos[1])
		if self.enableMouseControl == True:
			if mousePos[0] + jarak[0] > 0.95:
				assign = (0.06, mousePos[1])
			if mousePos[0] + jarak[0] < 0.05:
				assign = (0.94, mousePos[1])
				
			mo.position = assign
			
			#importing modul yg diperlukan untuk kontrol
			keyev = keyboard.events
			moev = mouse.events
			
			#control sectiom
			self.turnL = event(self.keymap, keyev, moev, 'turnL')
			self.turnR = event(self.keymap, keyev, moev, 'turnR')
			self.rollRight = event(self.keymap, keyev, moev, 'rollRight')
			self.rollLeft = event(self.keymap, keyev, moev, 'rollLeft')
			self.pitchUp = event(self.keymap, keyev, moev, 'pitchUp')
			self.pitchDown = event(self.keymap, keyev, moev, 'pitchDown')
			
			self.jetControlTurning()
			self.lastPos = [mo.position[0], mo.position[1]]
			bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
		
def getMaxSpeed(akselerasi, damping):
	maxTime = akselerasi / damping
	currentSpeed = 0.0
	for i in range(int(maxTime)):
		currentSpeed += akselerasi - i * damping
	return currentSpeed
	
def jetEngine(self):
	maju = 0.0
	force = 0.0
	gravity = -var.mapKonfigurasi['gravity']
	#gravity = 9.8
	#print('ok')
	faktorTanjakan = 1.0 - self.worldOrientation[2][1]
	self.faktorTanjakan = faktorTanjakan
	vx = self.localLinearVelocity.x
	vy = self.localLinearVelocity.y
	#vy = self.forwardVelocity
	vz = self.localLinearVelocity.z
	'''
	newton_local_x = 0.45 * 0.025 * self.plane_size_x * (vx)**2
	newton_local_y = 0.45 * 0.025 * self.plane_size_y * (vy)**2
	newton_local_z = 0.45 * 0.025 * self.plane_size_z * (vz)**2
	
	diakselerasi_local_x = newton_local_x / self.mass / bge.logic.getLogicTicRate()
	diakselerasi_local_y = newton_local_y / self.mass / bge.logic.getLogicTicRate()
	diakselerasi_local_z = newton_local_z / self.mass / bge.logic.getLogicTicRate()
	'''
	
	#damping = 0.3
	#damping = self.linearDamping
	
	#self.forwardVelocity = diakselerasi_local_y
	gravityFactor = self.worldOrientation[2][1] * gravity * (1.0 - self.worldLinearVelocity.z / self.maxSpeed)
	currentAngularVelocity = self.getAngularVelocity(True)
	sx = sin(currentAngularVelocity[0] / bge.logic.getLogicTicRate())
	
	pitchFactor = 1.0
	if sx < 0:
		pitchFactor = sx + 1.0
	else:
		pitchFactor = 1.0 - sx
	#print([pitchFactor, sx, currentAngularVelocity[0], sx > 1, sx < -1])
	#print([pitchFactor, sx, currentAngularVelocity[0], self.forwardVelocity])
	#print(pitchFactor)
	#pitchFactor = 1.0 - sin((currentAngularVelocity[0] - self.lastAngularVelocity[0]) / bge.logic.getLogicTicRate())
	rollFactor = sin(currentAngularVelocity[1] - self.lastAngularVelocity[1])
	yawFactor = 1.0 - sin(currentAngularVelocity[2] - self.lastAngularVelocity[2])
	'''
	if pitchFactor < 0:
		pitchFactor *= -1
	if rollFactor < 0:
		rollFactor *= -1
	if yawFactor < 0:
		yawFactor *= -1
	'''
	self.forwardVelocity -= gravityFactor / bge.logic.getLogicTicRate()
	momentumUdara = var.mapKonfigurasi['masaUdara'] * self.plane_size_y
	momentumVehicle = self.forwardVelocity * self.mass
	if self.maju == 2:
		#self.forwardVelocity += (self.akselerasi - (gravity * self.worldOrientation[2][1]))
		#print([self.forwardVelocity, diakselerasi_local_y])
		#maju = self.forwardSpeed
		#force = self.forwardForce
		v = self.akselerasi * (1.0 - vy / self.maxSpeed)
		
		#vy += self.akselerasi
		#self.forwardVelocity = oscmath.airResistance(vy*self.mass*1000, 1.25, 0.33, 1.8)
		
		#acc = (self.akselerasi / bge.logic.getLogicTicRate())
		#self.forwardVelocity = acc + (momentumVehicle - momentumUdara)  / self.mass
		
		self["acc"] = str(v)
		#print(v)
		self.forwardVelocity += v / bge.logic.getLogicTicRate()
	else:
		#karena udarah itu tidak bergerak jadi velocity udarah ialah 0 maka tak perlu dikalikan lagi karna bisa memberi pengaru 0 pada momentumnya
		if self.mundur:
			if self.forwardVelocity < 0.0:
				self.forwardVelocity -= 0.05
			else:
				self.forwardVelocity = (momentumVehicle - momentumUdara * 4)  / self.mass
		else:
			if self.forwardVelocity > 0.0:
				self.forwardVelocity = (momentumVehicle - momentumUdara)  / self.mass
				if self.forwardVelocity < 0.0:
					self.forwardVelocity = 0.0
			elif self.forwardVelocity < 0.0:
				self.forwardVelocity = -(-momentumVehicle - momentumUdara)  / self.mass
				if self.forwardVelocity > 0.0:
					self.forwardVelocity = 0.0
	#self.forwardVelocity *= pitchFactor * rollFactor * yawFactor
	#self.forwardVelocity *= pitchFactor
	self.forwardVelocity *= (pitchFactor + (1 - pitchFactor) / 2)
	self.localLinearVelocity.y = self.forwardVelocity
	
	g = gravity * self.mass
	
	
	vwx = self.worldLinearVelocity.x
	vwy = self.worldLinearVelocity.y
	
	vvw = hypot(vwx, vwy)#vertical world velocity
	
	if vvw < 0.0:
		vvw *= -1
	
	#speedToLift is velocity m/s that plane needed to lift
	if vy <= self.speedToLift:
		self.liftForce = vvw / self.speedToLift * g * faktorTanjakan
	else:
		self.liftForce = g * faktorTanjakan
		
	#print([vvw, self.liftForce, g, vy])
	self.applyForce([0.0, 0.0, self.liftForce])
	
	for i in self.jet_engines:
		i.run()
	
	#get last measurement
	self.lastFaktorTanjakan = faktorTanjakan
	self.lastAngularVelocity = self.getAngularVelocity(True)
	
	# ------------- Debugging Section ------------- #
	if var.ngecek == True:
		self['vel'] = str(vy)
		self.addDebugProperty('vel')
		kpj = int(vy * 3.6)
		self['km/h'] = str(kpj)
		self.addDebugProperty('km/h')
		self.addDebugProperty('acc')
		self['maxSpeed m/s'] = int(self.maxSpeed)
		self['maxSpeed km/s'] = int(self.maxSpeed * 3.6)
		self.addDebugProperty('maxSpeed m/s')
		self.addDebugProperty('maxSpeed km/s')
	# --------------------------------------------- #

class simpleObject:
	invalid = True
class CL_DummyObject:
	def __init__(self, object, applyAs = "position"):
		if hasattr(object, "position"):
			self.position = object.position
		else:
			self.position = Vector((0, 0, 0))
		self.worldLinearVelocity = Vector((0, 0, 0))
		if type(object) == Vector:
			if applyAs == 'position':
				self.position = object
			if applyAs == 'worldLinearVelocity':
				self.worldLinearVelocity = object
def jalankan(cont):
	cont.owner.run()
	
# ----------------------------- Effects Section -----------------------------
class KX_SimpleEffect(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		self.owner = None
		self.subEffects = []
		for i in self.childrenRecursive:
			if 'activeOn' in i:
				self.subEffects.append(i)
				
	def run(self):
		#cek = self.owner, self
		#print("ceking KX_SimpleEffect ref: " + str(cek))
		if self.owner != None:
			if self.owner.invalid == False:
				try:
					#if self.owner.__getattribute__(i['activeOn']) == 2:
					#keyev = keyboard.events
					#moev = mouse.events
					if 'affection' in self:
						if self['affection'] == 'show':
							#if event(self.owner.keymap, keyev, moev, self['activeOn']) > 1:
							et = "self.owner." + self['activeOn']
							t = eval(et)
							if t > 1:
								self.visible = True
							else:
								self.visible = False
					else:
						cek = self, 'KX_SimpleEffect'
						print('affection property not found ref:' + str(cek))
						bge.logic.endGame()
					#I just realize that this gonna effect all object with a same material even though other object does not use it
				except:
					cek = self, 'KX_SimpleEffect'
					print('some key doens not in control list. Ref : ' + str(cek))
					checker.getInfo()
					bge.logic.endGame()
# ---------------------------------------------------------------------------
	
def setTextScoreBoardTextAdder(cont):
	sca = KX_PlayerScoreTextAdder(cont.owner)
	#cek = sca
	#print(">>>>>>>>>>>>>>>>>>>>>>>>>>> asd <<<<<<<<<<<<<<<<<<<<<<<<<<<<< {0}".format(str(cek)))
	
# ------------------------------ MISC Section ------------------------------ 
class KX_VideoPlayer(bge.types.KX_GameObject):
	daftarVideo = []
	f = open(var.thisLok + 'init movie.txt')
	d = f.read()
	f.close()
	daftarVideo = d.split('\n')
	currentVideo = None
	indeks = 0
	status = None
	def __init__(self, old_owner):
		pass
	def run(self):
		self.status = videoPlayer.simplePlayer(self, self.daftarVideo[0])
		pass
		
class KX_TextPlane(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		self.textObject = None
		self.replaceText = None
		self.replaceTo = ''
		self.relation = None
		#self.scale = 1
		self.text = 'nama map'
		for i in self.children:
			if type(i) == bge.types.KX_FontObject:
				self.textObject = i
		if self.textObject == None:
			cek = self, id(self)
			print("textObject not found. Reff : KX_TextPlane, " + str(cek))
			bge.logic.endGame()
	def setText(self, text):
		self.text = text
		#cek = type(self.text), dir(self)
		#print("text bertipekan " + str(cek))
		if self.replaceText == None:
			self.textObject.text = ">>" + self.text
		else:
			if self.replaceText in self.text:
				self.textObject.text = ">>" + self.text.replace(self.replaceText, self.replaceTo)
			else:
				self.textObject.text = ">>" + self.text
			#self.textObject.text = ">>" + self.text.replace('.blend', '')
	def setScale(self, scale):
		#self.textObject.scaling = [scale, scale, scale]
		self.scaling = [scale, scale, scale]
	def run(self):
		pass
		
class KX_KeyBinding(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		self.textSize = 1.0
		self.mOver = None
		self.lastOverOn = None
		self.isInEditMode = False
		self.selectedKeyBind = None
		self.blinkingText = False
		self.tempEditedText = ""
		self.textTicks = 0
		self.daftarKeyBinding = []
		self.threshold = 0.1
		if 'threshold' in self:
			self.threshold = self['threshold']
		if 'mOver' in self.sensors:
			if type(self.sensors['mOver']) == bge.types.KX_MouseFocusSensor:
				self.mOver = self.sensors['mOver']
			else:
				print('mOver sensor is not a mouse over type')
				bge.logic.endGame()
		else:
			print("mouse over sensors not found")
			bge.logic.endGame()
		self.daftarKeyBind = {}
		if 'textSize' in self:
			self.textSize = self['textSize']
		self.showKeyList = None
		if 'showKeyList' in self:
			self.showKeyList = self.scene.objects[self['showKeyList']]
		self.showKeyBindList = None
		if 'showKeyBindList' in self:
			self.showKeyBindList = self.scene.objects[self['showKeyBindList']]
		
		if self.showKeyList == None and self.showKeyBindList == None:
			print('showKeyList and showKeyBindList not found. Exiting...')
			bge.logic.endGame()
			
		self.control = None
		self.cfg = None
		if 'lastSelectionControl' in var.globalDict:
			#self.control = var.globalDict['lastSelectionControl']
			#lok = var.thisLok + "\\cfg\\control.json"
			lok = var.cfgLok
			control = muat(open(lok).read())
			self.cfg = control
			self.control = control[var.globalDict['lastSelectionControl']]
		
		if self.control == None:
			print('control is None. Exiting...')
			bge.logic.endGame()
		else:
			if 'keyTextObject' in self and 'keyBindTextPlane' in self:
				for i in self.control:
					added = self.scene.addObject(self['keyTextObject'], self.showKeyList)
					added.text = i
					added.scaling = [self.textSize, self.textSize, self.textSize]
					self.showKeyList.position.y -= self.textSize
					added.setParent(self)
					
					asd = self.scene.addObject(self['keyBindTextPlane'], self.showKeyBindList)
					added = KX_TextPlane(asd)
					added.relation = i
					added.replaceText = 'KEY'
					added.setText(self.control[i].replace("bge.events.", ""))
					added.scaling = [self.textSize, self.textSize, self.textSize]
					self.showKeyBindList.position.y -= self.textSize
					self.daftarKeyBinding.append(added)
					added.setParent(self)
					
			else:
				print('keyTextObject nor keyBindTextPlane is found. Exiting...')
				bge.logic.endGame()
			
	def run(self):
		if self.isInEditMode == False:
			if self.lastOverOn != None:
				if self.lastOverOn != self.mOver.hitObject:
					self.lastOverOn.visible = False
					pass
			if self.mOver.hitObject in self.daftarKeyBinding:
				if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_SENSOR_JUST_ACTIVATED:
					self.selectedKeyBind = self.mOver.hitObject
					self.isInEditMode = True
					pass
					
				self.mOver.hitObject.visible = True
				self.lastOverOn = self.mOver.hitObject
		else:
			#put here the editing code
			#self.tempEditedText = 'A'
			keyboard = bge.logic.keyboard
			pressed = ''
			if keyboard.events[bge.events.ENTERKEY] == 0:
				m = osckey.getMouseEvents(self.threshold)[2]
				if m == []:
					pressed = osckey.getKeyPressed2()
					if pressed == None:
						pressed = self.tempEditedText
				else:
					pressed = m[0]
			else:
				#apply choice
				pressed = self.tempEditedText
				self.selectedKeyBind.setText(pressed)
				#self.selectedKeyBind.setText('asdasdas')
				self.isInEditMode = False
				return False
			if pressed != None:
				self.tempEditedText = pressed
			if self.blinkingText == False:
				self.selectedKeyBind.textObject.text = self.tempEditedText + "|"
				if self.textTicks > 30:
					self.blinkingText = True
					self.textTicks = 0
			else:
				self.selectedKeyBind.textObject.text = self.tempEditedText + ""
				if self.textTicks > 30:
					self.blinkingText = False
					self.textTicks = 0
			self.textTicks += 1
			pass
	def save(self):
		for i in self.daftarKeyBinding:
			#cek = i.relation, i.text
			#print(cek)
			self.cfg[var.globalDict['lastSelectionControl']][i.relation] = 'bge.events.' + i.text
			with open(var.cfgLok, 'w') as f:
				json.dump(self.cfg, f, sort_keys = True, indent = 4)
			
# --------------------------------------------------------------------------
# --------------------- ScoreBoard Object Section ---------------------
class KX_PlayerScoreTextAdder(bge.types.KX_GameObject):
	nameText = None
	def __init__(self, old_owner):
		cek = 'nameText' in self, var.players
		print("checking in score section : " + str(cek))
		if 'nameText' in self:
			self.nameText = self['nameText']
			if self.nameText in self.scene.objectsInactive:
				#self.scene.addObject(self.nameText)
				for team in var.players:
					for player in team:
						sc = db.getLastScore(str(player))
						mp = db.getLastMapPlayedData(player.name)
						
						teks = self.scene.addObject(self.nameText, self)
						if 'scale' in self:
							teks.scaling = [self['scale'], self['scale'], self['scale']]
						#teks.text = str(player)
						if player.kill > 1:
							kill = str(player.kill) + " kills"
						else:
							kill = str(player.kill) + " kill"
							
						#teks.text = str(player) + " with " + kill + ' and ' + str(player.death) + " death and " + str(player.suicide) + " suicide. So the score is " + str(player.point)
						teks.text = str(player) + " with " + kill + ' and ' + str(player.teamkill) + ' teamkill and ' + str(player.suicide) + " suicide of " + str(player.death) + " death. So the score is " + str(player.point)
						
						total_kill = sc['kill'] + player.kill
						total_death = sc['death'] + player.death
						total_kill_assist = 0
						total_suicide = sc['suicide'] + player.suicide
						total_scores = sc['scores'] + player.point
						total_teamkill = sc['teamkill'] + player.teamkill
						total_damage_cause = sc['damageCause'] + player.damageCause
						total_damage_recieve = sc['damageRecieve'] + player.damageRecieve
						newHighScores = sc['highScores']
						if player.point > newHighScores:
							newHighScores = player.point
							
						db.updateScore(player.name, total_kill, total_death, total_kill_assist, total_suicide, total_scores, total_teamkill, newHighScores, total_damage_cause, total_damage_recieve)
						
						mapName = var.map
						win = 0
						if player.team == var.lastWiningTeam:
							win = 1
						else:
							win = -1
						winCount = mp['winCount'] + win
						loseCount = mp['loseCount'] + win
						timePlayed = var.lastTimePlayed + mp['timePlayed']
						db.updateMapPlayed(player.name, mapName, winCount, loseCount, timePlayed)
						
						#save the score
						var.db.commit()
						
						self.position.y -= teks.worldScale.y
						#teks.position.z = self.position.z
						print('Setting up pos of socre text at ' + str(teks.position))
			else:
				print("object not found. ref : gameobjects.KX_PlayerScoreTextAdder")
		else:
			print('error no nameText is insert. ref gameobjects.KX_PlayerScoreTextAdder')
# ---------------------------------------------------------------------

class KX_ScoreObject(str):
	def __init__(self, old_owner):
		self.team = None
		self.kill = 0
		self.death = 0
		self.kill_assist = 0
		self.teamkill = 0
		self.suicide = 0
		self.damageCause = 0.0
		self.damageRecieve = 0.0
		self.point = 0
		self.name = str(self)
	
# ------------------------------------ Pathfinding Section ------------------------------------ 
class KX_WayPoint(bge.types.KX_PolyProxy):
	def __init__(self, old_owner):
		self.radius = 50
		self.relation = []
		if 'relation' in self:
			temp = self['relation']
			temp = temp.replace('[','')
			temp = temp.replace(']','')
			if ',' in temp:
				self.relation = temp.split(',')
			else:
				self.relation = temp
				
class KX_WayMesh(bge.types.KX_NavMeshObject):
	def __init__(self, old_owner):
		m = self.meshes[0]
		for i in range(m.numPolygons):
			pol = m.getPolygon(i)
			mi = pol.getMaterialIndex()
			print(mi)
			var.waypoints.append(pol)
			#wp = KX_WayPoint(m.getPolygon(i))
			#var.waypoints.append(wp)
		#print(" ------------------- waypoints --------------------")
		#print(var.waypoints)
		#print(" ------------------- waypoints --------------------")
				
class pathNode:
	def __init__(self, node, owner):
		'node ialah polygon dari meshes'
		self.node = node
		self.relation = []
		self.resultNodes = []
		self.material_id = node.material_id
		self.owner = owner
		self.keepTracking = False
		self.alreadyInTrace = False
		self.debugThisObject = False
		self.rangeFromBefore = None
		self.jumlahTerpanggil = 0
		
		v1 = self.owner.mesh.getVertex(self.material_id, node.v1)
		v2 = self.owner.mesh.getVertex(self.material_id, node.v2)
		v3 = self.owner.mesh.getVertex(self.material_id, node.v3)
		v4 = self.owner.mesh.getVertex(self.material_id, node.v4)
		
		self.v1 = v1.getXYZ()
		self.v2 = v2.getXYZ()
		self.v3 = v3.getXYZ()
		self.v4 = v4.getXYZ()
		
		#misalnya dia track dari node A kemudian ke node B maka historynya kan tercatat disini untuk diturunkan ke node selanjutnya
		#dan ketika node yg berada di tujuan lah yang akan me return daftar akhirnya
		self.nodesFromBefore = []
		
		#self.wayOfOrder = None
		self.position = oscmath.getPolygonCenter(node, self.owner.obj)
		if 'dummyEmpty' in self.owner.obj.scene.objects:
			dem = self.owner.obj.scene.objects['dummyEmpty']
			dem.position = self.position
			if 'dummyObject' in self.owner.obj.scene.objectsInactive:
				self.debugGObject = self.owner.obj.scene.addObject('dummyObject', dem)
				self.debugGObject.visible = False
				'''
				'''
				if self.getDistanceTo(Vector((-837.598, -441.796, 170.819))) < 10.0:
					#self.debugGObject.visible = True
					self.debugThisObject = True
					pass
			else:
				self.debugGObject = None
		else:
			self.debugGObject = None
			
	def __repr__(self):
		return "Node Object with id " + str(id(self))
			
	def getDistanceTo(self, other):
		if type(other) == pathNode:
			V = Vector(other.position - self.position)
			return V.length
		if type(other) == Vector:
			V = Vector(other - self.position)
			#print(V.length)
			return V.length
		return 0
	def tellTheOthers(self):
		#cek = self, self.nodesFromBefore
		#print("it's working ref " + str(cek))
		#print(self)
		self.jumlahTerpanggil += 1
		jml = 0
		if self == self.owner.wayOfOrder:
			self.nodesFromBefore.append(self)
			self.owner.daftarWay = list(self.nodesFromBefore)
			for i in self.nodesFromBefore:
				if i.debugGObject != None:
					i.debugGObject.visible = True
					pass
			#self.owner.listOFWays.append(self.nodesFromBefore)
			self.owner.listOFWays[self.rangeFromBefore] = self.nodesFromBefore
			#print(self.nodesFromBefore)
			print("last node is " + str(self))
			print("panjang nodesFromBefore ialah : " + str(len(self.nodesFromBefore)))
			#print('ada jo kah?')
			self.nodesFromBefore = []
		else:
			'''
			if len(self.nodesFromBefore) > 0:
				return False
				#a quick break
			'''
			#ygTamaso = self.nodesFromBefore
			for i in self.relation:
				if i != self:
					if i not in self.nodesFromBefore:
						#self.owner.trackedNodes[self] = {}
						'''
						'''
						jarak = i.getDistanceTo(self)
						ok = False
						if self.rangeFromBefore == None:
							self.rangeFromBefore = 0
							ok = True
						if i.rangeFromBefore == None:
							i.rangeFromBefore = jarak + self.rangeFromBefore
						if jarak + self.rangeFromBefore <= i.rangeFromBefore:
								ok = True
								#cek = jarak + self.rangeFromBefore , i.rangeFromBefore, jarak + self.rangeFromBefore <= i.rangeFromBefore
								#print(cek)
						i.rangeFromBefore = jarak + self.rangeFromBefore
								
						if ok == True:
							i.nodesFromBefore = list(self.nodesFromBefore)
							i.nodesFromBefore.append(self)
							jml += 1
							#cek = i, i.relation
							#print("node of relation : " + str(cek))
							try:
								pass
								#print("nodesFromBefore ialah " + str(self.nodesFromBefore))
								i.tellTheOthers()
							except:
								checker.getInfo()
								bge.logic.endGame()
		if self.debugThisObject == True:
			print(" --------------------------- Hasil Relasi Dari node yg di debug --------------------------- ")
			cek = self.nodesFromBefore, jml, self
			print(cek)
			print(" ------------------------------------------------------------------------------------------ ")
		self.nodesFromBefore = []
				
class KX_WayMesh2:
	def __init__(self, navMeshObject, playerController):
		m = navMeshObject.meshes[0]
		self.mesh = m
		self.obj = navMeshObject
		self.wayOfOrder = None
		self.firstNode = None
		self.daftarWay = []
		self.listOFWays = {}
		self.playerController = playerController
		self.nodes = []
		self.chooePath = 'closer'
		if 'chooePath' in var.mapKonfigurasi:
			self.chooePath = var.mapKonfigurasi['chooePath']
		
		self.doneTracing = False
		self.distToChangeNode = 100.0
		if 'distToChangeNode' in navMeshObject:
			self.distToChangeNode = navMeshObject['distToChangeNode']
		if 'distToChangeNode' in navMeshObject:
			self.distToChangeNode = navMeshObject['distToChangeNode']
		for i in range(m.numPolygons):
			pol = m.getPolygon(i)
			mi = pol.getMaterialIndex()
			
			wp = pathNode(m.getPolygon(i), self)
			var.waypoints.append(wp)
			self.nodes.append(wp)
		self.rebuildNodes()
		#print(" ------------------- waypoints --------------------")
		#print(var.waypoints)
		#print(" ------------------- waypoints --------------------")
	def __repr__(self):
		return "<class KX_WayMesh2 at " + str(id(self) + ">")
	def rebuildTrackList(self, playerObject, wayOfOrder):
		#reseting values
		self.listOFWays = {}
		
		jarak = wayOfOrder.getDistanceTo(self.nodes[0].position)
		node = self.nodes[0]
		for i in self.nodes:
			#first reseting value of nodes
			i.rangeFromBefore = None
			i.jumlahTerpanggil = 0
			
			if i.debugGObject != None:
				i.debugGObject.visible = False
			i.keepTracking = True
			tempj = wayOfOrder.getDistanceTo(i.position)
			if tempj  < jarak:
				jarak = tempj
				node = i
		self.wayOfOrder = node
		#print("way of order is on " + str(self.wayOfOrder))
		
		
		jarak = playerObject.getDistanceTo(self.nodes[0].position)
		node = self.nodes[0]
		for i in self.nodes:
			tempj = playerObject.getDistanceTo(i.position)
			#cek = jarak, i.position, i
			#print(cek)
			if tempj < jarak:
				jarak = tempj
				node = i
			i.nodesFromBefore = []
		self.doneTracing = False
		self.firstNode = node
		node.tellTheOthers()
		
		#print("cek jumlah terpanggil")
		'''
		for i in self.listOFWays[0]:
			print(i.jumlahTerpanggil)
		print(" ------------------- ")
		'''
		#cek = node, self.wayOfOrder
		#print("from player to destination. " + str(cek))
		#print("daftar way is " + str(self.daftarWay))
		#pa = len(self.daftarWay)
		#print("panjang dari listOFWays ialah " + str(len(self.listOFWays)))
		jarak = None
		if self.chooePath == 'closer':
			for i in self.listOFWays:
				#print(i)
				if jarak == None:
					jarak = i
				else:
					if i < jarak:
						jarak = i
			if jarak == None:
				if self.firstNode == self.wayOfOrder:
					return [self.wayOfOrder]
				else:
					cek = self.listOFWays, self.firstNode, self.wayOfOrder
					print('error jarak = None. ref = {0}. Exiting now'.format(str(cek)))
					bge.logic.endGame()
			return self.listOFWays[jarak]
		elif self.chooePath == 'random':
			ways = []
			for i in self.listOFWays:
				ways.append(self.listOFWays[i])
			way = random.choice(ways)
			if var.ngecek == True:
				print(" --------------------------------- WayPoints ---------------------------------")
				cek = way, self.daftarWay
				print(cek)
				print(" --------------------------------- WayPoints ---------------------------------")
			return way
		
	def rebuildNodes(self):
		#print('------------------------------------------------------------------------------------------------')
		for node in self.nodes:
			for relate in self.nodes:
				if node != relate:
					vkonekCount = 0
					if relate not in node.relation:
						if node.v1 == relate.v1:
							vkonekCount += 1
						if node.v1 == relate.v2:
							vkonekCount += 1
						if node.v1 == relate.v3:
							vkonekCount += 1
						if node.v1 == relate.v4:
							vkonekCount += 1
						
						if node.v2 == relate.v1:
							vkonekCount += 1
						if node.v2 == relate.v2:
							vkonekCount += 1
						if node.v2 == relate.v3:
							vkonekCount += 1
						if node.v2 == relate.v4:
							vkonekCount += 1
						
						if node.v3 == relate.v1:
							vkonekCount += 1
						if node.v3 == relate.v2:
							vkonekCount += 1
						if node.v3 == relate.v3:
							vkonekCount += 1
						if node.v3 == relate.v4:
							vkonekCount += 1
						
						if node.v4 == relate.v1:
							vkonekCount += 1
						if node.v4 == relate.v2:
							vkonekCount += 1
						if node.v4 == relate.v3:
							vkonekCount += 1
						if node.v4 == relate.v4:
							vkonekCount += 1
						
						if vkonekCount > 1:
							#cek = node, relate, vkonekCount
							#print(cek)
							#print("ada " + str(vkonekCount))
							node.relation.append(relate)
						elif vkonekCount == 1:
							#node.debugGObject.visible = True
							#cek = node, relate, 1
							#print(cek)
							#print("ada yg cuma 1")
							pass
			#cek = node, node.relation
			#print('the node is ' + str(cek))
		#print('------------------------------------------------------------------------------------------------')
# ---------------------------------------------------------------------------------------------
	
# --------------------- Arm Section ---------------------
def bentrokan(projectile, target):
	if (target < 0 and projectile < 0) or (target > 0 and projectile > 0):
		hasil = projectile / target
		if hasil < 0:
			hasil *= -1
		return hasil
	else:
		hasil = projectile / target * 0.5
		if hasil < 0:
			hasil *= -1
		return hasil
class KX_Projectile(bge.types.KX_GameObject):
	shotBy = None
	shotWith = None
	destroyWhenImpact = False
	restoreDynamicWhenImpact = False
	useImpulseFactor = True
	hitOwner = False
	lastVelocity = Vector((0.0, 0.0, 0.0))
	ticks = 0
	damage = 1.0
	explosionEffect = None
	fungsiTambahan = []
	def __init__(self, old_owner):
		if "destroyWhenImpact" in self:
			self.destroyWhenImpact = self['destroyWhenImpact']
		if 'restoreDynamicWhenImpact' in self:
			self. restoreDynamicWhenImpact = self['restoreDynamicWhenImpact']
		if 'damage' in self:
			self.damage = self['damage']
		if 'useImpulseFactor' in self:
			self.useImpulseFactor = self['useImpulseFactor']
		if 'hitOwner' in self:
			self.hitOwner = self['hitOwner']
		self.collisionCallbacks.append(self.onImpact)
		
		if 'explosionEffect' in self:
			if type(self['explosionEffect']) == str:
				self.explosionEffect = self['explosionEffect']
		for i in self.fungsiTambahan:
			f = self.__getattribute__(i)
			f()
	def destroy(self):
		#play some effect before being delete
		#play some sound effect before being deleted
		self.localScale = [1,1,1]
		if self.explosionEffect != None:
			self.scene.addObject(self.explosionEffect, self)
		self.endObject()
	def onImpact(self, hitObject, point, normal):
		if hasattr(hitObject, 'hit'):
			if self.useImpulseFactor == True:
				a = self.mass * self.lastVelocity
				b = hitObject.mass * hitObject.getLinearVelocity()
				impulse = Vector((bentrokan(a.x, b.x), bentrokan(a.y, b.y), bentrokan(a.z, b.z)))
				impulseFactor = impulse.length * hitObject.initialHitPoints
				#cek = self.lastVelocity, normal
				#print(cek)
				hitObject.lastHitBy = self.shotBy.owner
				hitObject.lastHitWith = self.shotWith
				if self.hitOwner == True:
					hitObject.hit(impulseFactor + self.damage)
				else:
					if self.shotBy != hitObject:
						damageCause = impulseFactor * self.damage
						hitObject.hit(damageCause)
						if self.shotBy != None:
							self.shotBy.owner.score.damageCause += damageCause
						if hitObject.owner != None:
							hitObject.owner.score.damageRecieve += damageCause
			else:
				hitObject.hit(self.damage)
				if self.shotBy != None:
					self.shotBy.owner.score.damageCause += damageCause
				if hitObject.owner != None:
					hitObject.owner.score.damageRecieve += damageCause
			for i in triggerList.onPlayerHit:
				i(hitObject, self.shotBy.owner, self.shotWith, self)
		if self.shotBy == hitObject:
			#cek = id(self.shotBy), id(hitObject), self, (self.shotBy == hitObject), self.ticks
			#print("bla bla bla >>> " + str(cek))
			pass
		elif self.shotBy != hitObject:
			#cek = id(self.shotBy), id(hitObject), self, (self.shotBy == hitObject), self.ticks
			#print("second >> " + str(cek))
			#print(type(hitObject))
			if type(hitObject) != KX_SensSekitar:
				if self.ticks > 60:
					if self.destroyWhenImpact == True:
						self.destroy()
					if self.restoreDynamicWhenImpact == True:
						self.restoreDynamics()
		else:
			cek = id(self.shotBy), id(hitObject), self, (self.shotBy == hitObject), self.ticks
			print("third >> " + str(cek))
			pass
		self.ticks += 1
		#print("player {0} was hit by {1} with {2}".format(hitObject.name, str(self.shotBy.owner), str(self.shotWith)))
		
class KX_PointedMissile(KX_Projectile):
	target = simpleObject()
	timeToLive = 5 * bge.logic.getLogicTicRate()
	maxRotX = radians(50)
	maxRotZ = radians(50)
	def initTracker(self):
		self.timeToLive = 60
		if "timeToLive" in self:
			self.timeToLive = self['timeToLive'] * bge.logic.getLogicTicRate()
		if 'maxRotX' in self:
			self.maxRotX = radians(self['maxRotX'])
		if 'maxRotZ' in self:
			self.maxRotZ = radians(self['maxRotZ'])
	fungsiTambahan = ['initTracker']
	
	def trackTo(self, location, localPosition=False):
		#print(location)
		if location == var.player:
			var.PCO.gotLocked()
			pass
		v = self.getVectTo(location)
		if localPosition == False:
			mat = v[2]
		else:
			mat = v[1]
		#print(mat)
		#patch 24 01 2018 212351
		if mat.y < 0:
			mat = Vector((mat.x, mat.y, 0.0))
		#-----------------------
		try:
			sdt = acos(mat[1])
		except ZeroDivisionError:
			sdt = 0
		except ValueError:
			sdt = 0
		try:
			if mat[2] > 1:
				sdtX = asin(1.0)
				print("mat[2] has reach beyond 1.0 and it's currentValue is " + str(mat[2]))
			else:
				sdtX = asin(mat[2])
		except ZeroDivisionError:
			sdtX = 0
		except ValueError:
			sdtX = 0
			
		derajat = degrees(sdt)
		derajatX = degrees(sdtX)
		if var.ngecek == True:
			self['degreeXLeft'] = derajatX
			self['degreeZLeft'] = derajat
			self.addDebugProperty('degreeXLeft')
			self.addDebugProperty('degreeZLeft')
		
		rotZ = 0.0
		rotX = 0.0
		
		if mat[0] < 0:
			if derajat > self.maxRotZ:
				#self.applyRotation((0, 0, radians(self.speedZ)), True)
				rotZ = self.maxRotZ
			else:
				#self.applyRotation((0, 0, radians(derajat)), True)
				rotZ = radians(derajat)
		if mat[0] > 0:
			if derajat > self.maxRotZ:
				#self.applyRotation((0, 0, radians(-self.speedZ)), True)
				rotZ = -self.maxRotZ
			else:
				#self.applyRotation((0, 0, radians(-derajat)), True)
				rotZ = radians(-derajat)
				
		if mat[2] < 0.0:
			#print(sdtX)
			if sdtX < self.maxRotX:
				rotX = -self.maxRotX
			else:
				rotX = -sdtX
		if mat[2] > 0.0:
			if sdtX > self.maxRotX:
				rotX = self.maxRotX
			else:
				rotX = sdtX
				
		#print([pitchFactor, rollFactor, yawFactor])
		self.setAngularVelocity([rotX, 0.0, rotZ], True)
		
		return derajatX, derajat

class radarObject(bge.types.KX_GameObject):
	missileOf = simpleObject()
	def __init__(self, old_owner):
		pass
	def run(self, cont):
		if self.missileOf.invalid == False:
			self.missileOf.run(cont)

class KX_SeekingMissile(KX_PointedMissile):
	lockOnStatus = None
	radar = simpleObject()
	ra = None
	eks = None
	def initSeeker(self):
		#radarSection
		for i in self.children:
			if 'Radar' in i.sensors and 'expandable' in i.controllers:
				if type(i.sensors['Radar']) == bge.types.KX_RadarSensor and type(i.controllers['expandable']) == bge.types.SCA_PythonController:
					radar = radarObject(i)
					radar.missileOf = self
					self.ra = radar.sensors['Radar']
					self.eks = radar.controllers['expandable']
					self.eks.script = "weapons.runRadar"
					break
	fungsiTambahan = ['initTracker', 'initSeeker']
		
	def setTarget(self, target):
		self.target = target
		
	def run(self, cont):
		self.lastVelocity = self.getLinearVelocity()
		if self.lockOnStatus == "locked":
			if self.ticks > self.timeToLive:
				self.destroy()
			self.ticks += 1
			'''
			if self.target.invalid == False:
				self.trackTo(self.target)
			'''
			#print("projectile has tracking for " + str(self.target))
			if self.target in self.ra.hitObjectList:
				#if self.target != None:
				if self.target.invalid == False:
					self.trackTo(self.target)
				else:
					print("target is " + str(self.target))
				pass
			else:
				if self.ra.hitObject != None:
					self.trackTo(self.ra.hitObject)
				pass
projectileList = [KX_Projectile, KX_PointedMissile, KX_SeekingMissile]
# --------------------------------------------------------
class KX_RayObject(bge.types.KX_GameObject):
	rxp = None
	rxm = None
	ryp = None
	rym = None
	rzp = None
	rzm = None
	ray = {}
	#for i in range(6):
	#	ray.append(None)
	def __init__(self, old_owner):
		for i in self.sensors:
			if type(i) == bge.types.KX_RaySensor:
				self.ray[i.axis] = i
	def update(self):
		info = []
		for i in self.ray:
			if i.positive:
				info.append(i.axis)
		return info
		
	def getRay(self):
		return self.ray

class KX_SensSekitar(bge.types.KX_GameObject):
	triggerOnStartDelay = 60
	vec = None
	touched = False
	sen = None
	ho = None
	def __init__(self, old_one):
		if 'triggerOnStartDelay' in self:
			self.triggerOnStartDelay = self['triggerOnStartDelay']
		self.controllers['createObstacle'].script = "mainscript.touching"
		self.collisionCallbacks.append(self.onCollide)
		for i in self.sensors:
			if type(i) == bge.types.KX_TouchSensor:
				i.reset()
				self.sen = i
		
	def onCollide(self, ho, point, normal):
		if type(ho) not in terrainSensUnacceptedList:
			self.vec = point
			self.ho = ho
	def onTouched(self):
		if self.sen != None:
			if type(self.sen.hitObject) not in terrainSensUnacceptedList:
				self.touched = self.sen.positive
			else:
				if self.ho in self.sen.hitObjectList:
					self.touched = True
				else:
					self.touched = False
			#cek = self.touched, self.ho
			#print('status KX_SensSekitar ialah ' + str(cek))
			
class KX_JetEngine(bge.types.KX_GameObject):
	def __init__(self, old_owner, owner):
		self.maxHP = 1000
		self.currentHP = 1000
		self.owner = owner
		self.effect = None
		self.akselerasi = 9.8
		self.effectScaleBy = 'speed'
		self.effectScaleFactor = 1
		if 'addEffect' in self:
			added = self.scene.addObject(self['addEffect'], self)
			for child in added.children:
				if 'scaleBy' in child:
					self.effect = child
					if 'y_factor'  in child:
						self.effectScaleFactor = child['y_factor']
			#added.owner = owner
			if 'effectScale' in self:
				added.scaling = [self['effectScale'], self['effectScale'], self['effectScale']]
				added.setParent(self)
	def run(self):
		#ator dp scaling disini
		if self.effect != None:
			if self.owner.localLinearVelocity.y > 0:
				#sf = self.owner.localLinearVelocity.y + 1
				if self.owner.localLinearVelocity.y < self.akselerasi:
					if self.owner.maju > 1:
						self.effect.localScale.y = self.effectScaleFactor
					else:
						sf = (self.effectScaleFactor + self.owner.localLinearVelocity.y) / self.effectScaleFactor
						self.effect.localScale.y = sf
				else:
					sf = (self.effectScaleFactor + self.owner.localLinearVelocity.y) / self.effectScaleFactor
					self.effect.localScale.y = sf
			else:
				if event(self.owner.keymap, keyev, moev, 'maju') > 1:
					self.effect.localScale.y = self.effectScaleFactor
				else:
					self.effect.localScale.y = 1.0
				
		pass

class KX_VehicleObject(bge.types.KX_GameObject):
	initTambahan = []
	runTambahan = []
	#sense section
	senseOfAxis = simpleObject()
	unkilledabletime = 180
	def __init__(self, old_owner):
		self.useBy = None
		self.lastHitBy = None
		self.delayForUse = 30
		self.lastHitWith = None#dipisah supaya kalo misalnya player sdh mengganti kendaraan data kill kan dimasuk mengenai kendaraan yg sebelumnya yg melakukan kill tersebut
		self.initialHitPoints = 1000.0
		self.hitPoints = self.initialHitPoints
		self.sensorSekitar = None
		self.colliderSens = None
		self.tiks = 0
		self.fallingTimeImpactWarning = 5.0
		if 'fallingTimeImpactWarning' in self:
			self.fallingTimeImpactWarning = self['fallingTimeImpactWarning']
		self.minimumHeightToFly = 100.0
		if 'minimumHeightToFly' in self:
			self.minimumHeightToFly = self['minimumHeightToFly']
		
		self.childEffects = []
		
		self.faktorTanjakan = 1.0 - self.worldOrientation[2][1]
		
		if 'delayForUse' in self:
			self.delayForUse = self['delayForUse']
		if 'hitPoints' in self:
			self.initialHitPoints = self['hitPoints']
			self.hitPoints = self['hitPoints']
		self.delayForBailOut = 30
		if 'delayForBailOut' in self:
			self.delayForBailOut = self['delayForBailOut']
		self.playerSeatPos = self#warning this can cause some error
		self.playerExitPos = None
		#perencanaan untuk exit pos nantinya
		"""
		Akan ada beberapa exit pos in case kalo salah satu exit pos da ta halang deng objek laeng
		Sebelum player bisa exit, di perlukan sensor untuk mendeteksi jika ada objek laeng yg menghalangi dp posisi exit
		Untuk bisa mendeteksi maka pada exit pos akan di spawn objek khusu untuk mendeteksi (sebuah sensor physic) objek laeng dan me-remove-nya setelah ia melakukan pekerjaannya
		dengan hal tersebut maka diperlukan rentan 1 logic step untuk mengeceknya dan 1 logic step untuk me-remove-nya kemudian menaruh datanya ke dalam array available exit pos
		kemudian mengecek jika ada tempat yg frei untuk player bisa exit
		if ada maka:
			player exit di frei
		else:
			player tak bisa exit lagi
		"""
		self[var.penandaPlayer] = True#agar sebentar beberapa sensor bisa mendeteksi objek dari ini
		self.team = 1
		self.target = None
		self.currentWeapon = None
		self.primaryWeapon = None
		self.weapons = []
		self.guiIndex = None
		if 'guiIndex' in self:
			self.guiIndex = self['guiIndex']
		self.tipe = "mobil"
		if 'type' in self:
			self.tipe = self['type']
		self.wIndex = 0
		self.owner = None
		self.dummyDict = {}
		self.keymap = var.globalDict['control']['control_kendaraan_umum']
		if 'keymap' in self:
			#self.keymap = self['keymap']
			self.keymap = var.globalDict['control'][self['keymap']]
			
		#print("keymap of this vehicle {0} is {1}".format(self.name, str(self.keymap)))
		
		self.GUIID = 'default'
		if 'GUIID' in self:
			self.GUIID = self['GUIID']
			
		# --------------- Camera Set ---------------
		#rencana untuk camera dibagi menjadi 2 yaitu Third Person dengan menggunakan camPoros atau hanya First Person tanpa menggunakan camPoros
		self.camPos = None
		self.camPoros = [None, None]
		# ------------------------------------------
		
		# --------------- Warning Section ---------------
		self.impactTimeWarning = 5
		if 'impactTimeWarning' in self:
			self.impactTimeWarning = self['impactTimeWarning']
		# -----------------------------------------------
		
		#a player that drive this vehicle
		self.driveBy = None
		
		self.gearRight = []
		self.gearLeft = []
		
		self.track_right = None
		self.track_left = None
		
		# ------------ Jet Section ------------ #
		#engine section
		self.jet_engines = []
		self.jet_engine_is_exist = False
		self.forwardVelocity = 0.0
		self.lastFaktorTanjakan = 1.0 - self.worldOrientation[2][1]
		self.forwardForce = 1.0
		if 'forwardForce' in self:
			self.forwardForce = self['forwardForce']
		
		#other section
		self.enableMouseControl = False
		if self.tipe == "airplane":
			self.enableMouseControl = True
		'''
		'''
		self.dimensi = get_dimensions(self)
		self.plane_size_x = hypot(self.dimensi[1], self.dimensi[2])
		self.plane_size_y = hypot(self.dimensi[0], self.dimensi[2])
		if 'plane_size_y' in self:
			self.plane_size_y = self['plane_size_y']
		self.plane_size_z = hypot(self.dimensi[0], self.dimensi[1])
		#total_rotation gonna use in counting rotation speed as factor untuk mengurangi kecepatan pada axisnya
		self.total_rotation_x = 0.0
		self.total_rotation_y = 0.0
		self.total_rotation_z = 0.0
		self.lastAngularVelocity = self.getAngularVelocity(True)
		self.akselerasi = 9.8
		if 'akselerasi' in self:
			self.akselerasi = self['akselerasi']
		self.liftForce = 0.0
		self.speedToLift = 350
		if 'speedToLift' in self:
			self.speedToLift = self['speedToLift']
		self.damping = 0.04
		if "damping" in self:
			self.damping = self['damping']
		
		#untuk sementara kase disable dulu
		#self.maxSpeed = getMaxSpeed(self.akselerasi, self.damping)
		#kong ganti deng
		self.drag = 0.02
		if 'drag' in self:
			self.drag = self['drag']
		self.maxSpeed = oscmath.getMaxSpeed(self.akselerasi*self.mass*1000, var.mapKonfigurasi['masaUdara'], self.drag, self.plane_size_y)
		
		self.speedToPitch = 350 / 3.6#350km/s diubah ke meter/detik
		self.speedToRoll = 350 / 3.6
		self.speedToYaw = 350 / 3.6
		
		if 'speedToPitch' in self:
			self.speedToPitch = self['speedToPitch'] / 3.6
		if 'speedToRoll' in self:
			self.speedToRoll = self['speedToRoll'] / 3.6
		if 'speedToYaw' in self:
			self.speedToYaw = self['speedToYaw'] / 3.6
		self.maxRotX = radians(40)
		self.maxRotY = radians(40)
		self.maxRotZ = radians(15)
		if 'maxRotX' in self:
			self.maxRotX = radians(self['maxRotX'])
		if 'maxRotY' in self:
			self.maxRotY = radians(self['maxRotY'])
		if 'maxRotZ' in self:
			self.maxRotZ = radians(self['maxRotZ'])
		# ------------ For jet AI -------------
		tikRate = bge.logic.getLogicTicRate()
		self.botMaxRotX = self.maxRotX / tikRate
		self.botMaxRotY = self.maxRotY / tikRate
		self.botMaxRotZ = self.maxRotZ / tikRate
		self.botTimeToFlight = 20*tikRate
		if 'botTimeToFlight' in self:
			self.botTimeToFlight = self['botTimeToFlight'] * bge.logic.getLogicTicRate()
		# ------------------------------------- #
		
		self.changeWeapon1 = 0
		self.changeWeapon2 = 0
		self.tembak = 0
		self.tembak2 = 0
		self.zoomIn = 0
		self.zoomOut = 0
		self.changetarget = 0

		self.maju = nope
		self.mundur = nope
		self.turnL = nope
		self.turnR = nope
		
		self.keluar = nope
		
		#self.forwardSpeed = 0.2
		self.forwardSpeed = 5.2
		if 'forwardSpeed' in self:
			#self.forwardSpeed = self['forwardSpeed'] / bge.logic.getLogicTicRate()
			self.forwardSpeed = self['forwardSpeed']
		self.backwardSpeed = 0.05
		if 'backwardSpeed' in self:
			self.backwardSpeed = self['backwardSpeed']
		self.turnSpeed = 0.7
		if 'turnSpeed' in self:
			self.turnSpeed = self['turnSpeed']
			
		
		#self.scene = bge.logic.getCurrentScene()
		self.interceptPoint = None
		if interceptPoint not in self.childrenRecursive:
			self.interceptPoint = self.scene.addObject(interceptPoint, self)#perlu mo hapus kalo main objeknya udah mokat
			#self.interceptPoint.groupObject(self)
			#self.interceptPoint.setParent(self)
			
		
		self.forwardRay = None
		self.topRay = None
		self.bottomRay = None
		for i in self.sensors:
			if type(i) == bge.types.KX_RaySensor:
				#self.ray[i.axis] = i
				if i.axis == 1:
					self.forwardRay = i
				if i.axis == 2:
					self.topRay = i
				if i.axis == 5:
					self.bottomRay = i
			
			
		''' ---------------------------- Checking up the other bundle ---------------------------- '''
		hitung = 0
		passed = 0
		for obj in self.childrenRecursive:
			hitung += 1
			try:
				if var.ngecek == True:
					print("{0} is ok".format(obj.name))
				if 'gear_right' in obj:
					self.gearRight.append(obj)
				if 'gear_left' in obj:
					self.gearLeft.append(obj)
				if 'track_right' in obj:
					self.track_right = obj
				if 'track_left' in obj:
					self.track_left = obj
				if 'setAsPrimaryCam' in obj:
					self.camPos = obj
				if 'setAsPlayerSeat' in obj:
					self.playerSeatPos = obj
				if 'playerExitPos' in obj:
					self.playerExitPos = obj
				#semua object yg di mutate harus kasih di akhir sectionnya untuk mencegah error
				if 'setAsCamPoros' in obj:
					xAda = False
					yAda = False
					if 'enableAxisX' in obj:
						if obj['enableAxisX'] == False:
							self.camPoros[1] = mouseLook(obj)
							self.camPoros[1].isEnable = True
							yAda = True
					if 'enableAxisY' in obj:
						if obj['enableAxisY'] == False:
							self.camPoros[0] = mouseLook(obj)
							self.camPoros[0].isEnable = True
							xAda = True
					if xAda == False and yAda == False:
						self.camPoros[0] = mouseLook(obj)
					
				#weaponSection
				if 'createPrimaryWeapon' in obj:
					self.primaryWeapon = weapons(obj, self)
				
				#sense section
				if 'createRay' in obj.controllers:
					if type(obj.controllers['createRay']) == bge.types.SCA_PythonController:
						if obj.controllers['createRay'].mode == 1:
							self.senseOfAxis = KX_RayObject(obj)
							#this version might be remove in the next update
				if 'createObstacle' in obj.controllers:
					if type(obj.controllers['createObstacle']) == bge.types.SCA_PythonController:
						if obj.controllers['createObstacle'].mode == 1:
							self.sensorSekitar = KX_SensSekitar(obj)
							pass
						else:
							print('to make sense object the createObstacle controllers should be a module one')
				if 'jet_engine' in obj:
					self.jet_engine_is_exist = True
					jEngine = KX_JetEngine(obj, self)
					if 'akselerasi' in jEngine:
						self.akselerasi = jEngine['akselerasi']
					jEngine.akselerasi = self.akselerasi
					self.jet_engines.append(jEngine)
					jEngine.owner = self
				#if 'createObstacle' in obj:
				#	this.sensorSekitar = KX_SensSekitar(obj)
				#	this.sensorSekitar.owner = self
			except SystemError:
				if var.ngecek == True:
					print("passing some object")
				passed += 1
				#print(obj)
		print("total object dalam vehicle {0} ialah {1} dan yg terlewati ialah {2}".format(self.name, str(hitung), str(passed)))
		''' --------------------------------------------------------------------------------------- '''
		try:
			self.rebuildChildEffects()
			if 'collider' in self.controllers and 'Collision' in self.sensors:
				if type(self.controllers['collider']) == bge.types.SCA_PythonController and type(self.sensors['Collision']) == bge.types.KX_TouchSensor:
					if self.controllers['collider'].mode == 1:
						self.controllers['collider'].script = 'mainscript.collide'
						self.colliderSens = self.sensors['Collision']
			for i in self.initTambahan:
				f = self.__getattribute__(i)
				f()
		except:
			checker.getInfo()
			bge.logic.endGame()
		
	def setCamPos(self):
		''' ------------------------------ Settingup Camera Position ------------------------------ '''
		if self.owner == var.PCO:
			if self.camPos != None:
				camPos = self.camPos
				try:
					if camPos != self.scene.active_camera:
						self.scene.active_camera = camPos
				except TypeError:
					print("error on gameobjects setCamPos function; you you're trying to add object that does not a cam object")
		else:
			print('self.name' + " camPos is None")
		''' --------------------------------------------------------------------------------------- '''
		
	def addLookAt(self):
		if var.lastAddedGameObjectId == id(self):
			print(' --------- Adding lookAt object --------- ')
			#self.scene.addObject('lookAt')
			print(' ---------------------------------------- ')
		else:
			print("objek {0} is not the lastAddedGameObject".format(self.name))
			print('referensi {0} missmatch {1}'.format(str(id(self)), str(var.lastAddedGameObjectId)))
			
	def setCont(self, cont):
		self.cont = cont
		#fungsi setCont mungkin akan dihapus di kemudian harinya
		
	def rebuildChildEffects(self):
		self.childEffects = []
		for i in self.childrenRecursive:
			if 'createEffect' in i:
				ef = KX_SimpleEffect(i)
				ef.owner = self
				self.childEffects.append(ef)
		#print(' ---------------------- the effect---------------------- ')
		#print(self.childEffects)
		#print(' ---------------------- the effect---------------------- ')
		
	def cek(self):
		print("test neh")
	
	def hit(self, hitpoints):
		self.hitPoints -= hitpoints
		if self.hitPoints < 0:
			print('destroying object because that object HP is below zero')
			self.destroy()
	def destroy(self):
		#algoritma lainnya sperti
		#play effect
		if 'onDestroyedEffect' in self:
			self.scene.addObject(self['onDestroyedEffect'], self)
		#play destroying sound
		#change camera
		if self.lastHitBy != None:
			if self.invalid == False and self.lastHitBy.invalid == False:
				if self.lastHitWith == None:
					print('object {0} has been destroy by {1} with {2}'.format(id(self), str(self.lastHitBy), str(self.lastHitWith)))
		else:
			self.lastHitWith == None
		if self == var.player:
			#HUD.removePGUI(None)
			#HUD.removeWGUI(None)
			self.scene.active_camera = self.scene.cameras['inGameMainCam']
			pa = self.scene.cameras['inGameMainCam'].parent
			if self.camPos != None:
				if self.camPos.invalid == False:
					pa.position = self.camPos.position
					pa.worldOrientation = self.worldOrientation
			var.player = None
		if self.owner != None:
			self.owner.score.death += 1
			if hasattr(self.lastHitBy, "team") == False:
				self.owner.score.suicide += 1
			if var.tikets[self.owner.team] != 'inf':
				var.tikets[self.owner.team] -= 1
				if var.tikets[self.owner.team] <= 0:
					for t in triggerList.onTicketReachZero:
						t(self.owner.team)
		for i in triggerList.onPlayerKilled:
			i(self.owner, self.lastHitBy, self.lastHitWith)
		mainscript.addKill(self.lastHitBy, self.owner)
		self.endObject()
		
	def setTarget(self, target, sens):
		self.target = target
		if hasattr(self.owner, "setTargetBySensing"):
			self.owner.setTargetBySensing(target, sens)
			#print(target)
		
	keyev = keyboard.events
	moev = mouse.events
	def proseskan(self):
		try:
			''' -------------------------------- Camera Section -------------------------------- '''
			#if hasattr(self.camPoros[0], 'run') == True:
			#	self.camPoros[0].run()
			''' -------------------------------------------------------------------------------- '''
			
			''' -------------------------------- Weapon Section -------------------------------- '''
			wp = len(self.weapons)
			if wp > 0:
				if self.currentWeapon == None:
					self.currentWeapon = self.weapons[0]
					self.wIndex = 0
				else:
					if wp > 1:
						#print(self.changeWeapon1)
						if self.changeWeapon1 == jaktif:
							if self.wIndex < wp - 1:
								selanjutnya = self.wIndex+1
								self.currentWeapon = self.weapons[selanjutnya]
								#HUD.weapon_name.text = self.currentWeapon.name
								self.wIndex += 1
							else:
								self.currentWeapon = self.weapons[0]
								#HUD.weapon_name.text = self.currentWeapon.name
								self.wIndex = 0
							print('object {0} is changing weapon to {1}'.format(self.name, self.currentWeapon.name))
						if self.changeWeapon2 == jaktif:
							if self.wIndex > 0:
								selanjutnya = self.wIndex-1
								self.currentWeapon = self.weapons[selanjutnya]
								#HUD.weapon_name.text = self.currentWeapon.name
								self.wIndex = selanjutnya
							else:
								reset = wp - 1
								self.currentWeapon = self.weapons[reset]
								#HUD.weapon_name.text = self.currentWeapon.name
								self.wIndex = reset
							print('object {0} is changing weapon to {1}'.format(self.name, self.currentWeapon.name))
						
					
					if self.currentWeapon.lockedTo == None:
						lookAt = mainscript.lookAt
						if lookAt != None:
							self.interceptPoint.position = lookAt
						else:
							self.interceptPoint.position = self.scene.objects['lookAtDummy'].position
					#if self.tembak == aktif:
					#	self.currentWeapon.fire()
					self.currentWeapon.checkFire(self.tembak2)
					self.primaryWeapon.checkFire(self.tembak)
					if self.tipe != "airplane":
						self.currentWeapon.run(self.interceptPoint, self.owner)
			''' -------------------------------------------------------------------------------- '''
			
			''' ------------------------------- Movement Section ------------------------------- '''
			if self.tipe == 'ground_tank':
				if type(self.track_left) == bge.types.KX_GameObject and type(self.track_right) == bge.types.KX_GameObject:
					maju = 0.0
					if self.maju == 2:
						for i in self.gearLeft:
							#rotateL(i)
							rotateR(i)
						for i in self.gearRight:
							rotateR(i)
						maju = self.forwardSpeed
					if self.mundur == 2:
						for i in self.gearLeft:
							#rotateL(i)
							rotateL(i)
						for i in self.gearRight:
							rotateL(i)
						maju = -self.backwardSpeed
					self.applyMovement([0, maju, 0], True)
					belok = 0.0
					if self.turnL == 2:
						belok = self.turnSpeed
					if self.turnR == 2:
						belok = -self.turnSpeed
					self.applyRotation([0,0,belok], True)
			#elif self.tipe == 'airplane':
			#	if self.jet_engine_is_exist == True:
			#		jetEngine(self)
			#		jetControl(self)
			if self.jet_engine_is_exist == True:
				jetEngine(self)
			''' -------------------------------------------------------------------------------- '''
			
			''' ------------------------------- Exiting Section -------------------------------- '''
			'''
			if self.keluar == jaktif and self.tiks > self.delayForBailOut:
				var.player = self.driveBy
				self.driveBy.camPosHere()
				eul = self.playerExitPos.worldOrientation.to_euler()
				eul = Euler((0.0, 0.0, eul.z), 'XYZ')
				self.driveBy.worldOrientation = eul.to_matrix()
				self.driveBy.removeParent()
				self.driveBy.disableRigidBody()
				self.driveBy.position = self.playerExitPos.position
				z = eul.z
				self.driveBy = None
				self.useBy = None
				#nanti kalo somo pake penumpang kong tu penumpang mo pindah tampa nanti pake switch rupa temp = self.driveBy self.driveBy = self.penumpang1 lalu self.penumpang1 = temp. Yah rupa itulah
			'''
			''' -------------------------------------------------------------------------------- '''
			
			#tikking section
			self.tiks += 1
			for i in self.runTambahan:
				f = self.__getattribute__(i)
				f()
		except:
			checker.getInfo()
			bge.logic.endGame()
	def runPlayer(self):
		try:
			self.keyev = keyboard.events
			moev = mouse.events
			'''
			if keyev[bge.events.FKEY] > 0:
				self.changeWeapon1 = cek(keymap, 'changeWeapon1')
				print(self.changeWeapon1)
			
			'''
			self.changeWeapon1 = event(self.keymap, self.keyev, moev, 'changeWeapon1')
			self.changeWeapon2 = event(self.keymap, self.keyev, moev, 'changeWeapon2')
			self.tembak = event(self.keymap, self.keyev, moev, 'tembak')
			self.tembak2 = event(self.keymap, self.keyev, moev, 'tembak2')
			#self.zoomIn = event(self.keymap, self.keyev, moev, 'zoomIn')
			#self.zoomOut = event(self.keymap, self.keyev, moev, 'zoomOut')
			self.changetarget = event(self.keymap, self.keyev, moev, 'changetarget')
			
			self.maju = event(self.keymap, self.keyev, moev, 'maju')
			self.mundur = event(self.keymap, self.keyev, moev, 'mundur')
			self.turnL = event(self.keymap, self.keyev, moev, 'turnL')
			self.turnR = event(self.keymap, self.keyev, moev, 'turnR')
			
			#self.keluar = event(self.keymap, self.keyev, moev, 'keluar')
			
		except:
			checker.getInfo(self.keyev)
			bge.logic.endGame()
		self.proseskan()
		
	def run(self):
		self.tiks += 1
		for i in self.childEffects:
			i.run()
			
	def runRays(self):
		if self.forwardRay != None:
			pass
			
	def getImpactWarning(self):
		v = self.localLinearVelocity
		ada = False
		
		front = False
		nFront = Vector((0,0,0))
		tFront = self.impactTimeWarning
		if self.forwardRay != None:
			self.forwardRay.range = self.impactTimeWarning * v.y
			if self.forwardRay.positive == True:
				nFront = 10 * Vector(self.forwardRay.hitNormal)
				front = True
				ada = True
				impactRange = (self.worldPosition - Vector(self.forwardRay.hitPosition)).length
				try:
					tFront = impactRange / v.y
				except ZeroDivisionError:
					tFront = self.impactTimeWarning
				
		top = False
		nTop = Vector((0,0,0))
		tTop = self.impactTimeWarning
		if self.topRay != None:
			self.topRay.range = self.impactTimeWarning * v.y
			if self.topRay.positive == True:
				nTop = 10 * Vector(self.topRay.hitNormal)
				top = True
				ada = True
				impactRange = (self.worldPosition - Vector(self.topRay.hitPosition)).length
				try:
					tTop = impactRange / v.y
				except ZeroDivisionError:
					tTop = self.impactTimeWarning
				
		bottom = False
		nBottom = Vector((0,0,0))
		tBottom = self.impactTimeWarning
		if self.bottomRay != None:
			self.bottomRay.range = self.impactTimeWarning * v.y
			if self.bottomRay.positive == True:
				nBottom = 10 * Vector(self.bottomRay.hitNormal)
				bottom = True
				ada = True
				impactRange = (self.worldPosition - Vector(self.bottomRay.hitPosition)).length
				try:
					tBottom = impactRange / v.y
				except ZeroDivisionError:
					tBottom = self.impactTimeWarning
				
		#return [front, top, bottom], {"front":nFront, "top":nTop, "bottom":nBottom}
		#return ada, {"front":nFront, "top":nTop, "bottom":nBottom}
		
		terdekat = nFront
		w = self.impactTimeWarning
		asal = 'depan'
		
		if tFront < w:
			terdekat = nFront
			w = tFront
			asal = 'depan'
		if tTop < w:
			terdekat = nTop
			w = tTop
			asal = 'atas'
		if tBottom < w:
			terdekat = nBottom
			w = tBottom
			asal = 'bawah'
		return ada, terdekat, asal, {"front":nFront, "top":nTop, "bottom":nBottom}, {"depan":tFront, "atas":tTop, "bawah":tBottom}#have toevade, axis to evade, impact_origin, evade list, impactTime
		
	def runJetEngine(self):
		jetEngine(self)
	def onCollide(self):
		o = self.colliderSens.hitObject
		if o!= None:
			if type(o) not in projectileList:
				self.lastHitBy = o
			if self.tiks > self.unkilledabletime:
				if type(o) not in terrainSensUnacceptedList:
					if 'landingPad' not in o:
						self.owner.score.damageRecieve += self.hitPoints
						self.destroy()
		
class KX_AirPlaneObject(KX_VehicleObject):
	isView360 = False
	cam = bge.logic.getCurrentScene().active_camera
	def initAirplane(self):
		#importing modul yg diperlukan untuk kontrol
		keyev = keyboard.events
		moev = mouse.events
		
		#control sectiom
		self.turnL = event(self.keymap, keyev, moev, 'turnL')
		self.turnR = event(self.keymap, keyev, moev, 'turnR')
		self.rollRight = event(self.keymap, keyev, moev, 'rollRight')
		self.rollLeft = event(self.keymap, keyev, moev, 'rollLeft')
		self.pitchUp = event(self.keymap, keyev, moev, 'pitchUp')
		self.pitchDown = event(self.keymap, keyev, moev, 'pitchDown')
		
	initTambahan = ['initAirplane']
	def jetControlTurning(self):
		rx = 0.0
		ry = 0.0
		rz = 0.0
		
		(rvx, rvy, rvz) = self.getAngularVelocity(True)
		
		if self.turnL:
			if type(self.turnL) == int:
				rz = self.maxRotZ
			else:
				rz = self.turnL * var.airPlaneMouseSensitivity
		if self.turnR:
			if type(self.turnR) == int:
				rz = -self.maxRotZ
			else:
				rz = self.turnR * var.airPlaneMouseSensitivity
		if self.rollRight:
			if type(self.rollRight) == int:
				ry =  -1 * var.airPlaneMouseSensitivity
			else:
				ry = self.rollRight * var.airPlaneMouseSensitivity
		if self.rollLeft:
			if type(self.rollLeft) == int:
				ry = 1 * var.airPlaneMouseSensitivity
			else:
				ry = self.rollLeft * var.airPlaneMouseSensitivity
		#if pitchUp or pitchDown:
		if self.pitchUp:
			if type(self.pitchUp) == int:
				rx = self.maxRotX
			else:
				rx = -self.pitchUp * var.airPlaneMouseSensitivity
		if self.pitchDown:
			if type(self.pitchDown) == int:
				rx = -self.maxRotX
			else:
				rx = -self.pitchDown * var.airPlaneMouseSensitivity
		
		rvx += rx * self.localLinearVelocity.y / self.speedToPitch
		rvy += ry * self.localLinearVelocity.y / self.speedToRoll
		rvz += rz * self.localLinearVelocity.y / self.speedToYaw
		
		#print([rx,rx,rz])
		if rvz > self.maxRotZ:
			rvz = self.maxRotZ
		if rvz < -self.maxRotZ:
			rvz = -self.maxRotZ
		if rvy < -self.maxRotY:
			rvy = -self.maxRotY
		if rvy > self.maxRotY:
			rvy = self.maxRotY
		if rvx < -self.maxRotX:
			rvx = -self.maxRotX
		if rvx > self.maxRotX:
			rvx = self.maxRotX
		self.setAngularVelocity([rvx, rvy, rvz], True)
		
		if var.ngecek == True:
			self['putaran'] = str([rvx, rvy, rvz])
			self.addDebugProperty("putaran")
	def rumAirPlane(self):
		self.swith360view = event(self.keymap, self.keyev, moev, 'swith360view')
		if self.swith360view > 0:
			self.cam = self.scene.active_camera
			if self.camPoros[1] != self.cam.parent and self.cam.parent != self.camPoros[0]:
				if self.cam.parent != None:
					if type(self.cam.parent) == mouseLook:
						self.camPoros[1] = self.cam.parent
						#self.camPoros[1].isEnable = True
						if self.camPoros[0] != self.camPoros.parent:
							if self.camPoros[1].parent != None:
								if type(self.camPoros[1].parent) == mouseLook:
									self.camPoros[0] = self.camPoros[1].parent
									#self.camPoros[0].isEnable = True
			if self.camPoros[0] != None and self.camPoros[1] != None:
				self.camPoros[0].isEnable = True
				self.camPoros[1].isEnable = True
				self.camPoros[0].run()
				self.camPoros[1].run()
				if self.swith360view > 1:
					self.isView360 = True
		else:
			jetControl(self)
			if self.camPoros[0] == None and self.camPoros[1] == None:
				#jetControl(self)
				pass
			else:
				'''
				'''
				if self.isView360 == True:
					xDone = False
					zDone = False
					if self.camPoros[0] != None:
						if self.camPoros[0].isResetCam == True:
							if self.camPoros[0].isEnable == True:
								self.camPoros[0].isEnable = False
							self.camPoros[0].run()
							if self.camPoros[0].resetStats == 'selesai':
								xDone = True
								self.camPoros[0].resetStats = 'waiting'
						else:
							xDone = True
					else:
						xDone = True
					if self.camPoros[1] != None:
						if self.camPoros[1].isResetCam == True:
							if self.camPoros[1].isEnable == True:
								self.camPoros[1].isEnable = False
							self.camPoros[1].run()
							if self.camPoros[1].resetStats == 'selesai':
								zDone = True
								self.camPoros[1].resetStats = 'waiting'
						else:
							zDone = True
					else:
						zDone = True
					#cek = self.camPoros, xDone, zDone
					#print(cek)
					if xDone == True and zDone == True:
						self.isView360 = False
						pass
				else:
					#jetControl(self)
					pass
	runTambahan = ['rumAirPlane']
class KX_TankObject(KX_VehicleObject):
	def __init__(self, old_owner):
		pass
	
	def runPlayer(self):
		try:
			
			''' ------------------------------- Movement Section ------------------------------- '''
			pass
		except:
			checker.getInfo()
			bge.logic.endGame()
	
class KX_SoldierObject(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		self[var.penandaPlayer] = True#agar bisa dideteksi oleb spesifik sensor
		self.team = 1
		self.target = None
		self.lookIsEnable = True
		self.currentWeapon = 1
		self.arms = []
		for i in range(0, 10):
			self.arms.append(None)
		self.hadWeapon = False
		self.wIndex = 0
		self.guiIndex = None
		if 'guiIndex' in self:
			self.guiIndex = self['guiIndex']
		self.useBy = None
		self.dummyDict = {}
		self.keymap = var.globalDict['control']['control_player']
		self.raySensor = None
		#self.lookAtObject = None
		'''
		self.lookAtSensor = None
		if 'lookAt' in self.scene.objects:
			temp = self.scene.objects['lookAt']
			if 'mOver' in temp.sensors:
				if type(temp.sensors['mOver']) == bge.types.KX_RaySensor:
					self.lookAtSensor = temp.sensors['mOver']
					print("apllying lookAtSensors")
		'''
		
		self.changeWeapon1 = 0
		self.changeWeapon2 = 0
		self.tembak = 0
		self.tembak2 = 0
		self.zoomIn = 0
		self.zoomOut = 0
		self.changetarget = 0
		
		self.normalSpeed = 0.08
		self.sprintSpeed = 0.2
		if 'normalSpeed' in self:
			self.normalSpeed = self['normalSpeed']
		if 'sprintSpeed' in self:
			self.sprintSpeed = self['sprintSpeed']
		self.jumpVelocity = 0.7
		if 'jumpVelocity' in self:
			self.jumpVelocity = self['jumpVelocity']
			
		self.GUIID = 'default'
		if 'GUIID' in self:
			self.GUIID = self['GUIID']
			
		self.bundleX = None
		self.camParent = None
		passed = 0
		for i in self.childrenRecursive:
			try:
				if 'cam_parent_here' in i:
					self.camParent = i
				if "mouseX here" in i:
					self.bundleX = mouseLook(i)
					print("binding mouseLook script to object {0} is success".format(self.bundleX.name))
					#self.bundleX = i
					#self.bundleX.enableAxisY = False
					self.bundleX.enableAxisX = False
				if 'setAsPrimaryCam' in i:
					self.camPos = i
			except SystemError:
				if var.ngecek == True:
					print("passing some object")
				passed += 1
				
		'''
		if type(self.bundleX) == bge.types.KX_GameObject or type(self.bundleX) == mouseLook:
			self.camPosHere()
		'''
			
		self.enableMouseControl()
		
	def setCamPos(self):
		''' ------------------------------ Settingup Camera Position ------------------------------ '''
		if self.owner == var.PCO:
			if self.camPos != None:
				camPos = self.camPos
				try:
					if camPos != self.scene.active_camera:
						self.scene.active_camera = camPos
				except TypeError:
					print("error on gameobjects setCamPos function; you you're trying to add object that does not a cam object")
		else:
			print('self.name' + " camPos is None")
		''' --------------------------------------------------------------------------------------- '''
		
	def camPosHere(self):
		"""This function might going to be remove on later"""
		camera = self.scene.active_camera.parent
		camPos = self.camParent
		#print(" ------------- Setting up player CamPos --------------- ")
		#print(self.scene)
		#print(self.scene.active_camera)
		#print(camera)
		#print(" ------------------------------------------------------ ")
		
		#print(" ------------------------ AAAAAAAAAAAAAAAAAAAA {0} --------------------------- ".format(str(porosKamera)))
		
		if var.scene['camPosIsOn'] != self:
			var.scene['camPosIsOn'] = self
			if camera.parent != None:
				camera.removeParent()
			camera.position = camPos.position
			camera.worldOrientation = camPos.worldOrientation
			camera.setParent(camPos)
			self.enableMouseControl()
			#camPos['terParent'] = True
	
	def enableMouseControl(self):
		self.lookIsEnable = True
		if type(self.bundleX) == bge.types.KX_GameObject or type(self.bundleX) == mouseLook:
			self.bundleX.isEnable = True
		
	def disableMouseControl(self):
		self.lookIsEnable = False
		if type(self.bundleX) == bge.types.KX_GameObject or type(self.bundleX) == mouseLook:
			self.bundleX.isEnable = False
				
	def rotZ(self):
		mo = bge.logic.mouse
		rm = mo.position[0] - 0.5
		if self.lookIsEnable == True:
			self.applyRotation([0.0, 0.0, -rm*var.soldierLookSensitivity], False)
			
	def run(self):
		pass
		
	def runPlayer(self):
		try:
			inVehicle = False#qt baru inga kote karna qt malas mo unindent samua maka qt cuma pake logic if tare :3
			if inVehicle == False:
				if type(self.bundleX) == mouseLook:
					self.bundleX.run()
				self.rotZ()
				keyev = keyboard.events
				moev = mouse.events
				'''
				if keyev[bge.events.FKEY] > 0:
					self.changeWeapon1 = cek(keymap, 'changeWeapon1')
					print(self.changeWeapon1)
				
				'''
				self.changeWeapon1 = event(self.keymap, keyev, moev, 'changeWeapon1')
				self.changeWeapon2 = event(self.keymap, keyev, moev, 'changeWeapon2')
				self.tembak = event(self.keymap, keyev, moev, 'tembak')
				self.quickZoom = event(self.keymap, keyev, moev, 'quickZoom')
				#self.tembak2 = event(self.keymap, keyev, moev, 'tembak2')
				self.use = event(self.keymap, keyev, moev, 'use')
				self.zoomIn = event(self.keymap, keyev, moev, 'zoomIn')
				self.zoomOut = event(self.keymap, keyev, moev, 'zoomOut')
				
				self.maju = event(self.keymap, keyev, moev, 'maju')
				self.mundur = event(self.keymap, keyev, moev, 'mundur')
				self.kiri = event(self.keymap, keyev, moev, 'kiri')
				self.kanan = event(self.keymap, keyev, moev, 'kanan')
				
				self.sprint = event(self.keymap, keyev, moev, 'sprint')
				self.lompat = event(self.keymap, keyev, moev, 'lompat')
				
				maju = 0.0
				samping = 0.0
				if self.maju == aktif:
					if self.sprint == aktif:
						maju = self.sprintSpeed
					else:
						maju = self.normalSpeed
				if self.mundur == aktif and self.maju == nope:
					maju = -self.normalSpeed
					
				if self.sprint == nope:
					if self.kiri == aktif and self.kanan == nope:
						samping = -self.normalSpeed
					if self.kiri == nope and self.kanan == aktif:
						samping = self.normalSpeed
				else:
					if self.kiri == aktif and self.kanan == nope:
						samping = -self.sprintSpeed
					if self.kiri == nope and self.kanan == aktif:
						samping = self.sprintSpeed
						
				self.applyMovement([samping, maju, 0.0], True)
				#self.applyMovement([0, 0.01, 0])
				#self.position.y += 0.01
				#print([self.maju, maju, self.position])
				
				if self.lompat == jaktif:
					#print("player melompat")
					#print("status variable ray sensor ialah : " + str(self.raySensor))
					if self.raySensor != None:
						#print("sensor raynya ialah " + str(self.raySensor.positive))
						if self.raySensor.positive == 1:
							#self.applyForce([0.0, 0.0, self.jumpVelocity], True)
							self.localLinearVelocity.z = self.jumpVelocity
					
				if 'playerLookAtObject' in var.scene:
					if var.scene['playerLookAtObject'] != None:
						lookAtObject = var.scene['playerLookAtObject']
						if lookAtObject in self.scene.objects and var.scene['playerLookAtRange'] != None:
							#HUD.willUseStatusText = lookAtObject.name
							if var.scene['playerLookAtRange'] <= var.globalDict['rangeOfUse']:
								if 'thisIsWeapon' in lookAtObject:
									senjata = lookAtObject
									#print("printing the text over the HUD")
									if 'itemIndex' in senjata:
										if self.arms[senjata['itemIndex']] == None:
											HUD.willUseStatusText = "take_item " + senjata.name
											if self.use == lepas and self.bundleX != None:
												self.arms[senjata['itemIndex']] = senjata
												senjata.setParent(self.bundleX, False, True)
												if self.hadWeapon == False:
													self.currentWeapon = senjata['itemIndex']
													senjata.setOnUse(self.bundleX)
													self.hadWeapon = True
												else:
													if var.alwaysUseNewlyTakenItem == True:
														self.arms[self.currentWeapon].setAsBackUp()
														self.currentWeapon = senjata['itemIndex']
														senjata.setOnUse(self.bundleX)
													else:
														if self.currentWeapon == senjata['itemIndex']:
															senjata.setOnUse(self.bundleX)
														else:
															senjata.setAsBackUp()
										else:
											if self.arms[senjata['itemIndex']].name == senjata.name:
												if senjata.mag > 0:
													HUD.willUseStatusText = "add_ammo"
													if self.use == lepas and self.bundleX != None:
														size = self.arms[senjata['itemIndex']].magSize - 1
														magLeft = self.arms[senjata['itemIndex']].mag
														ygDiPerlukan = size - magLeft
														if self.arms[senjata['itemIndex']].reloadStatus == "abis":
															self.arms[senjata['itemIndex']].reloadStatus = "standBy"
														if ygDiPerlukan <= senjata.mag:
															sisa = senjata.mag - ygDiPerlukan
															ygDiambil = ygDiPerlukan
															senjata.mag = sisa
															self.arms[senjata['itemIndex']].mag += ygDiambil
														else:
															if ygDiPerlukan > 0:
																sisa = 0
																ygDiambil = senjata.mag
																senjata.mag = sisa
																self.arms[senjata['itemIndex']].mag += ygDiambil
															
											else:
												HUD.willUseStatusText = "replace_item " + self.arms[senjata['itemIndex']].name + " with " + senjata.name
												if self.use == lepas and self.bundleX != None:
													self.arms[senjata['itemIndex']].removeParent()
													#self.arms[senjata['itemIndex']].restoreDynamics()
													self.arms[senjata['itemIndex']].visible = True
													self.arms[senjata['itemIndex']] = senjata
													senjata.worldOrientation = self.bundleX.worldOrientation
													senjata.setParent(self.bundleX, False, True)
													if var.alwaysUseNewlyTakenItem == True:
														self.arms[self.currentWeapon].setAsBackUp()
														self.currentWeapon = senjata['itemIndex']
														senjata.setOnUse(self.bundleX)
													else:
														if self.currentWeapon == senjata['itemIndex']:
															senjata.setOnUse(self.bundleX)
														else:
															senjata.setAsBackUp()
								if 'vehicle' in lookAtObject:
									HUD.willUseStatusText = "Get in vehicle"
									if self.use == jaktif:
										var.player = lookAtObject
										lookAtObject.driveBy = self
										lookAtObject.useBy = "player"
										lookAtObject.tiks = 0
										self.position = lookAtObject.playerSeatPos.position
										self.worldOrientation = lookAtObject.playerSeatPos.worldOrientation
										self.setParent(lookAtObject)
										HUD.willUseStatusText = ""
										self['enableMouse'] = False
										if self.bundleX != None:
											self.bundleX['enableMouse'] = False
							else:
								HUD.willUseStatusText = ""
						else:
							print("error some object is not in list")
							HUD.willUseStatusText = "error some object is not in list"
					else:
						#print("look at Object is None")
						pass
							
					if self.changeWeapon1 == jaktif:
						isNone = True
						notNoneCount = 0
						notNoneList = []
						pa = len(self.arms)
						for i in self.arms:
							if i != None:
								isNone = False
								notNoneCount += 1
								notNoneList.append(i)
						if isNone == False:
							if notNoneCount > 1:
								temp = self.currentWeapon
								#print(''' -------------------------------- ''')
								for i in range(pa):
									if temp < pa-1:
										temp += 1
									else:
										temp = 1
									#print(temp)
									if self.arms[temp] != None:
										break
								#print(''' -------------------------------- ''')
								self.arms[self.currentWeapon].setAsBackUp()
								self.arms[temp].setOnUse(self.bundleX)
								self.currentWeapon = temp
							#elif notNoneCount == 1:
							#	self.currentWeapon = notNoneList[0]['itemIndex']
						
						#print(''' -------------------------------- ''')
						#print([isNone, notNoneCount])
						#print(''' -------------------------------- ''')
					'''
					for i in self.arms:
						if i != None:
							i['itemIndex'] == self.currentWeapon:
								i.checkFire(self.tembak)
							else:
								i.checkFire(nope)
					'''
				if self.arms[self.currentWeapon] != None:
					self.arms[self.currentWeapon].checkFire(self.tembak)
				
		except:
			checker.getInfo()
			bge.logic.endGame()
		
	def runBot(self):
		try:
			inVehicle = False
			if inVehicle == False:
				#ai script put here
				pass
		except:
			checker.getInfo()
			bge.logic.endGame()
			
def createSoldierWeapon(cont):
	own = cont.owner
	newWeapon = KX_soldierWeapon(own)
	newWeapon.setController(cont)
	for i in cont.actuators:
		cont.activate(i)
			
class KX_soldierWeapon(bge.types.KX_GameObject):
	def __init__(this, old_owner):
		this.tipe = None
		this.useBy = None
		this.cont = None
		this.ZBundle = None
		this.XBundle = None
		this.barelZ = None
		this.pBarelZ_poros = None
		this.barelX = None
		this.weaponGUI = None
		if 'weaponGUI' in this:
			this.weaponGUI = this['weaponGUI']
		
		this.barels = []
		this.unShootBarels = []
		for child in this.childrenRecursive:
			if 'createBarel' in child:
				this.barels.append(child)
		if len(this.barels) == 0:
			this.barels.append(this)
		
		this.shootOneByOne = False
		this.lockedTo = None
		this.velocity = 20
		this.output = Vector([0.0, 1.0, 0.0])
		this.ammoSize = 30
		if 'ammoSize' in this:
			this.ammoSize = this['ammoSize']
		this.magSize = 7
		if 'magSize' in this:
			this.magSize = this['magSize']
		this.ammo = this.ammoSize
		this.mag = this.magSize
		this.interval = 0.1
		if 'interval' in this:
			this.interval = this['interval']
		this.reloadTime = 2.0
		if 'reloadTime' in this:
			this.reloadTime = this['reloadTime']
		this.reloadTimeLeft = this.reloadTime
		this.autoReload = True
		this.isReloading = False#rencana tuk dihapus
		this.reloadStatus = "awal"
		this.lastTimeOfFire = datetime.datetime.now()
		#this.readyToFire = False
		#this.readyToFire = True
		this.shell = 'generic shell'
		if 'type' in this:
			this.tipe = this['type']
		if this.tipe == "linear":
			this.shell = "linear_shell"
		if 'shell' in this:
			this.shell = this['shell']
		this.scale = "[1.0, 1.0, 1.0]"
		if 'scale' in this:
			this.scale = this['scale']
		this.timeToLive = 11
		if 'timeToLive' in this:
			this.timeToLive = this['timeToLive']
		this.infinityAmmo = False
		if "infinityAmmo" in this:
			this.infinityAmmo = this['infinityAmmo']
		this.infinityMag = False
		if 'infinityMag' in this:
			this.infinityMag = this['infinityMag']
		this.resetAsMain = False
		if 'resetAsMain' in this:
			this.resetAsMain = this['resetAsMain']
		this.hideWhenUnused = True
		if 'hideWhenUnused' in this:
			this.hideWhenUnused = this['hideWhenUnused']
		
		if 'velocity' in this:
			this.velocity = this['velocity']
		
		this.aimPoint = None
		
	def setController(this, cont):
		this.cont = cont
		
	'''
	def parentkan(this, obj):
		this.setParent(obj, False, True)
		if this.resetAsMain == True:
			if 'pos' in this:
				exec("this.position = {0}".format(this['pos']))
	'''
	
	def setOnUse(this, parent):
		this.worldOrientation = parent.worldOrientation
		if 'pos' in this:
			exec("this.position = {0}".format(this['pos']))
		this.visible = True
		
	def setAsBackUp(this):
		if 'posWhenUnUsed' in this:
			exec("this.position = {0}".format(this['posWhenUnUsed']))
		else:
			this.position = [0,0,0]
		if this.hideWhenUnused == True:
			this.visible = False
			
	def setTipe(this, tipe):
		this.tipe = tipe
		if this.tipe == "linear":
			this.shell = "linear_shell"
		
	def setShootOneByOne(this):
		this.shootOneByOne = True
		this.unShootBarels = this.barels
						
	def checkFire(this, tembak):
		now = datetime.datetime.now()
		jarak = now - this.lastTimeOfFire
		
		if tembak == 2:
			#print("trying to fire weapon {0} with time a : {1} and time b : {2}".format(this.name, str(jarak.seconds), str(this.reloadTime)))
			#if this.mag > -1:
			if this.ammo > 0:
				interval = rTimeLeft(jarak, this.interval)
				if interval <= 0:
					this['fire'] = True
					if this.tipe != "melee":
						if this.shootOneByOne == False:
							for barel in this.barels:
								projectile = this.scene.addObject(this.shell, barel)
								if this.infinityAmmo == False:
									this.ammo -= 1
								projectile.worldOrientation = this.worldOrientation
								projectile.localLinearVelocity = Vector((this.output.x * this.velocity, this.output.y * this.velocity, this.output.z * this.velocity))
								projectile['speed'] = [this.output.x * this.velocity, this.output.y * this.velocity, this.output.z * this.velocity]
								#print('projectile has been shot with speed = {0}'.format(projectile.localLinearVelocity))
								this.lastTimeOfFire = datetime.datetime.now()
								projectile['shootWith'] = this.name
								projectile['scale'] = this.scale
								if this.useBy != None:
									projectile['useBy'] = this.useBy
								if 'timeToLive' in projectile:
									projectile['timeToLive'] = this.timeToLive
					else:
						if this.cont != None:
							pass
							#melee script here
			#sampe sini
		else:
			this['fire'] = False
								
		if this.ammo == 0:
			if this.reloadStatus == "standBy":
				this.reloadStatus = "gonnaReload"
			
		if this.reloadStatus == "awal":
			if this.infinityMag == False:
				if this.mag > 0:
					this.mag -= 1
			this.reloadStatus = "standBy"
		if this.reloadStatus == "gonnaReload":
			this.lastTimeOfFire = datetime.datetime.now()
			jarak = now - this.lastTimeOfFire
			this.reloadTimeLeft = rTimeLeft(jarak, this.reloadTime)
			this.reloadStatus = "isReloading"
		if this.reloadStatus == "isReloading":
			jarak = now - this.lastTimeOfFire
			this.reloadTimeLeft = rTimeLeft(jarak, this.reloadTime)
			if this.reloadTimeLeft <= 0.0:
				this.reloadStatus ="reloaded"
		if this.reloadStatus == "reloaded":
			if this.mag > 0:
				if this.infinityMag == False:
					this.mag -= 1
				this.ammo = this.ammoSize
			if this.mag == 0 and this.ammo == 0:
				this.reloadStatus = "abis"
			else:
				this.reloadStatus = "standBy"
				
				
vehicleList = [KX_VehicleObject, KX_TankObject, KX_AirPlaneObject]
terrainSensUnacceptedList = []
for i in projectileList:
	terrainSensUnacceptedList.append(i)
for i in vehicleList:
	terrainSensUnacceptedList.append(i)
	

# ---------------------------- GameNetWork Section ----------------------------
class KX_KeyBox(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		pass

class KX_SlideDoor(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		self.jarak = 2
		self.speed = 1.5 #meter per seconds
		self.localAxis = "x"
		
		self.currentPos = 0.0
		
		self.networkInfo = self['networkInfo']
		var.networkInfo[self.networkInfo] = False
	def run(self):
		try:
			haveToOpen = var.networkInfo[self.networkInfo]
			movespeed = 0.0
			if haveToOpen == True and self.currentPos < self.jarak:
				movespeed = self.speed / bge.logic.getLogicTicRate()
			if haveToOpen == False and self.currentPos > 0.0:
				movespeed = -self.speed / bge.logic.getLogicTicRate()
			self.currentPos += movespeed
			if self.localAxis == 'x':
				self.position.x += movespeed
			if self.localAxis == 'y':
				self.position.y += movespeed
			if self.localAxis == 'z':
				self.position.z += movespeed
			if self.localAxis == '-x':
				self.position.x -= movespeed
			if self.localAxis == '-y':
				self.position.y -= movespeed
			if self.localAxis == '-z':
				self.position.z -= movespeed
		except:
			checker.getInfo()
			bge.logic.endGame()
networkInfoList = [KX_SlideDoor]
# -----------------------------------------------------------------------------
		
	
		