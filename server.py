import json
import time

r1r=False # Real Status of reefers
r2r=False
r3r=False
r4r=False
rr = [r1r, r2r, r3r, r4r]

r5r=False # Automatic Control of switches I don't think this matters for the server so it might be deleted
#TODO: Replace with SPI Commands
def turnOn(x):
	ra=[0,1,2,3]
	ra.remove(x)
	print(ra)
	for i in ra:
		print(str(i)+"is Off")
	print(str(x)+"is On")
def turnOff(x):
	print(str(x)+"is Off")
def getVoltages():
	VA=0
	VB=0
	VC=0
	return [VA,VB,VC]
def getCurrents():
	IA=0
	IB=0
	IC=0
	return [IA,IB,IC]

def run():
	lock = "false"
	data=""

	while (lock):
		with open("ReeferStatus.ss") as json_file:
			data = json.load(json_file)
		lock = bool(data["lock"])
		time.sleep(.1)

	data['lock'] = False
	with open("ReeferStatus.ss", "w") as jsonFile:
		json.dump(data, jsonFile)
	r1s = data['Reefer1']
	r2s = data['Reefer2']
	r3s = data['Reefer3']
	r4s = data['Reefer4']
	rs=[r1s,r2s,r3s,r4s]
	r5s = data['Automatic']

	for i in range(0,4): # go through the list and compare if they are different then change status, I am sure there is a cleaner way to implement this but this is what you get
		if rs[i] != rr[i] and rs[i]==False:
			turnOff(i)
		elif rs[i] != rr[i] and rs[i]==True:
			turnOn(i)
		rr[i]=rs[i]

	voltage= getVoltages()
	current = getCurrents()
	data['VoltageA'] = voltage[0]
	data['VoltageB'] = voltage[1]
	data['VoltageC'] = voltage[2]
	data['CurrentA'] = current[0]
	data['CurrentB'] = current[1]
	data['CurrentC'] = current[2]

	data['lock'] = False

	with open("ReeferStatus.ss", "w") as jsonFile:
		json.dump(data, jsonFile)
