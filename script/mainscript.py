'''
This mainscript is made by G. E. Oscar Toreh


This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.


This script is one of vital script on this game
'''
import bge
import var
import triggerList
import HUD
import traceback
from json import loads as muat
from math import radians, degrees
from mathutils import Vector
import ai
import spawner
import gameobjects
import videoPlayer
import aud
import checker
import db

#mungkin nga mo perlu nih modul for collecting sampah object yg telah di freed
#import weakref, gc


#customizeone

lookAt = None
#lookAtObject = None


nope = bge.logic.KX_INPUT_NONE
jaktif = bge.logic.KX_INPUT_JUST_ACTIVATED
aktif = bge.logic.KX_INPUT_ACTIVE
lepas = bge.logic.KX_INPUT_JUST_RELEASED

class USER(str):
	team = 0
	spawnTime = 15*bge.logic.getLogicTicRate()
	spawnLoc = None
	ViewHitObjectList = []
	viewObjectNeededToUpdate = False
	gameObject = None
	lockingObject = None
	singleLockStats = None
	isTracking = False
	audDevice = var.audDevice
	handle_buffered = None
	setMouseToCenterPerFrame = True
	def __init__(self, old_owner):
		self.name = str(old_owner)
		self.nick = str(old_owner)
		self.score = None
		self.invalid = False
		#lockedAudioFile = bge.logic.expandPath("//") + 'audio'
		try:
			lockedAudioFile = bge.logic.expandPath("//") + 'audio'
			#lockedAudioFile = bge.logic.expandPath("//")
			factory = aud.Factory(lockedAudioFile + "//locked.ogg")
			self.factory_buffered = aud.Factory.buffer(factory)
			#cek = lockedAudioFile
			#print("USER class state = " + str(cek))
		except:
			checker.getInfo()
			bge.logic.endGame()
		'''
		'''
		pass
		
	def gotLocked(self):
		'''
		'''
		if self.handle_buffered == None:
			self.handle_buffered = self.audDevice.play(self.factory_buffered)
		else:
			if self.handle_buffered.status != aud.AUD_STATUS_PLAYING:
				if self.handle_buffered.status == False:
					self.handle_buffered = self.audDevice.play(self.factory_buffered)
				#self.handle_buffered.loop_count += 1
				#self.handle_buffered.resume()
				#print('status user gotlock ialah ' + str(self.handle_buffered.status))
				#print('got locked again')
		pass
		
	def updateViewIndicator(daftar):
		self.ViewHitObjectList = daftar
		self.viewObjectNeededToUpdate = True
		
	def run(self):
		if self.gameObject != None:
			if self.gameObject.invalid == False:
				if 'USER' not in self.gameObject:
					self.gameObject['USER'] = True
				self.gameObject.runPlayer()
				self.gameObject.run()
				if self.setMouseToCenterPerFrame == True:
					bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
		
def runUSER(cont):
	var.PCO.run()
	own = cont.owner
	if var.PCO.score != None:
		if 'userDamageStats' not in own:
			own['userDamageStats'] = str(var.PCO.score.damageCause)
			own.addDebugProperty('userDamageStats')
		else:
			own['userDamageStats'] = str(var.PCO.score.damageCause)
	
	
def timeInScene(cont):
	'''
	scene = bge.logic.getCurrentScene()
	if 'time' not in scene:
		scene['time'] = 0
	else:
		scene['time'] += 1
	'''
	var.totalTicks += 1
class simpleObject:
	invalid = True
def deklarasi(cont):
	kamus = var.globalDict
	own = cont.owner
	scene = own.scene
	world = scene.world
	#world.backgroundColor = [0.0, 0.0, 0.0]
	if var.PCO == None:
		nikLok = bge.logic.expandPath('//') + 'cfg/id.txt'
		f = open(nikLok)
		n = f.readline()
		var.PCO = USER(n)
		print('id user is ' + str(var.PCO))
		f.close()
	getUserScore(cont)
	if var.player == None:
		var.player = gameobjects.simpleObject()
	if 'objek' not in var.scene:
		var.scene['objek'] = {}
	#var.player = simpleObject()
	'''
	if 'aiobject' not in kamus:
		kamus['aiobject'] = {}
	if 'object_target' not in kamus:
		kamus['object_target'] = {}
	if 'lookAtObject' not in var.scene:
		var.scene['lookAtObject'] = None
	'''
	if 'lookAtRange' not in var.scene:
		var.scene['lookAtRange'] = None
	if 'rangeOfUse' not in kamus:
		kamus['rangeOfUse'] = 1.5
	if 'inGame' not in var.scene:
		var.scene['inGame'] = None
		
	#custom script section
	import customScript
	try:
		customScript.main()
	except:
		checker.getInfo()
		bge.logic.endGame()
		
