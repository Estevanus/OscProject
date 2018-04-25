import triggerList
import bge
import var
import mainscript
import customScript.scoreBoard
#import scoreBoard

def initMap(map):
	tickets = var.mapKonfigurasi['tickets']
	var.tikets = tickets
	print("tickets >>>>>>>>>>>>> " + str(var.tikets))
	scoreBoard.init()
	#for i in var.ticketsObject:
	#	i.updateText()
	
def onTicketReachZero(team):
	if team == 1:
		var.lastWiningTeam = 2
	elif team == 2:
		var.lastWiningTeam = 1
	#cek = var.player, var.PCO.gameObject
	#print("status >>>>>>> {0} <<<<<<<<<<<".format(str(cek)))
	if var.player != None:
		var.player.scene.active_camera = var.player.scene.cameras['inGameMainCam']
		pa = var.player.scene.cameras['inGameMainCam'].parent
		if var.player.camPos != None:
			if var.player.camPos.invalid == False:
				if var.player.camPos.parent != None:
					if var.player.camPos.parent.invalid == False:
						pa.position = var.player.camPos.position
						pa.worldOrientation = var.player.camPos.worldOrientation
		var.player.useBy = None
		var.player.owner = None
		var.PCO.gameObject = None
		var.player = None
		
	for i in var.scene['bots']:
		if i.invalid == False:
			i.endObject()
	
	#bge.logic.endGame()
	'''
	'''
	for i in bge.logic.getSceneList():
		if i.name == 'inGame':
			#if 'peng back to main menu' not in i.objects:
			#	i.addObject('peng back to main menu')
			if 'playEndingMusic' not in i.objects:
				i.addObject('playEndingMusic')
			break
	pass

def main():#this funtion have to exist
	triggerList.onMapOpen.append(initMap)
	triggerList.onTicketReachZero.append(onTicketReachZero)
