'''
An AI script that made by G. E. Oscar Toreh

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''

import bge
import var
from math import radians, degrees, sqrt, sin, cos, asin, acos, hypot
from mathutils import Vector, Color, Euler, Matrix
import gameobjects
import weapons
import checker

def enemyInBound(own, this_id):
	scene = bge.logic.getCurrentScene()
	
	
	near = own.sensors['Near']
	
	target = None
	
	#cek setiap 2 detik
	allFrame = scene['time']
	if allFrame % 120 == 0 and allFrame != 0:
		for i in near.hitObjectList:
			temp_target = id(i)
			if temp_target in scene['PCO_tim']:
				if scene['PCO_tim'][temp_target] != scene['PCO_tim'][this_id]:
					if target == None:
						target = [temp_target, own.getDistanceTo(i)]
					else:
						jarak = own.getDistanceTo(i)
						if jarak < target[1]:
							target = [temp_target, jarak]
							
	else:
		target = 'scanning'
	return target
	
def enemyInSight(own, this_id):
	scene = bge.logic.getCurrentScene()
	
	
	seen = own.sensors['Radar']
	
	target = None
	
	#cek setiap 2 detik
	allFrame = scene['time']
	if allFrame % 120 == 0 and allFrame != 0:
		for i in seen.hitObjectList:
			temp_target = id(i)
			if temp_target in scene['PCO_tim']:
				if scene['PCO_tim'][temp_target] != scene['PCO_tim'][this_id]:
					if target == None:
						target = [temp_target, own.getDistanceTo(i)]
					else:
						jarak = own.getDistanceTo(i)
						if jarak < target[1]:
							target = [temp_target, jarak]
	else:
		target = 'scanning'
							
	return target
							
				
	
def predik(attacker, target, bulletSpeed):

	toTarget = target.position - attacker.position

	a = target.worldLinearVelocity.dot(target.worldLinearVelocity) - (bulletSpeed * bulletSpeed)
	b = 2 * target.worldLinearVelocity.dot(toTarget)
	c = toTarget.dot(toTarget)

	p = -b / (2 * a)
	
	#print(' -------------------------------------- ')
	#print(' -------- Checking math domain -------- ')
	#print([b, a, c])
	#print(' -------------------------------------- ')
	
	q = sqrt((b * b) - 4 * a * c) / (2 * a)

	t1 = p - q
	t2 = p + q
	t = 0.0

	if t1 > t2 and t2 > 0:
		t = t2
	else:
		t = t1

	aimSpot = target.position + target.worldLinearVelocity * t
	return aimSpot
	
def predik2(attacker, target, bulletSpeed):

	toTarget = target.position - attacker.position

	a = (target.worldLinearVelocity-attacker.worldLinearVelocity).dot(target.worldLinearVelocity - attacker.worldLinearVelocity) - (bulletSpeed * bulletSpeed)
	b = 2 * (target.worldLinearVelocity-attacker.worldLinearVelocity).dot(toTarget)
	c = toTarget.dot(toTarget)

	p = -b / (2 * a)
	
	#print(' -------------------------------------- ')
	#print(' -------- Checking math domain -------- ')
	#print([b, a, c])
	#print(' -------------------------------------- ')
	
	q = sqrt((b * b) - 4 * a * c) / (2 * a)

	t1 = p - q
	t2 = p + q
	t = 0.0

	if t1 > t2 and t2 > 0:
		t = t2
	else:
		t = t1

	aimSpot = target.position + target.worldLinearVelocity * t
	return aimSpot
		
def interceptPrediction(self, weapon, target):
	if weapon.tipe == "linear":
		p = predik2(self, target, weapon.velocity)
	else:
		return target
	return p
	
def vektorkan(obj):
	if type(obj) == Vector:
		return obj
	else:
		return obj.position

def getBotList(team):
	if team != "all":
		return var.NPCList[team]
class KX_BotCommander:
	players = []
	cacheFokusMoveTo = None
	firstCommand = True
	def __init__(self):
		self.tiks = 0
	def setTeam(self, team):
		self.team = team
	def cheatAttackPlayer(self):
		t = var.player.team
		if t != self.team:
			self.players = getBotList(self.team)
			for NPC in self.players:
				NPC.destinedByCommander = [var.player, "goto"]
	def fokusAttackTo(self, area):
		for i in self.players:
			i.destinedByCommander = [area, "attack"]
	def fokusMoveTo(self, area):
		if self.firstCommand == True:
			self.players = getBotList(self.team)
			self.firstCommand = False
		#print("ok >>>>> " + str(self.players))
		for i in self.players:
			i.destinedByCommander = [area, "goto"]
	def executeFirstMove(self):
		if self.cacheFokusMoveTo != None:
			for i in self.players:
				i.destinedByCommander = [area, "goto"]
	def updateStrategy(self):
		pass
	def run(self):
		self.tiks += 1
		
def assignCommander(cont):
	var.botCommanderTeamA = KX_BotCommander()
	var.botCommanderTeamA.setTeam(1)
	var.botCommanderTeamB = KX_BotCommander()
	var.botCommanderTeamB.setTeam(2)
	cont.activate(cont.actuators['State'])
	
def runBotCommanderA(cont):
	var.botCommanderTeamA.run()
def runBotCommanderB(cont):
	var.botCommanderTeamB.run()
	
class KX_BotController(bge.types.KX_GameObject):
	firstMoveTo = None
	def __init__(self, old_owner):
		self.watingTime = var.botWaitingTime
		destinedByCommander = []#format [VectorGoTo, "reason"] . reason = attack, def, repair, dan sebagainya
		enemy = None
		enemyLastPos = None
		pass
		
	def goToLastLoatPosition(self):
		pass
		
	def findTheEnemyInCertainSeconds(self):
		pass
		
	def fight(self):
		pass
		
	def chaseTheEnemy(self):
		if self.enemyLastPos != None:
			if enemy.position == self.enemyLastPos:
				self.fight()
		self.enemyLastPos = enemy.position
		
	def run(self):
		if self.enemy != None:
			self.chaseTheEnemy()
	
def spawnTuBot(self):
	''' old one
	if self.isAllowToSpawn == True:
		if self not in var.botAntrianForSpawn:
			var.botAntrianForSpawn.append(self)
	'''
	#if self.isAllowToSpawn == True:
	if var.isFirstSpawn == False:
		if self.spawnLoc != None:
			#print([self.spawnLoc.name, self.spawnLoc.inUse, self.spawnLoc.antrian.index(self), len(self.spawnLoc.antrian)])
			if self in self.spawnLoc.antrian:
				if self.spawnLoc.antrian.index(self) == 0 and self.spawnLoc.inUse == False:
					for scene in bge.logic.getSceneList():
						if scene.name == "inGame":
							added = scene.addObject(var.teamPCO[self.team], self.spawnLoc)
							added = gameobjects.KX_AirPlaneObject(added)
							self.gameObject = added
							#added.useBy = self
							added.owner = self
							weapons.setWeapons(added)
							self.spawnLoc.delAntrian(self)
							self.spawnLoc.inUse = True
							return True
							break
						else:
							print("wrong scene on function spawnTuBot at ai.py")
			else:
				self.spawnLoc.updateAntrian(self)
	return False
	pass
class KX_BotVehicleController(bge.types.KX_GameObject):
	nick = None
	isFirstMove = True
	senseRadius = 200
	targetDiketahui = False
	team = 0
	
	#weapon section
	lenOfArms = 0
	
	def __init__(self, old_owner):
		#misc section
		self.deathCount = 0
		self.score = None
		self.gameObject = None#objek yg akan dirasuki bot
		self.team = 0#sementara dulu apply di tim 2
		self.isHuman = False
		self.isAllowToSpawn = False
		self.spawnLoc = None
		self.spawnTime = 15 * 60#default 15 detik dikalikan 60 ticks perdetik
		self.ticks = 0
		self.restPosition = self.position
		self.hasGameObjectUpdated = False
		
		#flight control priority
		self.flightStats = "needToTakeOff"
		self.waymesh = None
		self.wayPoints = []
		self.wayIndex = 0
		self.isDirectTrackToTujuan = False
		self.evadingStats = "None"
		
		#priority section
		self.watingTime = var.botWaitingTime
		self.destinedByCommander = []#format [VectorGoTo or objective object to go to, "reason"]
		self.lastQuestByCommander = []# = last self.destinedByCommander
		self.triggered = False#jika ada sesuatu yg memicuh prioritasnya sperti disuruh commander, ada teammatenya menunjukan lokasi musuh, dll maka triggerednya akan berubah true kemudian bot perlu mengecek prioritasnya lagi kemudian beraksi sesuai prioritas dan menonaktifkan kembali variable triggered untuk dipakai nanti
		self.enemy = None
		self.enemyLastPos = None
		self.speedWhenNoOrder = 0.0
		
		#heading initialization section
		self.xSdt = 0.0
		self.ySdt = 0.0
		self.zSdt = 0.0
		
		self.rangeToStartGoUp = 100
	def sensSekitar(self, evadeTo=None, mode=0):
		if self.gameObject.sensorSekitar != None:
			if self.gameObject.tiks > self.gameObject.sensorSekitar.triggerOnStartDelay:
				if self.gameObject.sensorSekitar.sen != None:
					if self.gameObject.tiks < self.gameObject.sensorSekitar.triggerOnStartDelay + 2:
						self.gameObject.sensorSekitar.sen.reset()
					if self.gameObject.sensorSekitar.touched:
						if self.planeCollidiongPrediction() == False:
							#some script for turning
							if self.gameObject.sensorSekitar.vec != None:
								if evadeTo == None:
									vec = self.gameObject.sensorSekitar.vec - self.gameObject.position
									#vec = self.gameObject.getVectTo(self.gameObject.sensorSekitar.vec)[2]
									#print([vec, self.gameObject.position])
									ma = Euler((0.0, 0.0, self.gameObject.worldOrientation.to_euler().z), 'XYZ').to_matrix()
									ar = vec.z
									if ar < 0:
										ar *= -1
									#self.trackTo(self.gameObject.position + vec + ma * Vector((0.0, ar, 0.0)))
									self.trackTo(self.gameObject.position + ma * Vector((0.0, ar, 0.0)) + Vector((0.0, 0.0, -vec.z)))
									'''
									if vec.z < 0:
										self.gameObject.pitchUp == 2
									else:
										self.gameObject.pitchUp == 0
									if vec.z > 0:
										self.gameObject.pitchDown == 2
									else:
										self.gameObject.pitchDown == 0
									'''
								else:
									if mode == 0:
										if type(evadeTo) == Vector:
											self.trackTo((evadeTo.x, evadeTo.y, hypot(evadeTo.x, evadeTo.y)))
										else:
											print("wrong type on sensSekitar")
							pass
					return self.gameObject.sensorSekitar.touched
				else:
					return False
		else:
			return False
	def altitudeAwareness(self):
		'''
		#rangeZ = self.gameObject.position - (Vector((0.0, 0.0, self.rangeToStartGoUp)) * self.gameObject.worldOrientation )
		rangeZ = self.gameObject.position + Vector((0.0, 0.0, -self.rangeToStartGoUp))
		hz = self.rayCastTo(rangeZ, self.rangeToStartGoUp, '')
		#print(rangeZ)
		if hz != None:
			#self.trackTo(self.gameObject.position + (Vector((0.0, 0.0, self.rangeToStartGoUp)) * self.gameObject.worldOrientation ))
			#self.trackTo(self.gameObject.position + Vector((0.0, 1.0, self.rangeToStartGoUp)))
			#print('yups
			return True
		else:
			return False
		'''
		if self.gameObject.senseOfAxis.invalid == True:
			#print("sensOfAxis is invalid returning False of altitudeAwareness")
			return False
		else:
			rays = self.gameObject.senseOfAxis.getRay()
			if 5 in rays:
				alt = rays[5]
				#cek = alt.hitObject, type(alt.hitObject), type(alt.hitObject) not in gameobjects.terrainSensUnacceptedList
				#print(cek)
				try:
					if alt.hitObject == self.gameObject:
						return False
					if type(alt.hitObject) not in gameobjects.terrainSensUnacceptedList:
						if alt.hitPosition == [0,0,0]:
							alt.range += 10
							if hasattr(self, 'lastAltitudeHitZ'):
								hitRange = self.gameObject.worldPosition.z - self.lastAltitudeHitZ
							else:
								hitRange = self.gameObject.worldPosition.z - alt.hitPosition[2]
						else:
							hitRange = self.gameObject.worldPosition.z - alt.hitPosition[2]
							self.lastAltitudeHitZ = alt.hitPosition[2]
						cek = self.gameObject.worldOrientation[2][1], self.gameObject.worldLinearVelocity.z
						if 'altitudeAwareness' not in self:
							self['altitudeAwareness'] = str(cek)
							#self.addDebugProperty('altitudeAwareness')
						else:
							self['altitudeAwareness'] = str(cek)
						#if hitRange < alt.range:
						if hitRange < self.gameObject.minimumHeightToFly:
							#cek = hitRange, alt.range, self.flightStats
							#print("info benar " + str(cek))
							if self.gameObject.worldLinearVelocity.z < 0.0:
								return True
							else:
								return False
						else:
							#print('hit Range above alt.range')
							#cek = self.team, hitRange
							#print(cek)
							if self.gameObject.worldLinearVelocity.z < 0:
								timeToFall = hitRange / self.gameObject.worldLinearVelocity.z
								if timeToFall > -self.gameObject.fallingTimeImpactWarning:
									#print('bot will fall to ground in {0} seconds'.format(str(timeToFall)))
									#print(cek)
									return True
								else:
									return False
							else:
								return False
					else:
						#print("hitobject in gameobjects.terrainSensUnacceptedList reason + " + str(alt.hitObject))
						return False
				except SystemError:
					#print("System error occur returning False to altitudeAwareness")
					return False
			else:
				#print("5 not in ray. Ref altitudeAwareness")
				return False
	
	def planeCollidiongPrediction(self):
		#(rangeX, rangeY, rangeZ) = self.gameObject.worldLinearVelocity * 3
		detik = 7
		range = self.gameObject.worldLinearVelocity * detik
		hitObject = self.rayCastTo(range)
		
		if hitObject != None:
			cek = range, hitObject
			#print('object {0} kan bertubrukan dalam waktu kurang dari {1} detik. status {2}'.format(id(self), str(detik), str(cek)))
			if range.z < 0:
				self.gameObject.pitchUp = 2
			else:
				self.gameObject.pitchUp = 0
			if range.z > 0:
				self.gameObject.pitchDown = 2
			else:
				self.gameObject.pitchDown = 0
			self.gameObject.jetControlTurning()
			return True
		else:
			return False
		
		
	
	def goToLastLoatPosition(self):
		pass
		
	def findTheEnemyInCertainSeconds(self):
		pass
		
	def fight(self):
		pass
		
	def chaseTheEnemy(self):
		if self.enemyLastPos != None:
			if enemy.position == self.enemyLastPos:
				self.fight()
		self.enemyLastPos = enemy.position
		
	def goToPosition(self):
		pass
		
	def getAirPlaneTurnFactor(self):
		pitchFactor = 1.0
		rollFactor = 1.0
		yawFactor = 1.0
		if self.gameObject.localLinearVelocity.y < self.gameObject.speedToPitch:
			pitchFactor = self.gameObject.localLinearVelocity.y / self.gameObject.speedToPitch
		if self.gameObject.localLinearVelocity.y < self.gameObject.speedToRoll:
			rollFactor = self.gameObject.localLinearVelocity.y / self.gameObject.speedToRoll
		if self.gameObject.localLinearVelocity.y < self.gameObject.speedToYaw:
			yawFactor = self.gameObject.localLinearVelocity.y / self.gameObject.speedToYaw
		return (pitchFactor, rollFactor, yawFactor)
	def resetHeading(self, axis):
		if axis == "X":
			self.xSdt = 0.0
		if axis == "Y":
			self.ySdt = 0.0
		if axis == "Z":
			self.zSdt = 0.0
	def heading(self, sdt, axis="X"):
		(pitchFactor, rollFactor, yawFactor) = self.getAirPlaneTurnFactor()
		if axis == "X":
			rot = 0.0
			status = 0
			xSdtTertambah = degrees(self.xSdt)+self.gameObject.botMaxRotX * pitchFactor
			if xSdtTertambah < sdt:
				ygDitambahkan = self.gameObject.botMaxRotX * pitchFactor
				rot = ygDitambahkan
				self.xSdt += ygDitambahkan
				status = 1
			elif xSdtTertambah == sdt:
				rot = ygDitambahkan
				self.xSdt += ygDitambahkan
				status = 2
			elif xSdtTertambah > sdt:
				rot = 0.0
				self.xSdt += radians(sdt) - self.xSdt
				status = 2
			else:
				return False
			
			#print(self.xSdt)
			if self.xSdt < sdt:
				self.gameObject.applyRotation([rot, 0, 0], True)
			else:
				status = 3
			return status#0 ialah false, 1 masih dalam proses, 2 pas selesai, 3 sdh lama selesai
		
	def trackTo(self, vektor, localPosition=False):
		if self.gameObject.tipe == "airplane":
			v = self.gameObject.getVectTo(vektor)
			if localPosition == False:
				mat = v[2]
			else:
				mat = v[1]
			#print(mat)
			try:
				sdt = acos(mat[1])
			except ZeroDivisionError:
				sdt = 0
			except ValueError:
				sdt = 0
			try:
				s = mat[0]
				if s < 0:
					s *= -1
				sdtY = asin(s)
			except ZeroDivisionError:
				print("zero division error when attempting to devide {0} against {1}".format(str(mat[0]), str(jarakY)))
				sdtY = 0
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
			derajatY = degrees(sdtY)
			derajatX = degrees(sdtX)
			#cek = [derajatX, mat, vektor]
			#cek = mat
			#print(cek)
			#self['cek'] = str([cek])
			#seksi pengecekan sisah rotasi untuk trackingnya bot plane
			if var.ngecek == True:
				self['sdtY'] = sdtY
				self['degreeYLeft'] = derajatY
				self['degreeXLeft'] = derajatX
				self['degreeZLeft'] = derajat
				self.addDebugProperty('degreeYLeft')
				self.addDebugProperty('degreeXLeft')
				self.addDebugProperty('degreeZLeft')
			
			rotZ = 0.0
			rotY = 0.0
			rotX = 0.0
			
			(pitchFactor, rollFactor, yawFactor) = self.getAirPlaneTurnFactor()
			
			if mat[0] < 0:
				if derajat > self.gameObject.maxRotZ:
					#self.applyRotation((0, 0, radians(self.speedZ)), True)
					rotZ = self.gameObject.maxRotZ
				else:
					#self.applyRotation((0, 0, radians(derajat)), True)
					rotZ = radians(derajat)
					sdtY = 0.0
				if sdtY > self.gameObject.maxRotY:
					rotY = -self.gameObject.maxRotY
				else:
					rotY = -sdtY
			if mat[0] > 0:
				if derajat > self.gameObject.maxRotZ:
					#self.applyRotation((0, 0, radians(-self.speedZ)), True)
					rotZ = -self.gameObject.maxRotZ
				else:
					#self.applyRotation((0, 0, radians(-derajat)), True)
					rotZ = radians(-derajat)
					sdtY = 0.0
				if sdtY > self.gameObject.maxRotY:
					rotY = self.gameObject.maxRotY
				else:
					rotY = sdtY
					
			if mat[2] < 0.0:
				#print(sdtX)
				if sdtX < self.gameObject.maxRotX:
					rotX = -self.gameObject.maxRotX
				else:
					rotX = -sdtX
			if mat[2] > 0.0:
				if sdtX > self.gameObject.maxRotX:
					rotX = self.gameObject.maxRotX
				else:
					rotX = sdtX
					
			#print([pitchFactor, rollFactor, yawFactor])
			self.gameObject.setAngularVelocity([rotX*pitchFactor, rotY*rollFactor, rotZ*yawFactor], True)
			'''
			'''
			self.gameObject.pitchUp = -rotX
			self.gameObject.pitchDown = -rotX
			self.gameObject.rollRight = rotY
			self.gameObject.rollLeft = rotY
			self.gameObject.turnL = rotZ
			self.gameObject.turnR = rotZ
			
			return derajatX, derajatY, derajat
	
	def updateGameObjectData(self):
		#script for update tu gameObject pe data
		self.isDirectTrackToTujuan = False
		
		if 'speedWhenNoOrder' in self.gameObject:
			try:
				self.speedWhenNoOrder = self.gameObject['speedWhenNoOrder'] / 3.6
				self.gameObject.angularDamping = 0.0#sementara, mungkin kan di ganti di masa depan nanti
			except ZeroDivisionError:
				self.speedWhenNoOrder = 0.0
		if "senseRadius" in self.gameObject:
			self.senseRadius = self.gameObject['senseRadius']
			self.flightStats = 'needToTakeOff'
			#self.destinedByCommander = []
			
		#coloring red for B team
		#mo kse beda warna for beda team mar ternyata karna dia pake mesh yang sama deng material yang sama maka dp hasil samua dapa :'v
		
		#weapkon section update
		self.lenOfArms = len(self.gameObject.weapons)
		if self.lenOfArms == 1:
			if self.gameObject.currentWeapon == None:
				self.gameObject.currentWeapon = self.gameObject.weapons[0]
				
		#reset waypoints index
		self.wayIndex = 0
				
		
	def setTargetBySensing(self, target, sens):
		if hasattr(target, "owner"):
			#print([self.team, target, target.owner.team])
			if hasattr(target.owner, "team"):
				if target.owner.team != self.team:
					if self.gameObject.rayCastTo(target) == target:
						self.target = target
						self.flightStats = "fighting"
						self.targetDiketahui = sens.positive
					else:
						self.target = None
						self.targetDiketahui = False
	tujuan = Vector((0.0, 0.0, 0.0))
	firstWayPoint = None
	waypointOfOrder = None
	#kong pake dp range dari waypoint tersebut
	def run(self):
		#tahap spawn
		if self.gameObject == None:
			self.hasGameObjectUpdated = False
			hasil = spawnTuBot(self)
			if hasil == True:
				if var.waymesh != None:
					if self.waymesh == None:
						self.waymesh = gameobjects.KX_WayMesh2(var.waymesh, self)
						self.wayPoints = self.waymesh.rebuildTrackList(self.gameObject, self.destinedByCommander[0])
		else:
			if self.gameObject.invalid == True:
				self.hasGameObjectUpdated = False
				self.target = None
				spawnTuBot(self)
				#print("bot need to spawn reference " + str(var.isFirstSpawn))
				#self.ticks = 0
			else:
				if self.hasGameObjectUpdated == False:
					#initializing scrpit for bot gameObject
					self.updateGameObjectData()
					pass
				self.hasGameObjectUpdated = True
				# -------- Note --------
				#mungkin nanti stw qt mo perlu pake tuh botAirPlaneSensingObject for bot awarness
				# ----------------------
				if 'evadingStats' not in self:
					self['evadingStats'] = "id {0} dari team {1} ialah {2}".format(str(id(self)), str(self.team), self.evadingStats)
					self.addDebugProperty('evadingStats')
				else:
					self['evadingStats'] = "id {0} dari team {1} ialah {2}".format(str(id(self)), str(self.team), self.evadingStats)
				if self.gameObject.tipe == "airplane":
					#bot for jetplane ------------
					#willCollide = self.planeCollidiongPrediction()
					tooLow = self.altitudeAwareness()
					(willCollide, evadeTo, asal, evadeList, crashTime) = self.gameObject.getImpactWarning()
					#if var.ngecek == True:
					if 'a' == 'a':
						status = 'status of ' + self.nick + " of team " + str(self.team)
						if status not in self:
							self[status] = self.flightStats
							self.addDebugProperty(status)
						else:
							self[status] = self.flightStats
					
					if self.flightStats == 'needToTakeOff':
						self.gameObject.maju = 2
						self.gameObject.runJetEngine()
						#tooLow = self.altitudeAwareness()
						#if self.sensSekitar() == False:
						#	self.trackTo(self.gameObject.position + self.gameObject.worldOrientation * Vector((0, 45, 20)))
						self.trackTo(self.gameObject.position + self.gameObject.worldOrientation * Vector((0, 45, 20)))
						if self.gameObject.tiks > self.gameObject.botTimeToFlight:
							self.flightStats = "askingOrder"
							self.restPosition = Vector(self.gameObject.position)
					elif self.flightStats == "askingOrder":
						if self.gameObject.localLinearVelocity.y < self.speedWhenNoOrder:
							self.gameObject.maju = 2
							self.gameObject.runJetEngine()
						self.trackTo(self.restPosition)
						#print("rest position on " + str(self.restPosition))
						self.tujuan = self.destinedByCommander[0]
						if self.isFirstMove == True:
							if self.destinedByCommander != []:
								#self.isFirstMove = False
								self.flightStats = "doingOrder"
								#setWayPoints
								if var.waymesh != None:
									if self.waymesh != None:
										self.wayPoints = self.waymesh.rebuildTrackList(self.gameObject, self.destinedByCommander[0])
						else:
							if self.destinedByCommander != self.lastQuestByCommander:
								self.flightStats = "doingOrder"
								#setWayPoints
								if var.waymesh != None:
									if self.waymesh != None:
										self.wayPoints = self.waymesh.rebuildTrackList(self.gameObject, self.destinedByCommander[0])
										#print("let's rebuild it again")
					elif self.flightStats == "doingOrder":
						if self.destinedByCommander[1] == "goto":
							if willCollide == True and asal == 'depan':
								self.gameObject.maju = 0
								self.gameObject.mundur = 2
							else:
								self.gameObject.maju = 2
								self.gameObject.mundur = 0
							self.gameObject.runJetEngine()
							tujuan = self.destinedByCommander[0]
							#cek = tooLow, self.altitudeAwareness()
							#print("status toolownya ialah " + str(cek))
							if tooLow == True:
								if self.waymesh != None:
									if self.isDirectTrackToTujuan == False:
										pa = len(self.wayPoints)
										#print("way count is " + str(pa))
										if pa > 0:
											try:
												node = self.wayPoints[self.wayIndex].position
											except:
												checker.getInfo()
												bge.logic.endGame()
											#sdt = self.gameObject.worldOrientation.to_euler().z
											#ma = Matrix.Rotation(sdt, 3, 'Z')
											#va = Vector((0, 50, 0)) * ma + Vector((0, 0, 40))
											#vt = va + self.gameObject.worldPosition
											z = hypot(node.x - self.gameObject.position.x, node.y - self.gameObject.position.y)
											vv = Vector((0, 0, z)).length
											vvt = Vector((node.x, node.y, self.gameObject.position.z + vv))
											self.trackTo(vvt)
											self.evadingStats = "altitude warning using waymesh to evade"
											#self.trackTo(node)
											bge.render.drawLine(self.gameObject.position, vvt, [1.0, 0.0, 0.0])
											#if self.gameObject.getDistanceTo(node) < 100.0:
											if self.gameObject.getDistanceTo(node) < self.waymesh.distToChangeNode:
												if self.wayIndex < pa - 1:
													self.wayIndex += 1
												else:
													self.isDirectTrackToTujuan = True
										else:
											print("error!!!!!!!!!!, pa is zero")
											bge.logic.endGame()
								else:
									sdt = self.gameObject.worldOrientation.to_euler().z
									ma = Matrix.Rotation(sdt, 3, 'Z')
									va = Vector((0, 50, 0)) * ma + Vector((0, 0, 40))
									self.trackTo(va + self.gameObject.worldPosition)
									self.evadingStats == "altitude warning without navigation"
									#print("tooLow is True, now this tracking to " + str(va + self.gameObject.worldPosition))
							else:
								if self.waymesh != None:
									if self.isDirectTrackToTujuan == False:
										pa = len(self.wayPoints)
										#print("way count is " + str(pa))
										if pa > 0:
											try:
												node = self.wayPoints[self.wayIndex].position
											except:
												checker.getInfo()
												bge.logic.endGame()
											
											nodeSpeed = -self.gameObject.worldLinearVelocity
											nodePos = node + nodeSpeed
											if willCollide == True and crashTime[asal] < self.gameObject.impactTimeWarning / 2:
												evadePos = evadeTo + self.gameObject.worldPosition
												self.trackTo(evadePos)
												bge.render.drawLine(self.gameObject.position, evadePos, [0.0, 1.0, 0.0])
												#if self.team == 2:
												#	print("not low evade dengan asal " + asal)
											else:
												self.trackTo(nodePos)
												#if self.team == 2:
												#	print("not low node")
											self.evadingStats = "using navmesh, not evading"
											bge.render.drawLine(self.gameObject.position, node, [1.0, 0.0, 0.0])
											#if self.gameObject.getDistanceTo(node) < 100.0:
											if self.gameObject.getDistanceTo(node) < self.waymesh.distToChangeNode:
												if self.wayIndex < pa - 1:
													self.wayIndex += 1
												else:
													self.isDirectTrackToTujuan = True
										else:
											print("error!!!!!!!!!!! pa is zero")
											bge.logic.endGame()
								else:
									#if self.sensSekitar(tujuan.position) == False:
									#	self.trackTo(tujuan)
									self.trackTo(tujuan)
									self.evadingStats = "not evading"
							if var.ngecek == True:
								self['trakKepada'] = str(tujuan)
								self.addDebugProperty('trakKepada')
					elif self.flightStats == "fighting":
						self.gameObject.maju = 2
						self.gameObject.runJetEngine()
						if self.target != None:
							if self.target.invalid == False:
								if self.gameObject.rayCastTo(self.target) != self.target:
									self.target = None
									self.targetDiketahui = False
									self.flightStats = 'doingOrder'
								else:
									if self.gameObject.getDistanceTo(self.target) < self.senseRadius or self.targetDiketahui == True:
										if self.lenOfArms > 1:
											#algoritma untuk pergantian senjata bagi bot
											pass
										#print(self.gameObject.currentWeapon)
										if self.gameObject.currentWeapon != None or self.gameObject.primaryWeapon != None:
											shotAble = False
											if self.gameObject.primaryWeapon != None:
												icept = vektorkan(interceptPrediction(self.gameObject, self.gameObject.primaryWeapon, self.target))
												ak = self.gameObject.getVectTo(icept)
												#ak = self.gameObject.getVectTo(self.target)
												if tooLow == False:
													#print(ak[2][1])
													if willCollide == False:
														if ak[2][1] < 0:
															#print("target {0} is behind {1}".format(id(self.target), id(self)))
															(xl, yl, zl) = self.trackTo((icept.x, icept.y, self.gameObject.position.z - var.mapKonfigurasi['gravity'] + 2))
															'''
															if ak[2][0] != 0:
																vrot = self.worldPosition + Vector((ak[2][0] * ak[0], 0.0, 0.0)) * self.worldOrientation
																(xl, yl, zl) = self.trackTo((vrot.x, vrot.y, self.gameObject.position.z - var.mapKonfigurasi['gravity'] + 2))
															else:
																(xl, yl, zl) = self.trackTo((icept.x, icept.y, self.gameObject.position.z - var.mapKonfigurasi['gravity'] + 2))
															'''

															#print('yes')
														else:
															shotAble = True
															(xl, yl, zl) = self.trackTo(icept)
													else:
														shotAble = False
														(xl, yl, zl) = self.trackTo(evadeTo)
												else:
													'''
													if ak[2][1] < 0:
														print("target {0} is behind {1}".format(id(self.target), id(self)))
														(xl, yl, zl) = self.trackTo((icept.x, icept.y, self.gameObject.position.z - var.mapKonfigurasi['gravity'] + 2))
													else:
														pass
													'''
													#print(self.gameObject.worldPosition.z)
													#print("tooLow is " + str(tooLow))
													#(xl, yl, zl) = self.trackTo((icept.x + 20, icept.y + 20, self.gameObject.worldPosition.z + 20))
													shotAble = False
													tinggi = hypot(icept.x - self.gameObject.worldPosition.x, icept.y - self.gameObject.worldPosition.y)
													(xl, yl, zl) = self.trackTo((icept.x, icept.y, self.gameObject.worldPosition.z + tinggi/2))
													self.evadingStats = "tooLow while fighting"
													#print(tinggi/2)
												agl = self.gameObject.primaryWeapon.angleToShot
											else:
												self.evadingStats = "not evading"
												(xl, yl, zl) = self.trackTo(interceptPrediction(self.gameObject, self.gameObject.currentWeapon, self.target))
												agl = self.gameObject.currentWeapon.angleToShot
											if var.ngecek == True:
												if 'dleft' not in self:
													self['dleft'] = str([xl, zl])
													self.addDebugProperty('dleft')
												else:
													self['dleft'] = str([xl, zl])
												
											#print(shotAble)
											if shotAble == True:
												if xl < agl and zl < agl:
													if self.gameObject.primaryWeapon != None:
														self.gameObject.primaryWeapon.checkFire(2)
													if self.gameObject.currentWeapon != None:
														if self.gameObject.currentWeapon.tipe == "heatSeekingMissile":
															if self.gameObject.currentWeapon.lockOnStatus == 'locked':
																self.gameObject.currentWeapon.checkFire(2)
														else:
															self.gameObject.currentWeapon.checkFire(2)
														pass
													#print("bot is trying to fire")
												else:
													if self.gameObject.primaryWeapon != None:
														self.gameObject.primaryWeapon.checkFire(0)
													if self.gameObject.currentWeapon != None:
														self.gameObject.currentWeapon.checkFire(0)
										else:
											self.trackTo(self.target)
									else:
										self.flightStats = "doingOrder"
							else:
								self.flightStats = "doingOrder"
								if self.waymesh != None:
									self.wayPoints = self.waymesh.rebuildTrackList(self.gameObject, self.destinedByCommander[0])
									self.wayIndex = 0
						else:
							self.flightStats = "doingOrder"
						
						self.lastQuestByCommander = self.destinedByCommander
				
				if self.gameObject.tipe == "soldier":
					if self.enemy != None:
						self.chaseTheEnemy()
				
				self.ticks += 1
				#self.gameObject.tiks += 1
				self.gameObject.run()
				#----------------------------
	
'''
def runBotCommanderTeamA(cont):
	var.botCommanderTeamA.run()
def runBotCommanderTeamB(cont):
	var.botCommanderTeamB.run()
'''