def playGameMusic(cont):
	pass
	#for now I'm disabling this sound player
	'''
	if var.gMusic == None:
		var.gMusic = var.audDevice.play(var.gMusicBuff)
	else:
		if var.gMusic.status == False:
			var.gMusic = var.audDevice.play(var.gMusicBuff)
	'''
		
def disableMenuMusic(cont):
	speedToTurnOff = 0.00333333#it's about 5 second for song to turn off
	if var.gMusic != None:
		if var.gMusic.status == True:
			if var.gMusic.volume > speedToTurnOff:
				var.gMusic.volume -= speedToTurnOff
				#print(var.gMusic.volume)
			else:
				var.gMusic.stop()
				cont.owner.endObject()
		else:
			cont.owner.endObject()
		
def gotoMenuMaps(cont):
	sen = cont.sensors
	aktif = True
	for i in sen:
		if i.positive == False:
			aktif = False
	if aktif == True:
		for i in bge.logic.getSceneList():
			if i.name == 'vehiclePicker':
				i.end()
		cont.owner.scene.replace('menu_maps')
def setInGameScene(cont):
	var.scene['inGame'] = cont.owner.scene
	var.scene['camPosIsOn'] = None
	var.scene['playerLookAtObject'] = None
	var.scene['playerLookAtRange'] = None
	var.scene['playerLookAtPosition'] = None

def getControl(cont):
	own = cont.owner
	
	kamus = var.globalDict
	thislok = bge.logic.expandPath('//')
	
	#lok = thislok + "\\cfg\\control_fighter.json"
	lok = thislok + "\\cfg\\control.json"
	
	control = muat(open(lok).read())
	
	#control_fighter = control['control_fighter']
	
	if 'control' not in kamus:
		kamus['control'] = {}
	for i in control:
		#print(i)
		if i not in kamus['control']:
			kamus['control'][i] = {}
		for j in control[i]:
			exec("kamus['control']['{0}'][str(j)] = {1}".format(i, control[i][j]))
	print(kamus)
	#print(cekkey + " ialah : " + str(exec(cekkey)))
	#exec("print(bge.events.AKEY)")
	
def centeringMouse(cont):
	aktif = True
	for i in cont.sensors:
		if i.positive != 1:
			aktif = False
			
	if aktif == True:
		bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
	

def getID(cont):
	own = cont.owner
	dp_id = id(own)
	
	if 'a' not in own:
		own['a'] = None
		print(dp_id)
	
def cekKamus(cont):
	own = cont.owner
	kamus = var.globalDict
	
	if 'cekKamus' not in own:
		own['cekKamus'] = "checked"
		print(kamus)
		
def getLookAt(cont):
	global lookAt
	#global lookAtObject
	scene = bge.logic.getCurrentScene()
	mOver = cont.sensors['mOver']
	ray = cont.sensors['ray']
	'''
	var.scene['playerLookAtObject'] = None
	var.scene['playerLookAtRange'] = 0
	'''
	if var.player != None:
		if ray.positive:
			hitObject = ray.hitObject
			var.scene['playerLookAtObject'] = hitObject
			var.scene['playerLookAtRange'] = cont.owner.getDistanceTo(ray.hitPosition)
			if 'useBy' in hitObject:
				if hitObject['useBy'] != 'player':
					var.scene['playerLookAtPosition'] = ray.hitPosition
			else:
				var.scene['playerLookAtPosition'] = ray.hitPosition
		else:
			var.scene['playerLookAtPosition'] = None
		if mOver.positive:
			hitObject = mOver.hitObject
			#print(hitObject)
			#var.scene['lookAtObject'] = hitObject
			var.lookAtObject = hitObject
			var.scene['lookAtRange'] = cont.owner.getDistanceTo(mOver.hitPosition)
			#lookAtObject = hitObject
			if 'useBy' in hitObject:
				if mOver.hitObject['useBy'] != 'player':
					lookAt = mOver.hitPosition
			else:
				lookAt = mOver.hitPosition
			#lookAt = Vector((0, 50, 0))
		else:
			lookAt = None
	
minimapOpened = True	
def HUD_replacer_stats(cont):
	global minimapOpened
	own = cont.owner
	scene = bge.logic.getCurrentScene()
	keyboard = bge.logic.keyboard
	act1 = cont.actuators['minimap']
	act2 = cont.actuators['crosshair']
	keyev = keyboard.events
	if keyev[bge.events.ENTERKEY] == jaktif:
		if minimapOpened == False:
			cont.deactivate(act2)
			#act1.mesh = scene.objectsInactive['map plane'].meshes[0]
			cont.activate(act1)
			minimapOpened = True
		else:
			cont.deactivate(act1)
			cont.activate(act2)
			minimapOpened = False
			
