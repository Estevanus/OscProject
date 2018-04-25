'''
This weapons script is made by G. E. Oscar Toreh

This script is playing one of vital role in the game

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
import bge
import random
import var
import triggerList
import mainscript
import checker
import options
import datetime
import traceback
from math import hypot, radians, degrees, cos, sin, atan, asin, acos, sqrt
from mathutils import Vector, Euler, Matrix, Color
import gameobjects
#import triggerHandling

barelX = 'pBarelX'
pBarelZ_poros = 'pBarelZ_poros'
barelZ = 'pBarelZ'
shell = 'generic shell'
aimPoint = 'aimPoint'

def deltaTimeToSeconds(dt):
	s = float(dt.days) * 24 * 60 * 60 + float(dt.seconds) + (dt.microseconds / 1000000)
	return s
	
def rTimeLeft(jarak, reloadTime):
	s = deltaTimeToSeconds(jarak)
	return reloadTime - s
		

		
def TrajectoryAngle(own, interceptPoint, velocity):
	try:
		scene = bge.logic.getCurrentScene()
		if 'calculate' not in own:
			own['calculate'] = True
		if 'trajectoryAngle' not in own:
			own['trajectoryAngle'] = ''
		else:
			try:
				gravity = scene.gravity.z
				own['reachable'] = True
				
				vec = interceptPoint.getVectTo(own)
				px = hypot(vec[1].x, vec[1].y) * vec[0]
				pz = vec[1].z * vec[0]
				
				#rumus pertama menggunakan plus berfungsi untuk rumus mortar
				#rad = atan((velocity**2 + sqrt(velocity**4-gravity*(gravity*px**2 + 2*pz*velocity**2))) / (gravity*px))
				
				#rumus kedua menggunakan minus
				rad = atan((velocity**2 - sqrt(velocity**4-gravity*(gravity*px**2 + 2*pz*velocity**2))) / (gravity*px))
				
				
				#rad = asin(jarak * gravity / velocity**2) / 2
						
				sRad = sin(rad)
				cRad = cos(rad)
				
				y = cRad * velocity
				z = sRad * velocity
				
				own['cosine'] = str([sRad, cRad])
				
				own['travelTime'] = px / y
				own['vy'] = y
				own['vz'] = z
				
				own['angle'] = degrees(rad)
				
				if own.parent == None:
					Eul = Euler((rad, 0, 0), 'XYZ')
				else:
					parent = own.parent
					pR = parent.worldOrientation
					pE = pR.to_euler()
					Eul = Euler((-rad, pE.y, pE.z), 'XYZ')
				own.worldOrientation = Eul.to_matrix()
				own['reachable'] = True
				own['calculate'] = True
			except ValueError:
				own['reachable'] = False
				if own['calculate'] == True:
					print("calculate error")
					own['calculate'] = False
			except ZeroDivisionError:
				print('float division by zero')
	except:
		checker.getInfo()
		bge.logic.endGame()
	

def runRadar(cont):
	cont.owner.run(cont)
'''	
def trackTo(self, target):
	pass
