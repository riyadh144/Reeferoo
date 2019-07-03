import json
import time
import datetime
import spidev
import threading
weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=50000
spi.mode=3



r1r=0 # Real Status of reefers
r2r=0
r3r=0
r4r=0
rr = [r1r, r2r, r3r, r4r]

r5r=False # Automatic Control of switches I don't think this matters for the server so it might be deleted
#TODO: Replace with SPI Commands
def turnOn(x):
	ra=[0,1,2,3]
	ra.remove(x)
	spi.writebytes([176+x])
def turnOff(x):
	print(str(x)+"is Off")
	spi.writebytes([128+x])
def getVoltages():

	spi.writebytes([0b01000000])
	time.sleep(.05)
	phaseAVoltage = spi.readbytes(4)[1:4]
	phaseAVoltage = int.from_bytes(phaseAVoltage, byteorder='big', signed=True)

	spi.writebytes([0b01010000])
	time.sleep(.05)
	phaseBVoltage = spi.readbytes(4)[1:4]
	phaseBVoltage = int.from_bytes(phaseBVoltage, byteorder='big', signed=True)
	spi.writebytes([0b01100000])
	time.sleep(.05)
	phaseCVoltage = spi.readbytes(4)[1:4]
	phaseCVoltage = int.from_bytes(phaseCVoltage, byteorder='big', signed=True)

	return [phaseAVoltage,phaseBVoltage,phaseCVoltage]
def getCurrents():
	spi.writebytes([0b01000001])
	time.sleep(.05)
	phaseACurrent = spi.readbytes(4)[1:4]
	phaseACurrent = int.from_bytes(phaseACurrent, byteorder='big', signed=True)

	spi.writebytes([0b01010001])
	time.sleep(.05)
	phaseBCurrent = spi.readbytes(4)[1:4]
	phaseBCurrent = int.from_bytes(phaseBCurrent, byteorder='big', signed=True)

	spi.writebytes([0b01100001])
	time.sleep(.05)
	phaseCCurrent = spi.readbytes(4)[1:4]
	phaseCCurrent = int.from_bytes(phaseCCurrent, byteorder='big', signed=True)

	return [phaseACurrent,phaseBCurrent,phaseCCurrent]

def run():
	lock = "false"
	data=""

	while (lock):
		with open("/usr/lib/cgi-bin/reefer/ReeferStatus.ss") as json_file:
			data = json.load(json_file)
		lock = bool(data["lock"])
		time.sleep(.1)

	data['lock'] = False
	today = weekDays[datetime.datetime.today().weekday()]
	current_time = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute
	sod = data[today]
	with open("/usr/lib/cgi-bin/reefer/ReeferStatus.ss", "w") as jsonFile:
		json.dump(data, jsonFile)
	r1s = data['Reefer1']
	r2s = data['Reefer2']
	r3s = data['Reefer3']
	r4s = data['Reefer4']
	rs=[r1s,r2s,r3s,r4s]
	r5s = data['Automatic']
	if "1" in sod and r5s == 1:
		on = 0
		for interval in sod["1"]:
			timeInterval = [0, 0]  # Time inteval 0 is the start 1 is the end
			i = 0

			for timeV in interval:
				t = datetime.datetime.strptime(timeV, "%H:%M")
				timeInterval[i] = t.hour * 60 + t.minute
				i = i + 1
			# print(timeInterval)
			if (timeInterval[0] < current_time and timeInterval[1] > current_time):
				r1s = 1
				r2s = 0
				r3s = 0
				r4s = 0
				break
			else:
				r1s=0




	if "2" in sod and r5s == 1:
		on = 0
		for interval in sod["2"]:

			timeInterval = [0, 0]  # Time inteval 0 is the start 1 is the end
			i = 0
			for timeV in interval:
				t = datetime.datetime.strptime(timeV, "%H:%M")
				timeInterval[i] = t.hour * 60 + t.minute
				i = i + 1
			# print(timeInterval)
			if (timeInterval[0] < current_time and timeInterval[1] > current_time):
				r1s = 0
				r2s = 1
				r3s = 0
				r4s = 0
				break
			else:
				r2s=0
	if "3" in sod and r5s == 1:
		for interval in sod["3"]:

			timeInterval = [0, 0]  # Time inteval 0 is the start 1 is the end
			i = 0
			for timeV in interval:
				t = datetime.datetime.strptime(timeV, "%H:%M")
				timeInterval[i] = t.hour * 60 + t.minute
				i = i + 1
			# print(timeInterval)
			if (timeInterval[0] < current_time and timeInterval[1] > current_time):
				r1s = 0
				r2s = 0
				r3s = 1
				r4s = 0
				break

			else:
				r3s=0
	if "4" in sod and r5s == 1:
		for interval in sod["4"]:

			timeInterval = [0, 0]  # Time inteval 0 is the start 1 is the end
			i = 0
			for timeV in interval:
				t = datetime.datetime.strptime(timeV, "%H:%M")
				timeInterval[i] = t.hour * 60 + t.minute
				print(timeInterval[i])

				i = i + 1

   # print(timeInterval)
			if (timeInterval[0] < current_time and timeInterval[1] > current_time):
				r1s = 0
				r2s = 0
				r3s = 0
				r4s = 1
				break
			else:
				r4s=0
				print("4"+str(interval))
		print("Current Time")
		print(str(current_time)+"\n")



	rs=[r1s,r2s,r3s,r4s]

	for i in range(0,4): # go through the list and compare if they are different then change status, I am sure there is a cleaner way to implement this but this is what you get

		print(str(rs[i])+" rr "+str(rr[i]))
		if rs[i] != rr[i] and rs[i] == 1:
			turnOn(i)
			print("On"+str(i))
			break
		else:
			turnOff(i)
		rr[i] = rs[i]

	voltage= getVoltages()
	current = getCurrents()
	data['VoltageA'] = voltage[0]
	data['VoltageB'] = voltage[1]
	data['VoltageC'] = voltage[2]
	data['CurrentA'] = current[0]
	data['CurrentB'] = current[1]
	data['CurrentC'] = current[2]
	data['Reefer1'] = r1s
	data['Reefer2'] = r2s
	data['Reefer3'] = r3s
	data['Reefer4'] = r4s
	data['lock'] = False

	with open("/usr/lib/cgi-bin/reefer/ReeferStatus.ss", "w") as jsonFile:
		json.dump(data, jsonFile)


def run_check():
	threading.Timer(5.0, run_check).start()
	run()

run_check()