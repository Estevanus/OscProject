import bge
import var
kamus = var.globalDict

cont = bge.logic.getCurrentController()
own = cont.owner


ada = True
for i in cont.sensors:
	if not i.positive:
		ada = False

if ada == True:
	kamus['map'] = own.children[0].text + ".blend"
	cont.activate(cont.actuators['Scene'])
	cont.activate(cont.actuators['addLoading'])