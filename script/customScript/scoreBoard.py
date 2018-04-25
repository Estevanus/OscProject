import triggerList
#from mainscript import addScore
import mainscript

SCORE = 2
SUICIDE = -2
ASSIST = 1
TEAMKILL = -4

def init():
	triggerList.onPlayerKilled.append(onPlayerKill)
	#print(dir(mainscript))

'''
'''
def onPlayerKill(victim, killer, weapon):
	#cek = victim, killer, weapon , dir(victim)
	#print('onPlayerKill info ' + str(cek))
	if killer!= None:
		if hasattr(killer, 'team'):
			if killer.team == victim.team:
				mainscript.addScore(killer, TEAMKILL)
			else:
				mainscript.addScore(killer, SCORE)
		else:
			mainscript.addScore(victim, SUICIDE)
	else:
		mainscript.addScore(victim, SUICIDE)