'''
This picker script is made by G. E. Oscar Toreh

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
import bge
import var

class simpleObject:
	invalid = True
	
pemuncul = simpleObject()
class shower(bge.types.KX_GameObject):
	showingObject = simpleObject()
	kontestan = []
	indeks = 0
	def __init__(self, old_owner):
		kontestan = []
		root = bge.logic.expandPath("//")
		lok = root + 'objects\\vehicles'
		kontestan = bge.logic.getBlendFileList(lok)
		if len(kontestan) > 0:
			hasil = kontestan[0].replace(".blend", '')
			self.showingObject = self.scene.addObject(hasil, self)
			#self.showingObject.setVisible(True, True)
			#self.showingObject.position = self.position
			var.spawnAs = hasil
			print('hasil >>>>>>>>>>> ' + str(self.showingObject))
			print(type(self.showingObject))
		cek = root, lok, kontestan
		print(cek)
		self['kontestan'] = str(kontestan)
		self.addDebugProperty('kontestan')
		self.kontestan = kontestan
		
	def next(self):
		pa = len(self.kontestan)
		if pa > 1:
			self.indeks += 1
			if self.indeks > pa - 1:
				self.indeks = 0
			self.showingObject.endObject()
			hasil = self.kontestan[self.indeks].replace(".blend", '')
			self.showingObject = self.scene.addObject(hasil, self)
			var.spawnAs = hasil

def setup(cont):
	global pemuncul
	pemuncul = shower(cont.owner)
	
def lanjut(cont):
	aktif = True
	for i in cont.sensors:
		if i.positive == False:
			aktif = False
	if aktif == True:
		global pemuncul
		if pemuncul.invalid == False:
			pemuncul.next()