def setEnvironmentLightning(cont):
	own = cont.owner
	if 'environmentLightning' in own:
		scene = var.scene['inGame']
		exec("scene.world.backgroundColor = " + own['environmentLightning'])

def exitGame(cont):
	scenes = bge.logic.getSceneList()
	for s in scenes:
		if s.name == 'inGame':
			scene = s
			
			print('temporary resuming the game...')
			scene.resume()
			
			print('adding objek pengeluar...')
			scene.addObject('pengexit')
			
def bersihkanInGame(cont):
	#disable pulse mode of all sensors of all objects
	scene = bge.logic.getCurrentScene()
	print('disabling usePosPulseMode of allObjects')
	for i in scene.objects:
		for j in i.sensors:
			j.usePosPulseMode = False
			
	print("removing all objects parent in inGame scene...")
	for i in scene.objects:
		i.removeParent()
	var.tikets = ['inf', 10, 10]
	var.navigator = None
	var.waymesh = None 
	var.waypoints = []
		
	try:
		#removing scene HUD
		print('removing HUD...')
		HUD.end()
	except AttributeError:
		print('HUD may not exist, ignoring...')
	
	#end all of objects of scene
	print('removing all objects...')
	for i in scene.objects:
		if i != cont.owner:
				i.endObject()
				
	# - section of variables cleaning -
	bersihkan = True
	if bersihkan == True:
		pass
	# ---------------------------------
	#cont.owner.endObject()
def pengeluar(cont):
	print('starting exiting sequence...')
	
	try:
		'''
		print('deleting the libs...')
		for i in bge.logic.LibList():
			bge.logic.LibFree(i)
		print('the libs has been cleared')
		'''
		
		print(bge.logic.LibList())
		bersihkanInGame(cont)
		print('exiting the game')
		bge.logic.endGame()
	except:
		print("there's something error in the script mainscript.py on pengeluar(cont)")
		traceback.print_exc()
			
def matikanPulseObjects(scene):
	for i in scene.objects:
		for j in i.sensors:
			j.usePosPulseMode = False
def bersihkanObjectDalamScene(cont, scene):
	#end all of objects of scene
	print('removing all objects...')
	for i in scene.objects:
		if i != cont.owner:
				i.endObject()
def goToMainMenu(cont):
	aktif = True
	for i in cont.sensors:
		if i.positive == False:
			aktif = False
	if aktif == True:
		cont.owner.scene.replace("main_menu")


# --------------------------------- Plugable Function --------------------------------- #

def tombol(cont):
	own = cont.owner
	mouse = bge.logic.mouse
	over = None
	for i in cont.sensors:
		if type(i) == bge.types.KX_MouseFocusSensor:
			over = i
	if over == None:
		cek = cont.owner, cont.sensors
		print('mouse over sensor not found. Ref ' + str(cek))
	else:
		if over.positive == True:
			if 'siap' in own:
				#taruh disini tuh script utama
				if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_RELEASED:
					if 'function' in own:
						fus = []
						#exec(own['function'] + '(cont)')
						#exec("bb = " + own['function'])
						exec('bb = 12')
						cek = "bb = " + own['function'], bb
						print(cek)
						for fu in fus:
							fu(cont)
			#script tambahan untuk pemastian
			if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_NONE:
				own['siap'] = True
	

def onMouseOver(cont):
	over = None
	for i in cont.sensors:
		if type(i) == bge.types.KX_MouseFocusSensor:
			over = i
	if over != None:
		own = cont.owner
		if 'visibilityOnOver' in own:
			if own['visibilityOnOver'] == True:
				if over.positive == True:
					own.visible = True
				else:
					own.visible = False
	
		
def removeSceneButton(cont):
	over = None
	klik = None
	for i in cont.sensors:
		if type(i) == bge.types.SCA_MouseSensor:
			if i.mode == 1 or i.mode == 2:
				klik = i
		if type(i) == bge.types.KX_MouseFocusSensor:
			over = i
			
	if over != None and klik != None:
		own = cont.owner
		if 'siap' in own:
			if 'removeScene' in own.getPropertyNames():
				if type(own['removeScene']) == str:
					if over.positive == True:
						mouse = bge.logic.mouse
						if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_SENSOR_JUST_DEACTIVATED and 'siap' in own:
							for i in bge.logic.getSceneList():
								if i.name == own['removeScene']:
									i.end()
						if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_NONE:
							own['siap'] = True
				else:
					print(cont.owner.name+'>>removeScene property must be string')
			else:
				print(cont.owner.name + '>>removeScene property not found')
	else:
		print(cont.owner.name +'>>one or two sensor is not meet requirement. Ref an mouse click and mouse over is require')

