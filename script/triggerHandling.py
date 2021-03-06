'''
This "should be a trigger handling but does not happen to be it" script is made by G. E. Oscar Toreh

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
import bge
import var
import spawner
import gameobjects

def updateSpawnLocChace():
	pass

def onSpawnLocAdded():
	#update spawnLoc or rebuild spawn loc list
	pass

def onSpawnLocDestroyed():
	#update spawnLoc or rebuild spawn loc list
	pass
	
def onSpawnLocChange():
	#update spawnLoc or rebuild spawn loc list
	#contoh user edited event sperti:
	#onSpawnLocChangeL.append(fucntionName)
	pass
	
def rebuildSpawnPointAllocator(spawnPointObject):
	#seksi ini terlihat membingungkan bukan padahal bisa saja langsung pakai spawnPointObject.updateUntrian(var.PCO)
	#ini dimaksudkan untuk mereset lagi data antrian spawn di objek spawn location yg lain karena tidak dipilih oleh
	#player
	indeks = 0
	for h in var.spawnLocByTeam:
		for i in h:
			'''
			if indeks == spawnPointObject.team:
				if i == spawnPointObject:
					spawnPointObject.updateAntrian(var.PCO)
					var.PCO.spawnLoc = spawnPointObject
				else:
					i.delAntrian(var.PCO)
			else:
				i.delAntrian(var.PCO)
			'''
			#i.antrian = []
			i.resetAntrian()
			i.delAntrian(var.PCO)
		indeks += 1
	spawnPointObject.updateAntrian(var.PCO)
	spawnPointObject.inUse = True
	#print("tipe data dari spawnPointObject ialah " + str(type(spawnPointObject)))
	var.PCO.spawnLoc = spawnPointObject
	#---------------------------------------------------------------------------------------------------------------
	
	#kemudian alokasikan botnya
	sps = var.spawnLocByTeam
	cps = var.controlPoints
	'''
	print(" --- ---")
	for h in cps:
		for i in h:
			print([i.name, i.defBy])
	print(" --- ---")
	'''
	#pisahkan team dari spawn point
	# cek dulu tim 1 pe misi
	relasi = [{}, {}, {}]#format relasi[team][jarak] = spawnLoc
	terdekat = [[], [], []]#format netral, tim 1, tim 2
	indeks = 0
	cpTerdekat = [[], [], []]#format = cpTerdekat[team] = [jarak, cp]
	for teamSp in sps:
		for sp in teamSp:
			sp.resetAntrian(False)
			for cpt in cps:
				for cp in cpt:
					#print([cp.defBy, sp.team])
					if cp.defBy != sp.team:
						jarak = cp.getDistanceTo(sp)
						relasi[indeks][jarak] = sp
						terdekat[indeks].append(jarak)
						if cpTerdekat[indeks] == []:
							cpTerdekat[indeks] = [jarak, cp]
						else:
							if jarak < cpTerdekat[indeks][0]:
								cpTerdekat[indeks] = [jarak, cp]
						#print(jarak)
						#print([relasi[indeks], terdekat[indeks]])
		indeks += 1
	
	indeks = 0
	#print(sps)
	#print(terdekat)
	for temp in terdekat:
		#print("before sortir = " + str(temp))
		temp.sort()
		#print("after sortir = " + str(temp))
		terdekat[indeks] = temp
		indeks += 1
	
	#print("relasinya = " + str(relasi))
	
	#mengalokasi penempatan bot=
	inGame = None
	for scene in bge.logic.getSceneList():
		if scene.name == "inGame":
			inGame = scene
	indeks = 0
	#print(terdekat)
	for teams in var.NPCList:
		for bot in teams:
			if inGame != None:
				isAdded = False
				'''
				'''
				for jr in terdekat[indeks]:
					if jr in relasi[indeks]:
						sp = relasi[indeks][jr]
						'''
						if relasi[indeks][jr].inUse == False:
							added = inGame.addObject(var.teamPCO[indeks])
							added = gameobjects.KX_VehicleObject(added)
							bot.gameObjects = added
							relasi[indeks][jr].inUse = True
							isAdded = True
							break
						'''
						if len(sp.antrian) == 0:
							sp.updateAntrian(bot)
							bot.spawnLoc = sp
							isAdded = True
							break
					else:
						print("{0} not in relasi[{1}] with data".format(str(jr), str(indeks)), str(relasi[indeks]))
						pass
				if isAdded == False:
					if var.spawnStrategy == "balance":
						tersedikit = None
						denganJumlah = None
						#relasiSP = {None:None}#format relasiSP = relasiSP[jml:spawnPoint]
						#jumlahAntrian = None#julah antrian dalam spawn point
						for sp in sps[indeks]:
							if tersedikit == None:
								tersedikit = sp
								denganJumlah = len(sp.antrian)
							else:
								jml = len(sp.antrian)
								if jml < denganJumlah:
									tersedikit = sp
									denganJumlah = jml
						if tersedikit != None and denganJumlah != None:
							sp.updateAntrian(bot)
							bot.spawnLoc = sp
							isAdded = True
		'''
		'''
		if indeks == 1:
			#cpTerdekat
			#var.botCommanderTeamA.cacheFokusMoveTo = cpTerdekat[indeks][1]
			var.botCommanderTeamA.fokusMoveTo(cpTerdekat[indeks][1])
		if indeks == 2:
			var.botCommanderTeamB.fokusMoveTo(cpTerdekat[indeks][1])
		indeks += 1

def onMapOpen(mapName, mapPath, konfigurasi):
	pass
	
def onControlPointHasTaken(cont):
	#updateStrategy
	botCommanderTeamA.updateStrategy()
	botCommanderTeamB.updateStrategy()
	pass
	
def onObjectiveHasDestroyed(cont):
	botCommanderTeamA.updateStrategy()
	botCommanderTeamB.updateStrategy()
	
def onWeaponShot(player, weapon):
	#this should be occur when player/bot is shooting
	#good for checking shot from where and etc
	pass
	
def onPlayerChooseSpawn(spawnPointObject):
	if var.isFirstSpawn == True:
		#spawnPointObject.updateUntrian(var.PCO)
		rebuildSpawnPointAllocator(spawnPointObject)
		pass
	pass
	
def onPlayerJoin(player):
	#updatePlyerList()
	pass

def onUserSpawn(cont):
	#this function is called once when the player spawn for the first time in level
	if var.isFirstSpawn == True:
		nick = gameobjects.KX_ScoreObject(var.PCO.nick)
		var.players[var.PCO.team].append(nick)
		var.PCO.score = nick
		nick.team = var.PCO.team
		spawner.firstSpawnBot(cont)
		for scene in bge.logic.getSceneList():
			if scene.name == 'inGame':
				scene.addObject('inGameTimeGenerator')
		var.isFirstSpawn = False
	#print("player ialah " + str(var.PCO))
	#var.PCO.spawnLoc.delAntrian(var.PCO)
	
def onPlayerSpawn(player, spawnLoc):
	#sp.delAntrian
	spawnLoc.delAntrian(player)
	
	
def onPlayerKilled():
	#this should have player, killBy, killBy.weapon, vehicle
	#if vehicle exist
	pass