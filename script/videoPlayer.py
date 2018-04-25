'''
This videoPlayer script is made by G. E. Oscar Toreh since there's no other yet that make the same project from blender.

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
import bge

#video player script by G. E. Oscar Toreh
#version 21:36 31/01/2018

class videoPlayer:
	'obj = object of KX_GameObject'
	'a video player script made by G. E. Oscar Toreh'
	mat = None
	vFile = None
	obj = None
	daftar = []
	index = 0
	length = 0
	status = None
	repeat = False
	def __init__(self, obj):
		'obj = object of KX_GameObject'
		self.obj = None
		self.mat = None
		self.vFile = None
		self.daftar = []
		self.index = 0
		self.length = 0
		self.status = None
		self.repeat = False
		if type(obj) == bge.types.KX_GameObject:
			self.obj = obj
		else:
			print('wrong types of obj, expecting bge.types.KX_GameObject')
	def setMaterialName(self, mat):
		'''Set the material name'''
		self.mat = mat
	def play(self, vFile):
		'''Set name of video file. Won't work if video is not in current or child directory'''
		if vFile in self.daftar:
			self.index = self.daftar.index(vFile)
		else:
			if type(vFile) == str:
				self.daftar.append(vFile)
				self.length += 1
				self.index = self.daftar.index(vFile)
			else:
				print('wrong type of video path')
		#self.vFile = vFile
	def next(self):
		if self.length > 1:
			if self.index < self.length - 1:
				self.index += 1
				print('menaikan index video')
			else:
				self.index = 0
				print('memutar video pertama')
	def previous(self):
		if self.length > 1:
			if self.index > 0:
				self.index -= 1
			else:
				self.index = self.length - 1
			print('menurunkan index video')
	def addVideo(self, vFile):
		'''Add anotehr video to be play on next. This not implemented yet'''
		self.daftar.append(vFile)
		self.length += 1
	def removeAll(self):
		self.daftar = []
		self.index = 0
		self.length = 0
	def addRange(self, daftar):
		pa = len(self.daftar)
		pa2 = len(daftar)
		#self.daftar.insert(0, daftar)
		self.daftar.extend(daftar)
		self.length = pa + pa2
	def refresh(self):
		'''Play the video'''
		#cek = self.obj, self.vFile, self.mat
		#print('playing' + str(cek))
		
		if self.obj != None and self.length > 0 and self.mat != None:
			self.status = play(self.obj, self.daftar[self.index], self.mat)
			if self.status == 3:
				if self.repeat == 'all':
					self.next()
				else:
					if self.index < self.length - 1:
						self.next()
					else:
						self.status = 'finish'
	def refresh2(self):
		if self.obj != None and self.length > 0:
			self.status = simplePlayer(self.obj, self.daftar[self.index])
			#print(self.status)
			if self.status == 3:
				if self.repeat == 'all':
					self.next()
				else:
					if self.index < self.length - 1:
						self.next()
					else:
						self.status = 'finish'

def __doc__():
	print('video player script by G. E. Oscar Toreh')
	print('version 21:36 31/01/2018')
	
def info():
	"""Video player script by G. E. Oscar Toreh
Version 21:36 31/01/2018"""

def play(obj, fileLok, matName):
	"""Function to play a video

obj = object of plane
fileLok = path of video file
matName = name of material

returning status of video
"""
	if 'video' not in obj:
		video = None
		matID = bge.texture.materialID(obj, "MA" + matName)
		video = bge.texture.Texture(obj, matID)
		video.source = bge.texture.VideoFFmpeg(fileLok)
		if 'lv' not in obj:
			obj['lv'] = fileLok
		video.source.play()
		obj['video'] = video
		return video.source.status
	else:
		if obj['lv'] == fileLok:
			obj['video'].refresh(True)
			return obj['video'].source.status
		else:
			del obj['video']
			return 'reseting'
		
def simplePlayer(obj, fileLok):
	'''Function to play a video using the first meshes and first material of object

obj = object of plane
fileLok = path of video file

returning status of video
'''
	if 'video' not in obj:
		#dpMat = obj.meshes[0].materials[0]
		ada = False
		for dpMat in obj.meshes[0].materials:
			try:
				matID = bge.texture.materialID(obj, str(dpMat))
				ada = True
				print("materail found for video using purpose")
				break
			except:
				print("there's an error")
				ada = False
		if ada == False:
			return False
		video = bge.texture.Texture(obj, matID)
		video.source = bge.texture.VideoFFmpeg(fileLok)
		obj['lv'] = fileLok
		video.source.play()
		obj['video'] = video
		return video.source.status
	else:
		if obj['lv'] == fileLok:
			obj['video'].refresh(True)
			return obj['video'].source.status
		else:
			del obj['video']
			return 'reseting'
		
def playUsingProperty(cont):
	'''A video player function for logic brick user
property requirements:
- videoFile
- matName

videoFile is a name of video file of the current directory
matName is a name of material

create and overwriting value of property status as status of video
'''
	own = cont.owner
	if 'videoFile' in own and 'matName' in own:
		vf = bge.logic.expandPath("//" + own['videoFile'])
		status = play(own, vf, own['matName'])
		own['status'] = status
		
def simplePlayUsingProperty(cont):
	'''A video player function for logic brick user
property requirements:
- videoFile

videoFile is a name of video file of the current directory

create and overwriting value of property status as status of video
'''
	own = cont.owner
	if 'videoFile' in own:
		vf = bge.logic.expandPath("//" + own['videoFile'])
		status = simplePlyaer(own, vf)
		own['status'] = status
		

def contPlay(cont):
	"This function is used for debugging purpose"
	m = bge.logic.expandPath('//Intro.avi')
	dpMat = cont.owner.meshes[0].materials[0]
	cek = dpMat.material_index, dpMat.getMaterialIndex(), str(dpMat)
	#print("dp index mat asli ialah " + str(cek))
	#play(cont.owner, m, 'dummy')
	status = simplePlyaer(cont.owner, m)
	#print(status)
	
	
