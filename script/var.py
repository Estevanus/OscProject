'''
This var script is made by G. E. Oscar Toreh

Even though this just a bunch of variables, but this script is playing one of vital role in the game 

Feel free to use this script
'''
import bge
import aud
import sqlite3

ngecek = False

#status  sperti loadgameobject, dll
status = None

#get last added gameobject ID to put enableler lookAt script
lastAddedGameObjectId = None

class kamusyah(dict):
	pass
globalDict = kamusyah({})
scene = {}

#audiodevice
audDevice = aud.device()

#cfg section
thisLok = bge.logic.expandPath('//')
cfgLok = thisLok + "//cfg//control.json"
nickLok = thisLok + "//cfg//id.txt"
textureQuality = "low"

#Game Music
gFact = aud.Factory(thisLok + "//audio//Game Music.mp3")
gMusicBuff = aud.Factory.buffer(gFact)
gMusic = None

wigem = aud.Factory.buffer(aud.Factory(thisLok + 'audio//win.mp3'))
ligem = aud.Factory.buffer(aud.Factory(thisLok + 'audio//lose.mp3'))
igem_buffered = None


#variable dinamis nya map
#spawnLocations = {}
controlPoints = [[], [], []]#format [daftarNeutralCP, daftarTeam1CP, daftarTeam2CP]
#spawnLocations = []
spawnLocByTeam = [[], [], []]#ini perlu diupdate setiap kali ada spawn loc baru ataupun spawn loc yg menghilang bahkan juga ketika atribut team dari spawn loc diganti. Format 0 untuk netral, 1 for tim 1, 2 for tim 2
spawnStrategy = "balance"#rencananya juga kalo misalnya mo beking agresif mungkin mo pake rupa prioritas spawn 1 atau 2 spawn terdekat objektif yg jadi prioritas utama for bot mo spawn akang
isMapOpened = False
teamAPCO = 'FighterAlo'
teamBPCO = 'FighterAlo'
teamPCO = [None, teamAPCO, teamBPCO]
botPCO = [teamAPCO, teamBPCO]
destroyableObjective = [[], [], []]#0 untuk kedua tim lawan cepat, 1 untuk tim 1, 2 untuk tim 2
botCommanderTeamA = None
botCommanderTeamB = None
NPCList = [[], [], []]#0 for netral, 1 for team 1, 2 for team 2
players = [[], [], []]#0 for netral, 1 for team 1, 2 for team 2
botWaitingTime = 180#in logic ticks
#botAntrianForSpawn = []#may not be usable anymore
#antrialForSpawn = {}#format spawnpoint = []
totalTicks = 0
totalTime = 0.0


disableAllIngameControl = False#usage for when opening map or spawn map
alwaysUseNewlyTakenItem = True

#human player section var
player = None
isFirstSpawn = True
lookAtObject = None
penandaPlayer = "playerObject"
PCO = None
objectsInView = []#this might be remove later
userTotalScore = {}#this gonna use on personal scoreboard

#prefering vehicle
spawnAs = "FighterAlo"

isSpawnMenuOpened = False


#defaul maps settings
map = None
defaultMasaUdara = 1.293
defaultGravity = -9.8

#map setting
mapKonfigurasi = {}
masaUdara = 1.293
gravity = -9.8
navigator = None
waymesh = None
waypoints = []
tikets = ['inf', 10, 10]
ticketsObject = []
gotoScoreBoard = False
lastWiningTeam = None
lastTimePlayed = 0.0

#globalSettings
soldierLookSensitivity = 1.0
airPlaneMouseSensitivity = 1.0
#isModded = False


#Event section
mOverEvemt = 0

#db
#db = sqlite3.connect('Tambahan/db/air_world_fighter.oscdb')
db = sqlite3.connect(thisLok + '/Tambahan//db//air_world_fighter.oscdb')

#objects network info
networkInfo = {}
