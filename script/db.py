# ---------------------------------------------------------------------------------------------------------------------------
'''
							DatabaseManagementScript by G. E. Oscar Toreh


This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
# ---------------------------------------------------------------------------------------------------------------------------
import var


def getValuesOfCollumn(kolom, table):
	c = var.db.cursor()
	q = "select {0} from {1}".format(kolom, table)
	c.execute(q)
	hasil = []
	for i in c:
		hasil.append(i[0])
	c.close()
	return hasil
	
def addValue(value, kolom, table):
	c = var.db.cursor()
	v = value
	if type(value) == str:
		v = "'{0}'".format(value)
	c.execute("insert into {0} ({1}) values ({2})".format(table, kolom, v))
	var.db.commit()
	c.close()
	
def addPlayerScore(nick):
	c = var.db.cursor()
	#c.execute("insert into scores values (nick='{0}', kill=0, death=0, kill_assist=0, suicide=0, scores=0, teamkill=0)".format(nick))
	#q = "insert into scores (nick, kill, death, kill_assist, suicide, scores, teamkill) values ({0}, 0, 0, 0, 0, 0, 0)".format(nick)
	#q = "insert into scores ('{0}', 0, 0, 0, 0, 0, 0) values (nick, kill, death, kill_assist, suicide, scores, teamkill)".format(nick)
	q = "insert into scores (nick, kill, death, kill_assist, suicide, scores, teamkill, highScores, damageCause, damageRecieve) values ('{0}', 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0)".format(nick)
	#print(q)
	c.execute(q)
	c.close()
	
def addMapPlayed(nick, mapName):
	c = var.db.cursor()
	#c.execute("insert into map_played values (nick='{0}', mapName='{1}', winCount=0, loseCount=0, timePlayed=0.0)".format(nick, mapName))
	q = "insert into map_played (nick, mapName, winCount, loseCount, timePlayed) values ('{0}', '{1}', 0, 0, 0.0)".format(nick, mapName)
	#q = "insert into map_played ('{0}', '{1}', 0, 0, 0.0) values (nick, mapName, winCount, loseCount, timePlayed)".format(nick, mapName)
	#print(q)
	c.execute(q)
	c.close()

def checkPalyerForScore():
	listOfScores = getValuesOfCollumn('nick', 'scores')
	listOfMapPlayed = getValuesOfCollumn('nick', 'map_played')
	
	kamus = var.globalDict
	map = kamus['map']
	namaMap = map.replace('.blend', '')
	
	for team in var.players:
		for p in team:
			if str(p) not in listOfScores:
				addPlayerScore(p)
			if str(p) not in listOfMapPlayed:
				addMapPlayed(p, namaMap)
				
	if var.PCO.nick not in listOfMapPlayed:
		addPlayerScore(var.PCO.nick)
	if var.PCO.nick not in listOfScores:
		addMapPlayed(var.PCO.nick, namaMap)
		
	var.db.commit()
				
def toDict(c, row):
	hasil = {}
	d = c.description
	for i in range(len(row)):
		hasil[d[i][0]] = row[i]
	return hasil
	
def getLastScore(nick):
	c = var.db.cursor()
	c.execute("select * from scores where nick='{0}'".format(nick))
	h = c.fetchall()
	hasil = toDict(c, h[0])
	return hasil
		
	
def getLastMapPlayedData(nick):
	c = var.db.cursor()
	c.execute("select * from map_played where nick='{0}'".format(nick))
	h = c.fetchall()
	hasil = toDict(c, h[0])
	return hasil
	
def updateScore(nick, total_kill, total_death, total_kill_assist, total_suicide, total_scores, total_teamkill, newHighScores, total_damage_cause, total_damage_recieve):
	c = var.db.cursor()
	c.execute("update scores set kill={0}, death={1}, kill_assist={2}, suicide={3}, scores={4}, teamkill={5}, highScores={6}, damageCause={8}, damageRecieve={9} where nick='{7}'".format(total_kill, total_death, total_kill_assist, total_suicide, total_scores, total_teamkill, newHighScores, nick, total_damage_cause, total_damage_recieve))
	c.close()
	
def updateMapPlayed(nick, mapName, winCount, loseCount, timePlayed):
	c = var.db.cursor()
	c.execute("update map_played set winCount={1}, loseCount={2}, timePlayed={3} where nick='{4}' and mapName='{0}'".format(mapName, winCount, loseCount, timePlayed, nick))
	c.close()
	
def getUserScore(nick):
	c = var.db.cursor()
	c.execute("select * from scores where nick='{0}'".format(nick))
	h = c.fetchall()
	if len(h) < 1:
		return False
	else:
		hasil = toDict(c, h[0])
		c.close()
		return hasil
