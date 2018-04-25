'''
This console script is made by G. E. Oscar Toreh

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
import bge
import var

def endHUD():
	for i in bge.logic.getSceneList():
		if i.name == 'HUD':
			i.end()
			break

def showMouse():
	bge.logic.mouse.visible = True
	
def hideMouse():
	bge.logic.mouse.visible = False
	
def getMainCamPos():
	cam = bge.logic.getCurrentScene().active_camera
	print(cam.position)
	
def getVarSceneInfo():
	print(var.scene)
	
def getViewO():
	print(var.objectsInView)
	
def bullyMe():
	var.botCommanderTeamA.cheatAttackPlayer()
	var.botCommanderTeamB.cheatAttackPlayer()
	print("cheat attack player is activated")
	
def tempStunAll():
	pass
	
def bukaMenuMap():
	for i in bge.logic.getSceneList():
		if i.name == "inGame":
			i.replace("vehiclePicker")

def execute(cont):
	own = cont.owner
	kamus = var.globalDict
	exec(own["Text"])
	own['Text'] = ""