'''
class simpleObject:
	invalid = True

def setLock(self, sen, cam):
	self.lockOnStatus = "found"
	self.target = sen.hitObject
	self.lastLockPosition = cam.getScreenPosition(self.target)

class weapons(bge.types.KX_GameObject):
	angleToShot = radians(1.0)
	heldBy = None
	nama = "noName"
	def __init__(self, old_owner, heldBy):
		self.ticks = 0
		self.shootCount = 0
		self.shooterFactor = Vector((0, 0, 0))
		self.target = None
		self.lockedTo = None
		self.lockOnStatus = "searching"
		self.initialTimeToLock = 180.0
		self.lockingTime = 0.0
		self.isTracking = False
		self.lastLockPosition = None
		self.hideBarrelAfterShot = False
		if 'hideBarrelAfterShot' in self:
			self.hideBarrelAfterShot = self['hideBarrelAfterShot']
		
		if "createWeapon" in self:
			self.nama = self['createWeapon']
		self.heldBy = heldBy
		self.tipe = None
		self.weaponGUI = None
		if 'weaponGUI' in self:
			self.weaponGUI = self['weaponGUI']
		self.ZBundle = None
		self.XBundle = None
		self.barelZ = None
		self.pBarelZ_poros = None
		self.barelX = None
		self.barrels = []
		self.barrelsDeviation = []
		#self.unShootBarels = []
		self.currentBarrelIndex = 0
		for child in self.children:
			if 'createBarrel' in child:
				added = self.scene.addObject('kosongObject', child)#menambahkan object kosong tanpa apapun
				added.setParent(child)
				self.barrels.append(child)
				self.barrelsDeviation.append(added)
		if len(self.barrels) == 0:
			self.barrels.append(self)
			added = self.scene.addObject('kosongObject', self)
			added.setParent(self)
			self.barrelsDeviation.append(added)
		self.shootOneByOne = False
		if 'shootOneByOne' in self:
			self.shootOneByOne = self['shootOneByOne']
			#if self.shootOneByOne == True:
			#	self.unShootBarels = self.barrelsDeviation
		self.velocity = 20
		self.output = Vector([0.0, 1.0, 0.0])
		if 'output' in self:
			exec("self.output = Vector({0})".format(self['output']))
			print("-------------------------------------------------------------------")
			print(self.output)
			print(self.name)
			print("-------------------------------------------------------------------")
		self.ammoSize = 30
		if 'ammoSize' in self:
			self.ammoSize = self['ammoSize']
		self.magSize = 7
		if 'magSize' in self:
			self.magSize = self['magSize']
		self.ammo = self.ammoSize
		self.mag = self.magSize
		self.interval = 0.1
		if 'interval' in self:
			self.interval = self['interval']
		self.reloadTime = 2.0
		self.reloadTimeLeft = self.reloadTime
		if 'reloadTime' in self:
			self.reloadTime = self['reloadTime']
		self.autoReload = True
		self.isReloading = False#rencana tuk dihapus
		self.reloadStatus = "awal"
		self.lastTimeOfFire = datetime.datetime.now()
		self.deviation = 0.0
		if 'deviation' in self:
			self.deviation = radians(self['deviation'])
		if "angleToShot" in self:
			self.angleToShot = self['angleToShot']
		#self.readyToFire = False
		#self.readyToFire = True
		self.shell = shell
		if self.tipe == "linear":
			self.shell = "linear_shell"
		if 'projectile' in self:
			self.shell = self['projectile']
		self.scale = [1.0, 1.0, 1.0]
		if 'scale' in self:
			exec("self.scale = " + self['scale'])
		self.timeToLive = int(3 * bge.logic.getLogicTicRate())
		if 'timeToLive' in self:
			self.timeToLive = int(self['timeToLive'] * bge.logic.getLogicTicRate())
		
		if 'velocity' in self:
			self.velocity = self['velocity']
		
		n = self
		
		print("checking for budle for weapon {0} of {1}".format(str(self.nama), str(self.heldBy.name)))
		self.zRotSpeed = 0.6# = 180 / 5 /60
		self.zMinRot = 0.0
		self.zMaxRot = 0.0
		self.xRotSpeed = 0.6# = 180 / 5 /60
		self.xMinRot = -5
		self.xMaxRot = 80
		while (self.ZBundle == None or self.XBundle == None) and n.parent != None:
			if self.ZBundle == None:
				if 'bundleTurretZ' in n:
					self.ZBundle = n
					if 'limiteRot' not in self.ZBundle:
						self.ZBundle['limiteRot'] = False
					if 'rotSpeed' in self.ZBundle:
						#self.ZBundle['rotSpeed'] = 0.6# = 180 / 5 /60
						self.zRotSpeed = 180 / self.ZBundle['rotSpeed'] /60
					if "minRotZ" in self.ZBundle:
						self.zMinRot = self.ZBundle['minRotZ']
					if 'maxRotZ' in self.ZBundle:
						self.zMaxRot = self.ZBundle['maxRotZ']
					if 'degrees' not in self.ZBundle:
						self.ZBundle['degrees'] = 0.0
					print("adding bundleZ : " + str(self.XBundle))
				if 'bundleTurretX' in n:
					self.XBundle = n
					if 'rotSpeed' in self.XBundle:
						self.xRotSpeed = 180 / self.XBundle['rotSpeed'] /60
					if "minRotX" in self.XBundle:
						self.xMinRot = self.XBundle['minRotX']
					if 'maxRotX' in self.XBundle:
						self.xMaxRot = self.XBundle['maxRotX']
					print("adding bundleX : " + str(self.XBundle))
			#if self.ZBundle == None and self.XBundle == None:
			#	break
			if self.ZBundle != None and self.XBundle != None:
				print("end of searching")
				break
			if n.parent != None:
				n = n.parent
			else:
				print("end of searching")
				break
		
		
		self.aimPoint = None
		
	def setShootOneByOne(self):
		self.shootOneByOne = True
		self.unShootBarels = self.barrelsDeviation
		
	def setName(self, name):
		self.name = name
		
	def setTipe(self, tipe):
		self.tipe = tipe
		if self.tipe == "linear":
			#self.shell = "linear_shell"
			pass
		if self.ZBundle != None and self.XBundle != None:
			print("ZBundle dan XBundle tidak None pada weapon " + self.name)
			if self.tipe == 'balistic weapon':
				print("since self is balistic type of weapon then  it's going to check for requiring components")
				if pBarelZ_poros not in self.XBundle.children:
					print("found pBarelZ_poros in {0} of {1}".format(str(self.XBundle.children), self.name))
					self.pBarelZ_poros = self.scene.addObject(pBarelZ_poros, self.XBundle)
					self.pBarelZ_poros.setParent(self.XBundle)
					#print(" -------------------------- langkah satu pBarelZ_poros : {0}, -------------------------- ".format(self.pBarelZ_poros))
					if self.barelZ == None:
						self.barelZ = self.pBarelZ_poros.children[barelZ]
						print("adding {0} as barelZ for {1}".format(str(self.barelZ), self.name))
					if barelX not in self.barelZ.children:
						self.barelX = self.scene.addObject(barelX, self.barelZ)
						self.barelX.setParent(self.barelZ)
						print("adding {0} as barelZ for {1}".format(str(self.barelZ), self.name))
				else:
					print("pBarelZ_poros is already in {0} of {1}".format(str(self.XBundle.children), self.name))
					self.pBarelZ_poros = self.XBundle.children[pBarelZ_poros]
					self.barelZ = self.pBarelZ_poros.children[barelZ]
					print("adding {0} as barelZ for {1}".format(str(self.barelZ), self.name))
					self.barelX = self.barelZ.children[barelX]
					print("adding {0} as barelZ for {1}".format(str(self.barelZ), self.name))
					
				if aimPoint not in self.barelX.children:
					self.aimPoint = self.scene.addObject(aimPoint, self.barelX)
					self.aimPoint.position = Vector((0, 10, 0)) * self.barelX.worldOrientation + self.barelX.position
					self.aimPoint.setParent(self.barelX)
				else:
					self.aimPoint = self.barelX.children[aimPoint]
					
		
	''' ----------- It's unused for now
	def setZBundle(self, KX_GameObject):
		self.ZBundle = KX_GameObject
	def setXBundle(self, KX_GameObject):
		self.XBundle = KX_GameObject
	'''
	def TurretRot(self, target):
		scene = bge.logic.getCurrentScene()
		obj = scene.objects
		rot = self.ZBundle.worldOrientation
		lPos = target.position - self.ZBundle.position
		
		mat = lPos * self.ZBundle.worldOrientation
		tp = mat
		jarak = hypot(tp[0], tp[1])
		
		try:
			sdt = acos(tp[1] / jarak)
		except ZeroDivisionError:
			sdt = 0
		
		derajat = degrees(sdt)
		self.ZBundle['degreeLeft'] = derajat
		timeLeft = derajat / (self.zRotSpeed * 60)
		self.ZBundle['timeToTrack'] = timeLeft
		
		#print([self.ZMinRot, maxRot])
		if self.ZBundle['limiteRot'] == False:
			if mat[0] < 0:
				if derajat > self.zRotSpeed:
					self.ZBundle.applyRotation((0, 0, radians(self.zRotSpeed)), True)
					self.ZBundle['ready'] = False
				else:
					self.ZBundle.applyRotation((0, 0, radians(derajat)), True)
					self.ZBundle['ready'] = True
			if mat[0] > 0:
				if derajat > self.zRotSpeed:
					self.ZBundle.applyRotation((0, 0, radians(-self.zRotSpeed)), True)
					self.ZBundle['ready'] = False
				else:
					self.ZBundle.applyRotation((0, 0, radians(-derajat)), True)
					self.ZBundle['ready'] = True
		else:
			if mat[0] < 0:
				if self.ZBundle['degrees'] > self.zMinRot:
					if derajat > self.zRotSpeed:
						self.ZBundle.applyRotation((0, 0, radians(self.zRotSpeed)), True)
						self.ZBundle['degrees'] -= self.zRotSpeed
						self.ZBundle['ready'] = False
					else:
						self.ZBundle.applyRotation((0, 0, radians(derajat)), True)
						self.ZBundle['degrees'] -= derajat
						self.ZBundle['ready'] = True
			if mat[0] > 0:
				if self.ZBundle['degrees'] < self.zMaxRot:
					if derajat > self.zRotSpeed:
						self.ZBundle.applyRotation((0, 0, radians(-self.zRotSpeed)), True)
						self.ZBundle['degrees'] += self.zRotSpeed
						self.ZBundle['ready'] = False
					else:
						self.ZBundle.applyRotation((0, 0, radians(-derajat)), True)
						self.ZBundle['degrees'] += derajat
						self.ZBundle['ready'] = True
		
		self.ZBundle['cek'] = str(mat)
		
	def GunRot(self, target):
		scene = bge.logic.getCurrentScene()
		obj = scene.objects
		parent = self.XBundle.parent
		mainParent = self.XBundle.parent.parent
		rot = self.XBundle.worldOrientation
		lPos = (target.position - self.XBundle.position)
		
		mat = lPos * self.XBundle.worldOrientation
		tp = mat
		jarak = hypot(tp[1], tp[2])
		
		sdt = acos(tp[1] / jarak)
		
		derajat = degrees(sdt)
		self.XBundle['degreeLeft'] = derajat
		timeLeft = derajat / (self.xRotSpeed * 60)
		self.XBundle['timeToTrack'] = timeLeft
		
		if mat[2] < 0:
			if self.XBundle['degrees'] > self.xMinRot:
				if derajat > self.xRotSpeed:
					self.XBundle.applyRotation((radians(-self.xRotSpeed), 0, 0), True)
					self.XBundle['degrees'] -= self.xRotSpeed
					self.XBundle['ready'] = False
				else:
					self.XBundle.applyRotation((radians(-derajat), 0, 0), True)
					self.XBundle['degrees'] -= derajat
					self.XBundle['ready'] = True
			else:
				self.XBundle['ready'] = False
		if mat[2] > 0:
			if self.XBundle['degrees'] < self.xMaxRot:
				if derajat > self.xRotSpeed:
					self.XBundle.applyRotation((radians(self.xRotSpeed), 0, 0), True)
					self.XBundle['degrees'] += self.xRotSpeed
					self.XBundle['ready'] = False
				else:
					self.XBundle.applyRotation((radians(derajat), 0, 0), True)
					self.XBundle['degrees'] += derajat
					self.XBundle['ready'] = True
			else:
				self.XBundle['ready'] = False
				
		self.XBundle['cek'] = str(lPos)
		
	def rotateGun(interceptPoint):
		if self.ZBundle != None:
			self.TurretRot(interceptPoint)
		if self.XBundle != None:
			self.GunRot(interceptPoint)
						
	def checkFire(self, tembak):
		now = datetime.datetime.now()
		jarak = now - self.lastTimeOfFire
		
		if tembak == 2:
			#print("trying to fire weapon {0} with time a : {1} and time b : {2}".format(self.name, str(jarak.seconds), str(self.reloadTime)))
			if self.mag > -1:
				if self.ammo > 0:
					interval = rTimeLeft(jarak, self.interval)
					if interval <= 0:
						projectile = None
						if self.shootOneByOne == False:
							for barrel in self.barrelsDeviation:
								if self.hideBarrelAfterShot == True:
									barrel.parent.visible = False
								#print("dp scene ialah " + self.scene.name + " dengan objek " + self.self.name)
								#ator dp deviation
								nx = random.random() * self.deviation
								nx = nx - self.deviation / 2
								nz = random.random() * self.deviation
								nz = nz - self.deviation / 2
								deviation = Euler((nx, 0.0, nz))
								#print([nx, ny, nz, self.deviation])
								na = barrel.parent.worldOrientation
								#na.rotate(deviation)
								eul = Vector(na.to_euler()) + Vector(deviation)
								eul = Euler(eul)
								barrel.worldOrientation = eul.to_matrix()
								#cek = deviation, na.to_euler(), barrel.worldOrientation.to_euler()
								#print(cek)
								projectile = self.scene.addObject(self.shell, barrel, self.timeToLive)
						else:
							barrel = self.barrelsDeviation[self.currentBarrelIndex]
							if self.hideBarrelAfterShot == True:
								barrel.parent.visible = False
							nx = random.random() * self.deviation
							nx = nx - self.deviation / 2
							nz = random.random() * self.deviation
							nz = nz - self.deviation / 2
							deviation = Euler((nx, 0.0, nz))
							na = barrel.parent.worldOrientation
							eul = Vector(na.to_euler()) + Vector(deviation)
							eul = Euler(eul)
							barrel.worldOrientation = eul.to_matrix()
							#print("dp scene ialah " + self.scene.name + " dengan objek " + self.self.name)
							projectile = self.scene.addObject(self.shell, barrel, self.timeToLive)
							'''
							if 'type' in projectile:
								if projectile['type'] == "heatSeekingMissile":
									projectile = KX_SeekingMissile(projectile)
								else:
									projectile = KX_Projectile(projectile)
							else:
								projectile = KX_Projectile(projectile)
							self.ammo -= 1
							#print('dp putput = ' + str(self.output))
							#print("dp velocity = " + str(self.velocity))
							projectile.localLinearVelocity = Vector((self.output.x * self.velocity + self.heldBy.localLinearVelocity.x, self.output.y * self.velocity + self.heldBy.localLinearVelocity.y, self.output.z * self.velocity + self.heldBy.localLinearVelocity.z))
							#print('projectile has been shot with speed = {0}'.format(projectile.localLinearVelocity))
							self.lastTimeOfFire = datetime.datetime.now()
							projectile.shotWith = self.name
							projectile.shotBy = self.heldBy
							projectile.scaling = Vector(self.scale)
							projectile.target = self.target
							'''
							
							
							pb = len(self.barrelsDeviation)
							if pb > 1:
								self.currentBarrelIndex += 1
								if self.currentBarrelIndex > pb-1:
									self.currentBarrelIndex = 0
								#rint(self.currentBarrelIndex)
						if projectile != None:
							if 'type' in projectile:
								if projectile['type'] == "heatSeekingMissile":
									projectile = gameobjects.KX_SeekingMissile(projectile)
									projectile.target = self.lockedTo
									projectile.lockOnStatus = self.lockOnStatus
								else:
									projectile = gameobjects.KX_Projectile(projectile)
							else:
								projectile = gameobjects.KX_Projectile(projectile)
							self.ammo -= 1
							projectile.localLinearVelocity += Vector((self.output.x * self.velocity + self.heldBy.localLinearVelocity.x, self.output.y * self.velocity + self.heldBy.localLinearVelocity.y, self.output.z * self.velocity + self.heldBy.localLinearVelocity.z))
							#print('projectile has been shot with speed = {0}'.format(projectile.localLinearVelocity))
							projectile.lastVelocity = projectile.worldLinearVelocity
							self.lastTimeOfFire = datetime.datetime.now()
							projectile.shotWith = self.name
							projectile.shotBy = self.heldBy
							projectile.scaling = Vector(self.scale)
							self.shootCount += 1
		if self.ammo == 0:
			if self.reloadStatus == "standBy":
				self.reloadStatus = "gonnaReload"
			
		if self.reloadStatus == "awal":
			self.mag -= 1
			self.reloadStatus = "standBy"
		if self.reloadStatus == "gonnaReload":
			self.lastTimeOfFire = datetime.datetime.now()
			jarak = now - self.lastTimeOfFire
			self.reloadTimeLeft = rTimeLeft(jarak, self.reloadTime)
			self.reloadStatus = "isReloading"
		if self.reloadStatus == "isReloading":
			jarak = now - self.lastTimeOfFire
			self.reloadTimeLeft = rTimeLeft(jarak, self.reloadTime)
			if self.reloadTimeLeft <= 0.0:
				self.reloadStatus ="reloaded"
		if self.reloadStatus == "reloaded":
			if self.mag > 0:
				self.mag -= 1
				self.ammo = self.ammoSize
			if self.mag == 0 and self.ammo == 0:
				self.reloadStatus = "abis"
			else:
				self.reloadStatus = "standBy"
				if self.hideBarrelAfterShot == True:
					for barrel in self.barrels:
						barrel.visible = True
	
	def updateLockTarget(self, cont):
		sen = cont.sensors['Radar2']
		cam = self.scene.active_camera
		#print('vvvvvvvvvvvvvvvvvvvvvv')
		#print(self.lockOnStatus)
		#print(len(sen.hitObjectList))
		#print(sen.hitObjectList)
		#print("sensor positive is " + str(sen.positive))
		#---------- debug section ----------
		if self.heldBy.owner == var.PCO:
			if 'kunci' not in self:
				self['kunci'] = self.lockOnStatus
				self['lockingTime'] = str(self.lockingTime)
				self['target'] = str(id(self.target))
				self.addDebugProperty("kunci")
				self.addDebugProperty("lockingTime")
				self.addDebugProperty("target")
			else:
				self['kunci'] = self.lockOnStatus
				self['lockingTime'] = str(self.lockingTime)
				self['target'] = str(id(self.target))
		#-----------------------------------
		if sen.positive == True:
			hitObjectList = sen.hitObjectList
			if self.target in hitObjectList:
				if self.lockOnStatus == "locking":
					gotFlare = False
					for obj in hitObjectList:
						if 'flareObject' in obj:
							self.target = obj
							#self.lockOnStatus = "flareTrack"
							#print("there's flare here")
							gotFlare = True
							break
					if gotFlare == False:
						#algoritma waktu untuk melocknya
						if cam != None:
							p = cam.getScreenPosition(self.target)
							adding = 1.0
							a = hypot(p[0], p[1])
							if self.lastLockPosition == None:
								self.lastLockPosition = p
							b = hypot(self.lastLockPosition[0], self.lastLockPosition[1])
							self.lastLockPosition = p
							if a > b+0.1:
								adding = (b - a) * self.initialTimeToLock
							tertambah = self.lockingTime + adding
							if tertambah > -0.1:
								self.lockingTime = tertambah
							if self.lockingTime > self.initialTimeToLock:
								self.lockOnStatus = "locked"
								self.lastLockPosition = None
								self.lockingTime = 0.0
							else:
								self.lastLockPosition = p
				if self.lockOnStatus == "locked":
					ada = False
					for obj in hitObjectList:
						if id(self.target) == id(obj):
							ada = True
							self.lockedTo = self.target
							break
					#print('lockon status')
					#print(ada)
					if ada == False:
						self.lockOnStatus = 'searching'
						self.lockedTo = simpleObject()
			else:
				if len(hitObjectList) > 0:
					for obj in hitObjectList:
						if obj != None:
							if hasattr(obj, 'owner'):
								if obj.owner != None and self.heldBy.owner != None:
									if obj.owner.team != self.heldBy.owner.team:
										self.lockOnStatus = "locking"
										self.target = obj
										self.lastLockPosition = cam.getScreenPosition(self.target)
										self.isTracking = True
										break
							else:
								self.lockOnStatus = "locking"
								self.target = obj
								self.lastLockPosition = cam.getScreenPosition(self.target)
								self.isTracking = True
								break
				else:
					self.lockOnStatus = "searching"
					self.lockedTo = simpleObject()
					self.target = None
					self.isTracking = False
		else:
			self.lockOnStatus = "searching"
			self.target = None
			self.isTracking = False
			
		# --------------------------------------------------------------
		
		if self.heldBy == var.player:
			var.PCO.lockingObject = self.target
			var.PCO.singleLockStats = self.lockOnStatus
			var.PCO.isTracking = self.isTracking
	
	def run(self, interceptPoint, useBy):
		#print([self.name, self.tipe, self.ZBundle, self.XBundle])
		#cam = self.scene.active_camera
		
		if self.ZBundle != None and self.XBundle != None:
			lookAt = mainscript.lookAt
			#print("yang dilihat ialah " + str(lookAt))
			if self.tipe == 'balistic weapon':
				#print(" -------------------------- langkah dua pBarelZ_poros : {0}, -------------------------- ".format(self.pBarelZ_poros))
				if barelX in self.barelZ.children:
					#weapons type here
					if useBy == var.PCO:
						#trajectory script put here
						if self.lockedTo == None:
							if lookAt != None:
								#interceptPoint.position = lookAt
								trackTo = self.barelZ.actuators['trackTo']
								trackTo.object = interceptPoint
								self.barelZ.sensors['Always'].usePosPulseMode = True
								#print("calculating trajectory...")
								if self.velocity != None:
									TrajectoryAngle(self.barelX, interceptPoint, self.velocity)
									
							else:
								self.barelZ.sensors['Always'].usePosPulseMode = False
								
						self.TurretRot(self.aimPoint)
						self.GunRot(self.aimPoint)

			elif self.tipe == 'linear':	
				#linear script put here
				if useBy == 'player':
					rotateGun(self.ZBundle, self.XBundle, interceptPoint)
			elif self.tipe == 'visual_guided_missile':
				if useBy == 'player':
					rotateGun(self.ZBundle, self.XBundle, interceptPoint)
				'''
				if options.enableUnusedWeaponHeadingToPointer == True:
					if self.ZBundle != None:
						TurretRot(self.ZBundle, interceptPoint)
					if self.XBundle != None:
						GunRot(self.XBundle, interceptPoint)
				'''
		else:
			if self.XBundle != None:
				if self.tipe == "balistic weapon":
					#script yg cocok untuk tank masa depan contohnya tank covenant yg ada di HALO
					pass
				elif self.tipe == "linear":
					#script yg cocok untuk AAV versi masa depan
					self.GunRot(interceptPoint)
			if self.ZBundle != None:
				if self.tipe == 'linear':
					#script yg cocok untuk gun dari kapal
					pass
				elif self.tipe == "visual_guided_missile":
					self.TurretRot(interceptPoint)
		
def runGenericShell(cont):
	own = cont.owner
	now = datetime.datetime.now()
	if 'firstShot' not in own:
		own['firstShot'] = now
		if 'scale' not in own:
			own['scale'] = '[1.0, 1.0, 1.0]'
		else:
			try:
				exec("own.scaling = {0}".format(own['scale']))
			except:
				traceback.print_exc()
		if 'color' in own:
			try:
				exec("own.meshes[0].materials['shell'].diffuseColor = Color({0})".format(own['color']))
			except:
				traceback.print_exc()
		if 'emit' in own:
			own.meshes[0].materials['shell'].emit = own['emit']
	else:
		jarak = now - own['firstShot']
		if jarak.seconds > own['timeToLive']:
			own.endObject()
			
def runLinearShell(cont):
	own = cont.owner
	now = datetime.datetime.now()
	#print(own['speed'])
	if 'firstShot' not in own:
		own['firstShot'] = now
		if 'scale' not in own:
			own['scale'] = '[1.0, 1.0, 1.0]'
		else:
			try:
				exec("own.scaling = {0}".format(own['scale']))
			except:
				traceback.print_exc()
		if 'color' in own:
			try:
				exec("own.meshes[0].materials['shell'].diffuseColor = Color({0})".format(own['color']))
			except:
				traceback.print_exc()
		if 'emit' in own:
			own.meshes[0].materials['shell'].emit = own['emit']
	else:
		#own['speed']
		lt = bge.logic.getLogicTicRate()
		#print([lt, own['speed']])
		own.applyMovement([own['speed'][0] / lt, own['speed'][1] / lt, own['speed'][2] / lt], True)
		jarak = now - own['firstShot']
		if jarak.seconds > own['timeToLive']:
			own.endObject()
			
def runProjectile(cont):
	cont.owner.run(cont)
	
def updateLockOn(cont):
	'''
	own = cont.owner
	if 'versiKa2' in own:
		print('versi ka dua')
	else:
		print('versi pertama')
	
	sen = cont.sensors['Radar2']
	print(sen.positive)
	ids = []
	for i in sen.hitObjectList:
		ids.append(id(i))
	cek = [sen.positive, ids, sen.hitObjectList, id(var.player)]
	print(cek)
	if sen.positive == False:
		print('yeah sensor is negatif')
	print('---------------------------------------')
	'''
	try:
		if cont.owner.scene.name == 'inGame':
			if hasattr(cont.owner, 'updateLockTarget'):
				cont.owner.updateLockTarget(cont)
	except:
		checker.getInfo()
		bge.logic.endGame()
	
def setWeapons(own):
	scene = bge.logic.getCurrentScene()
	kamus = var.globalDict
	
	print('cheking weapon of {0}'.format(str(own)))
	
	#getting all weapons
	for i in own.childrenRecursive:
		#print('checking up arms of {0}'.format(str(i)))
		if 'createWeapon' in i:
			arm = weapons(i, own)
			arm.heldBy = own
			arm.useBy = own.owner
			#arm.setName(i['createWeapon'])
			tipe = ""
			if 'type' in arm:
				tipe = arm['type']
			arm.setTipe(tipe)
			own.weapons.append(arm)
			print('adding weapon {0} to {1}'.format(arm.name, str(own)))
	
	#settingpup weapon specs
