'''
This spawner script is made by G. E. Oscar Toreh

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
import bge
import var
#from json import loads as muat
from mathutils import Vector as vektor, Euler as eul
import gameobjects
import ai
from weapons import setWeapons
import HUD
import checker
import random
import db

mouse_is_shown = True

spawnPoints = "spawnPoints.json"


def cekKamus(cont):
	own = cont.owner
	kamus = var.globalDict
	
	if 'cekKamus' not in own:
		own['cekKamus'] = "checked"
		print(kamus)
		

def mutate(own, tipe="vehicle"):
	old_object = own
	
	if tipe == 'vehicle':
		mutated_object = gameobjects.KX_VehicleObject(own)
		# After calling the constructor above, references to the old object
		# should not be used.
		assert(old_object is not mutated_object)
		assert(old_object.invalid)
		assert(mutated_object is own)
		
def subMunculkan(cont):
	own = cont.owner
	print('\nend of spawning object')
	print("..........................................")
	own['endAdding'] = None
	#for i in dir(HUD): print(i)
	HUD.addHUD()
	#print(scene.objects)
	#print(bge.logic.getSceneList())
	#cekKamus(cont)
	var.status = 'loadgameobject'
	#obj.addLookAt()
	own.endObject()

def deklarasi(cont):
	if cont.sensors['Always'].positive:
		scene = bge.logic.getCurrentScene()
		
		if 'bots' not in var.scene:
			var.scene['bots'] = []
		
		kamus = var.globalDict
		own = cont.owner
		
		'''
		#telah dipindahkan ke script openmap.py
		map = kamus['map'].split('.')
		map = map[0]
		
		thislok = bge.logic.expandPath('//')
		own['Nama Map'] = str(map)
		
		if 'mapKonfigurasi' not in own:
			mc = thislok + "maps\\" + own['Nama Map'] + "\\mapConfigurasi.json"
			own['mapKonfigurasi'] = True
			var.mapKonfigurasi = muat(open(mc).read())
			#var,mapKonfigurasi['jari2'] = var.mapKonfigurasi['dimensi']/2
			print(var.mapKonfigurasi)
			initializeMap()
			#posisi_unit_di_minimap = posisi_unit / jari2_map * jari2_minimap
		'''
		'''
		if 'getSpawnLocations' not in own:
			spl = thislok + "maps\\" + own['Nama Map'] + "\\spawnPoints.json"
			var.spawnLocations = muat(open(spl).read())
			own['getSpawnLocations'] = muat(open(spl).read())
			print(var.spawnLocations)
		'''
		
		#spawnCommanderController(cont, 1)
		#spawnCommanderController(cont, 2)
		scene.addObject('commanderControllerObject')
		spawnBotControllerObject(cont)
		for i in cont.actuators:
			cont.activate(i)
			
def setObjective(cont):
	own = cont.owner
	if 'type' in own:
		if own['type'] == "captureable":
			newone = gameobjects.KX_ControlPoints(cont.owner)
			var.controlPoints[newone.defBy].append(newone)
			cont.activate(cont.actuators['s2'])

def spawnCommanderController(cont, team=1):
	scene = bge.logic.getCurrentScene()
	added = scene.addObject('commanderControllerObject')
	added = gameobjects.KX_Commander(added)
	added.team = team
def spawnBotControllerObject(cont):
	print("assigning team for bots... with object " + cont.owner.name)
	botAssigning = var.mapKonfigurasi['botAssigning']
	scene = bge.logic.getCurrentScene()
	f = open(var.thisLok + 'cfg//bot names.txt')
	d = f.read()
	f.close()
	dl = d.split('\n')
	
	#randomize bot name
	#dl = random.choice(dl)
	
	nickYgTergunakan = []
	
	print("result from spliting bot names is " + str(dl))
	a = botAssigning[0]
	b = botAssigning[1]
	print("there's {0} bot/bots in team A".format(a))
	print("there's {0} bot/bots in team B".format(b))
	nameIndex = 0
	for i in range(botAssigning[0]):
		bot = scene.addObject('botControllerObject')
		bot = ai.KX_BotVehicleController(bot)
		var.scene['bots'].append(bot)
		bot.team = 1
		var.NPCList[1].append(bot)
		'''
		if nameIndex < len(dl) - 1:
			bot.nick = dl[nameIndex]
			nameIndex += 1
		'''
		nick = random.choice(dl)
		tlahAda = nickYgTergunakan.count(nick)
		if tlahAda == 0:
			bot.nick = nick
			nickYgTergunakan.append(nick)
		else:
			bot.nick = nick + str(tlahAda)
			nickYgTergunakan.append(nick)
		if bot.nick == None:
			nick = gameobjects.KX_ScoreObject(str(id(bot)))
			var.players[bot.team].append(nick)
			bot.score = nick
			nick.team = bot.team
		else:
			nick = gameobjects.KX_ScoreObject(bot.nick)
			var.players[bot.team].append(nick)
			bot.score = nick
			nick.team = bot.team
			
	for i in range(botAssigning[1]):
		bot = scene.addObject('botControllerObject')
		bot = ai.KX_BotVehicleController(bot)
		var.scene['bots'].append(bot)
		bot.team = 2
		var.NPCList[2].append(bot)
		'''
		if nameIndex < len(dl) - 1:
			bot.nick = dl[nameIndex]
			nameIndex += 1
		'''
		nick = random.choice(dl)
		tlahAda = nickYgTergunakan.count(nick)
		if tlahAda == 0:
			bot.nick = nick
			nickYgTergunakan.append(nick)
		else:
			bot.nick = nick + str(tlahAda)
			nickYgTergunakan.append(nick)
		if bot.nick == None:
			nick = gameobjects.KX_ScoreObject(str(id(bot)))
			var.players[bot.team].append(nick)
			bot.score = nick
			nick.team = bot.team
		else:
			nick = gameobjects.KX_ScoreObject(bot.nick)
			var.players[bot.team].append(nick)
			bot.score = nick
			nick.team = bot.team
			
	try:
		db.checkPalyerForScore()
	except:
		checker.getInfo()
		bge.logic.endGame()
	
def firstSpawnBot(cont):
	own = cont.owner
	if own['firstSpawn'] == True:
		#print("spawn disini tuh bot")
		for i in var.scene['bots']:
			i.isAllowToSpawn = True
			pass
		own['firstSpawn'] = False
	pass
	
def checkLocSpawner():
	spawns = []
	for i in var.spawnLocByTeam:
		for j in i:
			if i.invalid == False:
				spawns.append(j)
	return spawns
	