def goToSceneButton(cont):
	over = None
	klik = None
	for i in cont.sensors:
		if type(i) == bge.types.SCA_MouseSensor:
			if i.mode == 1 or i.mode == 2:
				klik = i
		if type(i) == bge.types.KX_MouseFocusSensor:
			over = i
			
	if over != None and klik != None:
		own = cont.owner
		if 'goto' in own:
			if type(own['goto']) == str:
				if over.positive == True:
					mouse = bge.logic.mouse
					if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_SENSOR_JUST_DEACTIVATED and 'siap' in own:
						cont.owner.scene.replace(own['goto'])
					if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_NONE:
						own['siap'] = True
			else:
				print(cont.owner.name+'>>goto property must be string')
		else:
			print(cont.owner.name + '>>goto property not found')
	else:
		print(cont.owner.name +'>>one or two sensor is not meet requirement. Ref an mouse click and mouse over is require')
	
# ------------------------------------------------------------------------------------- #

def resetTriggerList():
	#trigger freeing section
	triggerList.onSpawnLocAdded = []
	triggerList.onSpawnLocDestroyed = []
	triggerList.onSpawnLocChange = []
	
	triggerList.onMapOpen = []
	triggerList.onGameEnded = []
	triggerList.onControlPointHasTaken = []
	triggerList.onObjectiveHasDestroyed = []
	
	triggerList.onTicketReachZero = []
	
	triggerList.onWeaponShot = []
	triggerList.onPlayerHit = []
	triggerList.onPlayerChooseSpawn = []
	triggerList.onPlayerJoin = []
	triggerList.onPlayerSpawn = []
	triggerList.onPlayerKilled = []
	
	triggerList.onRadarUpdate = []
	#for i in dir(triggerList):
	#	triggerList.__getattribute__(i) = []
	#for i in triggerList:
	#	i = []
	#-----------------------
def pengQuitToMainMenu(cont):
	#by object peng back to main menu
	#bersihkanInGame(cont)
	# - section of variables cleaning -
	bersihkan = True
	if bersihkan == True:
		print("getting ingame scene and active scene to be freed")
		inGameS = None
		inGameMenuS = None
		for s in bge.logic.getSceneList():
			if s.name == "menu_ingame":
				inGameMenuS = s
				inGameMenuS.end()
			if s.name == "inGame":
				inGameS = s
		print("disabling all objects pulse mode in inGame scene...")
		matikanPulseObjects(inGameS)
		
		print("removing all objects parent in inGame scene...")
		for i in inGameS.objects:
			i.removeParent()
		
		print('making lookAt = None')
		#mainscript.lookAt = None
		global lookAt
		lookAt = None
		
		print('deleting the unused memory...')
		kamus = var.globalDict
		#del kamus['aiobject']
		#del kamus['object_target']
		#var.spawnLocations = {}
		var.totalTicks = 0
		var.totalTime = 0.0
		#var.spawnLocations = []
		var.spawnLocByTeam = [[], [], []]
		var.controlPoints = [[], [], []]#format [daftarNeutralCP, daftarTeam1CP, daftarTeam2CP]
		var.destroyableObjective = [[], [], []]
		var.objectsThatNeedToSpawn = {}
		var.botCommanderTeamA = None
		var.botCommanderTeamB = None
		var.NPCList = [[], [], []]#0 for netral, 1 for team 1, 2 for team 2
		#var.players = [[], [], []]#0 for netral, 1 for team 1, 2 for team 2
		var.tikets = ['inf', 10, 10]
		var.ticketsObject = []
		var.navigator = None
		var.waymesh = None
		var.waypoints = []
		for i in var.scene['bots']:
			if i.invalid == False:
				i.endObject()
		if var.player != None:
			if var.player.invalid == False:
				var.player.endObject()
				#var.player = simpleObject()
		print("cek ingame scene objects")
		if "FighterAlo" in inGameS.objects:
			inGameS.objects['FighterAlo'].endObject()
			
		print(inGameS.objects)
		var.scene = {}
		var.player = None
		var.lookAtObject = None
		var.isFirstSpawn = True
		var.botAntrianForSpawn = []
		var.igem_buffered = None
		
		resetTriggerList()
		
		#HUD.end()
		'''
		'''
		if HUD.HUD != None:
			HUD.HUD.end()
			HUD.HUD = None
		print('deleting the libs...')
		for i in bge.logic.LibList():
			bge.logic.LibFree(i)
			#mari ba debugging dulu tare
			#cek = [type(i), i]
			#print(str(cek))
			pass
		print('the libs has been cleared')
		
		#print("membersihkan sisah2 object dalam inGame scene...")
		#bersihkanObjectDalamScene(cont, inGameS)
		#print("done")
		if var.gotoScoreBoard == False:
			cont.owner.scene.replace("main_menu")
		else:
			inGameS.replace("ScoreBoard")
			var.gotoScoreBoard = False
		
	# ---------------------------------

