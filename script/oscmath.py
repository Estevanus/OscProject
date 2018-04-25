# ---------------------------------------------------------------------------------------------------------------------------
'''
								Custom Physics by Osccar

Since I'm bad at math and nobody like to help me with math so I just make my custom math.
And with that statement I declare that criticsm will be ignore and only advise is accepted.


This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
# ---------------------------------------------------------------------------------------------------------------------------
import bge
from math import *
from mathutils import *

def unhypot(h, x):
	y = sqrt(h**2-x**2)
	return y

def getMomentum(velocity, mass):
	return mass * velocity
	
def trajectoryFall(velocity, dari, intercept, g):
	pass
	
def linearPrediction2D(pv, tv3, p2t):
	#pv ialah projectile velocity
	#tv3 = target worldLinearVelocity
	#p2t = projectile.getDistanceTo(target)
	b = tv3.x, tv3.y
	A = hypot(tv3.x, tv3.y)
	tv = A
	B = pv
	pv3 = Vector((0,1,0))
	pv3.y = tv3.y
	pv3.x = -unhypot(pv, tv3.y)
	C = tv3.x + pv3.x
	
	t = p2t / C
	return pv3, t
	
def getVertexDistance(v1, v2):
	v = v1.getXYZ() - v2.getXYZ()
	return v.length
	
def getPolygonCenter(polygonProxy, obj):
	mi = polygonProxy.material_id
	mesh = polygonProxy.getMesh()
	v1 = mesh.getVertex(mi, polygonProxy.v1)
	v2 = mesh.getVertex(mi, polygonProxy.v2)
	v3 = mesh.getVertex(mi, polygonProxy.v3)
	v4 = mesh.getVertex(mi, polygonProxy.v4)
	
	c1 = (v1.getXYZ() - v3.getXYZ()) / 2
	c2 = v1.getXYZ() - c1
	c3 = c2 + obj.position
	cek = c3, v1.getXYZ(), v3.getXYZ()
	#print(cek)
	return c3
	
def getDistance(pst, dari):
	'pst ialah vektor awal'
	'dari ialah vektor yang akan diukur jaraknya terhadap vektro pst'
	v = dari - dst
	return v.length
	
	
def getImpactData(obj, impactTo):
	#obj = object that contain last velocity and last rotation
	terdekat = None
	jt = None
	jarak = None
	me = impactTo.meshes[0]
	polPos = None
	for i in range(me.numPolygons):
		pol = m.getPolygon(i)
		polPos = getPolygonCenter(pol, impactTo)
		jarak = getDistance(obj.position, polPos)
		if terdekat == None:
			terdekat = pol
			jt = jarak
		else:
			if jarak < jt:
				terdekat = pol
				jt = jarak
				
	return pol, polPos
	
def gatPolygonFacing_ko(pol, obj, incoming):
	m = pol.getMesh()
	v1 = m.getVertex(0, pol.v1)
	v2 = m.getVertex(0, pol.v2)
	v3 = m.getVertex(0, pol.v3)
	v4 = m.getVertex(0, pol.v4)
	
	v1l = v1.getXYZ()
	v2l = v2.getXYZ()
	v3l = v3.getXYZ()
	v4l = v4.getXYZ()
	
	oRot = obj.worldOrientation
	#v1p = v1.getXYZ() * oRot
	#v2p = v2.getXYZ() * oRot
	#v3p = v3.getXYZ() * oRot
	#v4p = v4.getXYZ() * oRot
	v1p = oRot * v1.getXYZ()
	v2p = oRot * v2.getXYZ()
	v3p = oRot * v3.getXYZ()
	v4p = oRot * v4.getXYZ()
	
	v1n = v1.normal * oRot
	v2n = v2.normal * oRot
	v3n = v3.normal * oRot
	v4n = v4.normal * oRot
	
	v1nm = v1p.normalized()
	v2nm = v2p.normalized()
	v3nm = v3p.normalized()
	v4nm = v4p.normalized()
	
	#x = v1nm - v2nm
	#y = v2nm - v3nm
	#z = Vector((0, 0, 0))
	
	x = v1nm
	y = v2nm
	#z = Vector((hypot(x.x, x.y), x.z, 0.0)) * Matrix.Rotation(radians(90), 3, 'Z')
	z = Vector((0.0, hypot(x.x, x.y), x.z)) * Matrix.Rotation(radians(90), 3, 'X')
	z2 = Vector((hypot(y.x, y.y), 0.0, x.z)) * Matrix.Rotation(radians(90), 3, 'Y')
	z3 = Vector((0.0, 0.0, y.y))
	z4 = Vector((0.0, 0.0, x.x * y.y))
	
	h1 = incoming.reflect(v1nm)
	h2 = incoming.reflect(v2nm)
	#hasil = v1nm.reflect(incoming)
	#hasil = v1nm
	#hasil = v1nm.project(incoming)
	
	sv = Vector((x.x, y.y, 0.0)).normalized()
	sm = Matrix([
	[sv.x, -sv.y, 0.0],
	[sv.y, sv.z, 0.0],
	[0.0, 0.0, 1.0]
	])
	
	
	normal = geometry.normal([v1p, v2p, v3p, v4p])
	facing = Vector((0.0, 0.0, 0.0))
	
	'''
	rx = Matrix([
	[1, 0, 0],
	[0, y, z],
	])
	'''
	
	#if v1nm.y
	#facing.z = 
	
	#cek = v1p, v2p
	#print("pos : " + str(cek))
	#cek = v2nm
	#print(cek)
	
	#return v1n, v2n, v1p, v2p
	#return v1n, v2n
	#return normal
	#return h1, h2
	return normal, h2
	#return x, y
	
def getPolyGoneHeading(pol, obj):
	m = pol.getMesh()
	v1 = m.getVertex(0, pol.v1)
	v2 = m.getVertex(0, pol.v2)
	v3 = m.getVertex(0, pol.v3)
	v4 = m.getVertex(0, pol.v4)
	
	oRot = obj.worldOrientation
	v1p = oRot * v1.getXYZ()
	v2p = oRot * v2.getXYZ()
	v3p = oRot * v3.getXYZ()
	v4p = oRot * v4.getXYZ()
	
	normal = geometry.normal([v1p, v2p, v3p, v4p])
	return normal
	
def mirror_point_plane(point, pol, obj):
	heading = getPolyGoneHeading(pol, obj)
	
	r = -point.reflect(heading)
	return r
	
def root(value, size):
	return value ** (1/size)
	
def airResistance(watt, airDensity, drag, frontalArea):
	print(" -------------------------- ")
	da = (2*watt) / (airDensity * drag * frontalArea)
	v = abs(da ** (1/3))
	print(2*watt)
	print(airDensity * drag * frontalArea)
	print((2*watt) / (airDensity * drag * frontalArea))
	print(v)
	print(" -------------------------- ")
	return v
	
def getMaxSpeed(watt, airDensity, drag, frontalArea):
	print(" -------------------------- ")
	da = (2*watt) / (airDensity * drag * frontalArea)
	v = abs(da ** (1/3))
	print(2*watt)
	print(airDensity * drag * frontalArea)
	print((2*watt) / (airDensity * drag * frontalArea))
	print(v)
	print(" -------------------------- ")
	return v
#