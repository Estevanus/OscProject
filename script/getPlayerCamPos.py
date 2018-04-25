import bge

scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()

alw = cont.sensors['Always']

if alw.positive:
	own = cont.owner

	obj = scene.objects

	if 'playerCamPos' in obj:
		#print('ok')
		own.position = obj['playerCamPos'].position
		own.worldOrientation = obj['playerCamPos'].worldOrientation
		
		#for i in cont.actuators:
		#	cont.activate(i)