def parentViewPointToCam(cont):
	viewPoint = scene.objects['viewPoint']
	if 'viewPoint' not in scene:
		scene['viewPoint'] = viewPoint
	cam = scene.active_camera
	viewPoint.position = Vector([0, 20, 0])
	viewPoint.setParent(cam)
		
	
def centeringMouse(cont):
	bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
	for i in cont.actuators:
		cont.activate(i)
	
def konfirmEnabligMouseLook(cont):
	print('enabling mouse look')
	
def tankCamPosHere(cont):
	camera = bge.logic.getCurrentScene().objects['camPos']
	#porosKamera = bge.logic.getCurrentScene().objects['porosKamera']
	own = cont.owner
	
	#print(" ------------------------ AAAAAAAAAAAAAAAAAAAA {0} --------------------------- ".format(str(own)))
	
	if 'camPos' in own:
		#porosKamera.position = own.position
		#porosKamera.worldOrientation = own.worldOrientation
		#porosKamera.worldTransform = own.worldTransform
		if 'camPosIsOn' in var.scene:
			#own['camPosIsParented'] = True
			if var.scene['camPosIsOn'] != own:
				var.scene['camPosIsOn'] = own
				#exec("camera.position = own.position + (own.worldOrientation * Vector(" + own['camPos'] + "))")
				#camera.worldOrientation = porosKamera.worldOrientation
				#camera.setParent(porosKamera)
				#look =  cont.actuators['Look']
				#print('trying to enable mouse look')
				#own.sendMessage('enableMouseLook', "", "porosKamera")
				for i in own.childrenRecursive:
					if 'setAsPrimaryCam' in i:
						camera.position = i.position
						camera.worldOrientation = i.worldOrientation
						camera.setParent(i)
						i['enableMouse'] = True
						break
			
	else:
		camera.position = own.position
		#pass
		
def signSpawnPointInUse(cont):
	own = cont.owner
	if hasattr(own, "setInUse"):
		own.setInUse()
def signSpawnPointNotUse(cont):
	own = cont.owner
	if hasattr(own, "setNotUse"):
		own.setNotUse()
def cekSpawnPointIsUsed(cont):
	own = cont.owner
	if hasattr(own, "inUse"):
		own.inUse = cont.sensors['Near'].positive
		#print(own.inUse)
								
def botEyes(cont):
	own = cont.owner
	if "Radar" in cont.sensors:
		if own == var.player:
			#var.PCO.updateViewIndicator(cont.sensors['Radar'].hitObjectList)
			var.objectsInView = list(cont.sensors['Radar'].hitObjectList)
			#var.objectsInView = cont.sensors['Radar'].hitObjectList
			for pemicuh in triggerList.onRadarUpdate:
				pemicuh(cont.sensors['Radar'].hitObjectList)
			#print(var.PCO.ViewHitObjectList)
			pass
		else:
			if hasattr(own, "setTarget"):
				own.setTarget(cont.sensors['Radar'].hitObject, cont.sensors['Radar'])
				#print(cont.sensors['Radar'].positive)
				pass

def player_object(cont):
	own = cont.owner
	kamus = var.scene
	if var.player == own:
		#playerCamPosHere(cont)
		if 'cont' not in own:
			own['cont'] = cont
		if 'hasRaySensor' not in own:
			if 'Ray' in cont.sensors:
				print("checking the availablelity of ray sensor in " + str(own))
				if type(cont.sensors['Ray']) == bge.types.KX_RaySensor:
					own.raySensor = cont.sensors['Ray']
					print("applying Ray Sensor to object " + str(own))
					own['hasRaySensor'] = True
		own.runPlayer()
	else:
		pass
		#cek if run by bot then
		#	own.runBot()
		#else:
		#	hide and parent to something kind of vehicle
		
def botController(cont):
	cont.owner.run()
	
def touching(cont):
	own = cont.owner
	if hasattr(own, 'onTouched'):
		own.onTouched()
		
def collide(cont):
	cont.owner.onCollide()
	
def setNavigator(cont):
	if type(cont.owner) == bge.types.KX_NavMeshObject:
		var.navigator = cont.owner
	
def setWayMesh(cont):
	#if type(cont.owner) == bge.types.KX_NavMeshObject:
	#	#var.waymesh = gameobjects.KX_WayMesh(cont.owner)
	var.waymesh = cont.owner
		
