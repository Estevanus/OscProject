

import bge
scene = bge.logic.getCurrentScene()


root = bge.logic.expandPath("//")

maps = bge.logic.getBlendFileList("//maps")

cont = bge.logic.getCurrentController()
own = cont.owner

own['maps'] = str(maps)
#own['added'] = []

for i in maps:
	added = scene.addObject('mapPlane', own)
	own.position.y -= 1.5
	added.children[0].text = i.replace('.blend', '')

