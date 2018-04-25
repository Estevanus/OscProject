from bge import logic


def getScene(nama):
	daftarScene = logic.getSceneList()
	sLen = len(daftarScene)
	
	i = 0
	while i < sLen:
		if daftarScene[i].name == nama:
			return daftarScene[i]
		
		i += 1
		
	return False