def createWaypoint(cont):
	#wp = gameobjects.KX_WayPoint(cont.owner)
	#var.waypoints.append(wp)
	#it may not be needed
	pass
	
def playEndingMusic(cont):
	own = cont.owner
	song = None
	var.gotoScoreBoard = True
	if var.lastWiningTeam == var.PCO.team:
		song = var.wigem
	else:
		song = var.ligem
	if var.igem_buffered == None:
		var.igem_buffered = var.audDevice.play(song)
	else:
		#print('song should be end for now')
		#cek = var.igem_buffered.status, own['tik']
		#print(cek)
		if var.igem_buffered.status == False:
			if own['tik'] > own['delay']:
				#print('time to end this')
				for trigger in triggerList.onGameEnded:
					trigger()
				if 'peng back to main menu' not in cont.owner.scene:
					cont.owner.scene.addObject('peng back to main menu')
			own['tik'] += 1
			pass

def setUpVideoPlayer(cont):
	'''
	gameobjects.KX_VideoPlayer(cont.owner)
	for i in cont.actuators:
		cont.activate(i)
	'''
	own = cont.owner
	'''
	if 'vp' not in own:
		f = open(var.thisLok + 'init movie.txt')
		d = f.read()
		f.close()
		daftarVideo = d.split('\n')
	'''
	if 'vp' not in own:
		f = open(var.thisLok + 'init movie.txt')
		d = f.read()
		f.close()
		daftarVideo = d.split('\n')
		vp = videoPlayer.videoPlayer(cont.owner)
		#vp.daftar = daftarVideo
		vp.addRange(daftarVideo)
		#vp.play(daftarVideo[0])
		#vp.setMaterialName("dummy")
		own['vp'] = vp
	else:
		vp = own['vp']
		#vp.play()
		vp.refresh2()
		if vp.status == 'finish':
			#pergi ke main menu
			own.scene.replace('main_menu')
			own['vp'] = None
			del vp
			pass

def playVideos(cont):
	own = cont.owner
	if 'playlist' in own:
		if 'vp' not in own:
			f = open(var.thisLok + own['playlist'])
			d = f.read()
			f.close()
			daftarVideo = d.split('\n')
			vp = videoPlayer.videoPlayer(cont.owner)
			vp.addRange(daftarVideo)
			if 'repeat' in own:
				vp.repeat = own['repeat']
			own['vp'] = vp
		else:
			vp = own['vp']
			#vp.play()
			vp.refresh2()
			if vp.status == 'finish':
				#pergi ke main menu
				if 'changeScene' in own:
					own.scene.replace('main_menu')
					own['vp'] = None
					del vp
class TextAdder:
	def __init__(self):
		self.daftar = []
		self.sen = None
		self.lastHitObject = None
		self.lastOverOn = None
		self.lastClickOn = None
		self.theChoosenOne = None
	def run(self):
		if self.sen != None:
			mouse = bge.logic.mouse
			if self.lastOverOn != None:
				if self.lastOverOn != self.sen.hitObject:
					self.lastOverOn.visible = False
					
			if self.sen.hitObject in self.daftar:
				if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_SENSOR_JUST_ACTIVATED:
					if self.sen.hitObject.name + "_child" in self.sen.hitObject.children:
						self.sen.hitObject.children[self.sen.hitObject.name + "_child"].visible = True
						if self.lastClickOn != self.sen.hitObject and self.lastClickOn != None:
							self.lastClickOn.children[self.sen.hitObject.name + "_child"].visible = False
					self.theChoosenOne = self.sen.hitObject
					self.lastClickOn = self.sen.hitObject
				
				self.sen.hitObject.visible = True
				self.lastOverOn = self.sen.hitObject
				

def showMapList(cont):
	own = cont.owner
	if 'maps' not in cont.owner:
		root = bge.logic.expandPath("//")
		maps = bge.logic.getBlendFileList("//maps")
		own['maps'] = []
		#print(maps)
		for i in maps:
			added = own.scene.addObject(own['textPlane'], own)
			added = gameobjects.KX_TextPlane(added)
			added.replaceText = ".blend"
			added.setText(i)
			added.setScale(own['scale'])
			#nanti pikirkan lagi sbantar jo tu parent
			#added.setParent(own)
			own['maps'].append(added)
			#cek = i, added, id(added), added.position
			#print(cek)
			#own.position.y -= own['scale']
			own.position.y -= own['scale']
			#added.children[0].text = i.replace('.blend', '')
	else:
		if 'hasParent' not in own:
			for i in cont.owner['maps']:
				i.setParent(cont.owner)
			own['hasParent'] = True
		else:
			if 'control' not in own:
				own['control'] = TextAdder()
				own['control'].daftar = own['maps']
				own['control'].sen = cont.sensors['mOver']
			else:
				own['control'].run()
				if own['control'].theChoosenOne != None:
					var.globalDict['map'] = own['control'].theChoosenOne.text
					var.map = own['control'].theChoosenOne.text
				
