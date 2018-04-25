import bge


def main(cont):
	own = cont.owner
	scene = bge.logic.getCurrentScene()
	if "for_add" in own:
		scene.addObject(own["for_add"] ,own)