'''
This openMap script is made by G. E. Oscar Toreh

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
import bge
import var
import triggerHandling
from daftarScene import getScene
from json import loads as muat
import triggerList

cont = bge.logic.getCurrentController()
kamus = var.globalDict
root = bge.logic.expandPath("//")
own = cont.owner
scene = bge.logic.getCurrentScene()

map = kamus['map']
namaMao = kamus['map'].split('.')
namaMao = namaMao[0]
namaMap = map.replace('.blend', '')

thislok = bge.logic.expandPath('//')
own['Nama Map'] = str(namaMap)

#reset player list
var.players = [[], [], []]
		
def initializeMap():
	con = var.mapKonfigurasi
	scene = bge.logic.getCurrentScene()
	print("initializing map configuration...")
	if "gravity" in con:
		scene.gravity = [0, 0, con['gravity']]
	pass
	
if 'tim' not in var.scene:
	var.scene['tim'] = 1

if 'mapKonfigurasi' not in own:
	mc = thislok + "maps\\" + own['Nama Map'] + "\\mapConfigurasi.json"
	own['mapKonfigurasi'] = True
	var.mapKonfigurasi = muat(open(mc).read())
	#var,mapKonfigurasi['jari2'] = var.mapKonfigurasi['dimensi']/2
	print(var.mapKonfigurasi)
	initializeMap()
	#posisi_unit_di_minimap = posisi_unit / jari2_map * jari2_minimap

def removeLoading(status):
	global scene
	loading = getScene('loading')
	loading.end()
	print('successfull removing loading scene')
	print("successfull loaded file at " + map)
	print('disabling map loader at openMap.py')
	added = scene.addObject("map_initializer", own)
	print('adding '+str(added))
	for i in triggerList.onMapOpen:
		i(map)
	#status.libraryName = "test_neh"
	#nama libnya tak bisa di bypas :(
	
aktif = True
for i in cont.sensors:
	if i.positive == 0:
		aktif = False
		
if aktif == True:
	lokMap = root + '//maps//' + map
	triggerHandling.onMapOpen(map, root + '//maps', var.mapKonfigurasi)
	#bge.logic.LibLoad(root + '//maps//' + map, 'Scene', async=True).onFinish = removeLoading
	loadedMap = bge.logic.LibLoad(lokMap, 'Scene', async=True, load_actions=True)
	#loadedPlayer = bge.logic.LibLoad(root + '//objects//vehicle//' + 'VC00.blend', 'Scene', async=True)
	#scene = bge.logic.getCurrentScene()
	
	loadedMap.onFinish = removeLoading