def openMapButton(cont):
	over = None
	klik = None
	for i in cont.sensors:
		if type(i) == bge.types.SCA_MouseSensor:
			if i.mode == 1 or i.mode == 2:
				klik = i
		if type(i) == bge.types.KX_MouseFocusSensor:
			over = i
			
	if over != None and klik != None:
		own = cont.owner
		if over.positive == True:
			mouse = bge.logic.mouse
			if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_SENSOR_JUST_DEACTIVATED and 'siap' in own:
				#main command
				if var.map == None:
					#cont.activate((cont.actuators['FalseSound'])
					ac = cont.actuators['FalseSound']
					cont.activate(ac)
				else:
					ac = cont.actuators['TrueSound']
					cont.activate(ac)
					bge.logic.addScene('loading')
					own.scene.replace('inGame')
			if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_NONE:
				own['siap'] = True

def addScore(player, score):
	if hasattr(player, 'team') and hasattr(player, 'nick'):
		#var.players[player.team][var.players.index(player.nick)].point += score
		player.score.point += score
		return True
	else:
		return False
		
def addKill(killer, victim):
	try:
		if hasattr(killer, 'score'):
			if killer.team == victim.team:
				killer.score.teamkill += 1
			else:
				killer.score.kill += 1
			return True
		else:
			return False
	except:
		checker.getInfo()
		bge.logic.endGame()

def getSpawnAs(cont):
	cont.owner.text = "Spawn As " + var.spawnAs
	
	
def runCustomCredits(cont):
	own = cont.owner
	if 'ok' not in own:
		own['ok'] = True
		bl = bge.logic.getBlendFileList("//Credits")
		lok = "//Credits//" + bl[0]
		if lok not in bge.logic.LibList():
			bge.logic.LibLoad(lok, "Scene")
			
def getNick(cont):
	cont.owner.text = var.PCO.nick
	
def setNick(cont):
	own = cont.owner
	aktif = True
	for i in cont.sensors:
		if i.positive == False:
			aktif = False
			break
	if aktif == True:
		if 'nick' in own:
			var.PCO.nick = own['nick']
			f = open(var.nickLok, 'w')
			f.write(own['nick'])
			f.close()
			for j in cont.actuators:
				cont.activate(j)
		else:
			print('nick property not found')
		
def toggleFullscreen(cont):
	over = None
	klik = None
	for i in cont.sensors:
		if type(i) == bge.types.SCA_MouseSensor:
			if i.mode == 1 or i.mode == 2:
				klik = i
		if type(i) == bge.types.KX_MouseFocusSensor:
			over = i
			
	if over != None and klik != None:
		own = cont.owner
		if over.positive == True:
			mouse = bge.logic.mouse
			if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_SENSOR_JUST_DEACTIVATED and 'siap' in own:
				#main command
				fs = bge.render.getFullScreen()
				if fs == True:
					bge.render.setFullScreen(False)
				else:
					bge.render.setFullScreen(True)
			if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_NONE:
				own['siap'] = True
		
def setResolution(cont):
	over = None
	klik = None
	for i in cont.sensors:
		if type(i) == bge.types.SCA_MouseSensor:
			if i.mode == 1 or i.mode == 2:
				klik = i
		if type(i) == bge.types.KX_MouseFocusSensor:
			over = i
			
	if over != None and klik != None:
		own = cont.owner
		if over.positive == True:
			mouse = bge.logic.mouse
			if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_SENSOR_JUST_DEACTIVATED and 'siap' in own:
				#main command
				if 'width' in own and 'height' in own:
					bge.render.setWindowSize(own['width'], own['height'])
			if mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_NONE:
				own['siap'] = True
				
