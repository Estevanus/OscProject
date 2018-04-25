import bge
import var
import gameobjects

def loadMap(cont):
	own = cont.owner
	loadedMap = "00"
	mapDir = var.thisLok + "//storymaps//" + loadedMap
	mapFile = mapDir + "//mapFile.blend"
	
	
	loadedMap = bge.logic.LibLoad(mapFile, 'Scene', async=True, load_actions=True)
	
def spawnPlayer(cont):
	own = cont.owner
	p = own['player']
	scene = own.scene
	bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
	added = scene.addObject("soldier", own)
	soldier = gameobjects.KX_SoldierObject(added)
	soldier.owner = var.PCO
	var.PCO.gameObject = soldier
	var.player = soldier
	var.player.setCamPos()
	#print(var.PCO)
	
	
	