def showControlList(cont):
	own = cont.owner
	if 'control' not in cont.owner:
		root = bge.logic.expandPath("//")
		lok = var.thisLok + "\\cfg\\control.json"
		#cfg = muat(open(lok).read())
		control = muat(open(lok).read())
		own['control'] = []
		#print(control)
		for i in control:
			added = own.scene.addObject(own['textPlane'], own)
			added = gameobjects.KX_TextPlane(added)
			added.setText(i)
			added.setScale(own['scale'])
			#nanti pikirkan lagi sbantar jo tu parent
			#added.setParent(own)
			own['control'].append(added)
			#cek = i, added, id(added), added.position
			#print(cek)
			#own.position.y -= own['scale']
			own.position.y -= own['scale']
			#added.children[0].text = i.replace('.blend', '')
	else:
		if 'hasParent' not in own:
			for i in cont.owner['control']:
				i.setParent(cont.owner)
			own['hasParent'] = True
		else:
			if 'bind' not in own:
				own['bind'] = TextAdder()
				own['bind'].daftar = own['control']
				own['bind'].sen = cont.sensors['mOver']
			else:
				own['bind'].run()
				if own['bind'].theChoosenOne != None:
					mouse = bge.logic.mouse
					if mouse.events[bge.events.LEFTMOUSE] == 3:
						var.globalDict['lastSelectionControl'] = own['bind'].theChoosenOne.text
						for act in cont.actuators:
							cont.activate(act)
							
def setup_keybinding(cont):
	gameobjects.KX_KeyBinding(cont.owner)
	#print("------------------------------------------")
	#cek = var.globalDict['lastSelectionControl']
	#print(cek)
	#print("------------------------------------------")
	for act in cont.actuators:
		cont.activate(act)
		
def saveKeyBinding(cont):
	cont.owner.save()
	for i in cont.actuators:
		cont.activate(i)
		
def setSkyBoxPosition(cont):
	own = cont.owner
	scene = cont.owner.scene
	if scene.active_camera != None:
		if scene.active_camera.invalid == False:
			own.position = scene.active_camera.position
	
def getMirror(self, sen):
	obj = sen.hitObject
	
	n = Vector(sen.hitNormal)
	hp = Vector(sen.hitPosition)
	
	point = hp - self.worldPosition
	r = point.reflect(n)
	
	#bge.render.drawLine(obj.worldPosition, r, [0, 1, 0])
	return r
	
def runRays(cont):
	own = cont.owner
	if type(own) in gameobjects.terrainSensUnacceptedList:
		own.runRays()
		
def runtMapTimer(cont):
	var.lastTimePlayed = cont.owner['timer']
	
# ------------------------- db section -------------------------
def getUserScore(cont):
	usc = db.getUserScore(var.PCO.nick)
	if usc != False:
		var.userTotalScore = dict(usc)
	else:
		var.userTotalScore = False
	print("--------------------- UserScore ---------------------")
	print(var.userTotalScore)
	print("--------------------- UserScore ---------------------")
# --------------------------------------------------------------

# ------------------------- Scoring Section -------------------------
def getKills(cont):
	own = cont.owner
	try:
		if var.userTotalScore != False:
			own.text = str(var.userTotalScore['kill'])
	except:
		print("error ref : " + str(var.userTotalScore))
		checker.getInfo()
		bge.logic.endGame()
def getDeathCount(cont):
	own = cont.owner
	if var.userTotalScore != False:
		own.text = str(var.userTotalScore['death'])
def getKillAssistCount(cont):
	own = cont.owner
	if var.userTotalScore != False:
		own.text = str(var.userTotalScore['kill_assist'])
def getTeamkillsCount(cont):
	own = cont.owner
	if var.userTotalScore != False:
		own.text = str(var.userTotalScore['teamkill'])
def getSuicideCount(cont):
	own = cont.owner
	if var.userTotalScore != False:
		own.text = str(var.userTotalScore['suicide'])
def getTotalDamageCount(cont):
	own = cont.owner
	if var.userTotalScore != False:
		own.text = str(var.userTotalScore['damageCause'])
def damageRecieveCount(cont):
	own = cont.owner
	if var.userTotalScore != False:
		own.text = str(var.userTotalScore['damageRecieve'])
# -------------------------------------------------------------------
		
# ---------------- DB Section ----------------

# --------------------------------------------

# ---------------------------- GameNetWork Section ----------------------------
def toggleNetworVal(cont):
	own = cont.owner
	aktif = True
	for i in cont.sensors:
		if i.positive == False:
			aktif = False
	if aktif == True:
		networkInfo = own['networkInfo']
		if networkInfo in var.networkInfo:
			if var.networkInfo[networkInfo] == False:
				var.networkInfo[networkInfo] = True
			else:
				var.networkInfo[networkInfo] = False
				
def setupNetworkAbleObject(cont):
	own = cont.owner
	jenis = own['type']
	for i in gameobjects.networkInfoList:
		je = "<class 'gameobjects.{0}'>".format(jenis)
		if str(i) == je:
			this = i(own)
			print("applying object {0} as {1}".format(str(this), str(i)))
			for act in cont.actuators:
				cont.activate(act)
			break
# -----------------------------------------------------------------------------
	
# ------------------ This should be end of file ------------------ 