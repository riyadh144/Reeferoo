#!/usr/bin/env python3
import cgi
import cgitb
import json
import time
import ast
import datetime

weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
today=weekDays[datetime.datetime.today().weekday()]
current_time =  datetime.datetime.now().hour*60 +datetime.datetime.now().minute
#print(current_time)
count = -1
r1s = ""
r2s = ""
r3s = ""
r4s = ""
data = ""
cgitb.enable()
lock = "false"
data=""
while (lock):
	with open("ReeferStatus.ss") as json_file:
		data = json.load(json_file)
	lock = bool(data["lock"])
	time.sleep(.1)

data['lock'] = False;
with open("ReeferStatus.ss", "w") as jsonFile:
	json.dump(data, jsonFile)
r1s = data['Reefer1']
r2s = data['Reefer2']
r3s = data['Reefer3']
r4s = data['Reefer4']
r5s = data['Automatic']
mon = data['Monday']
tue = data['Tuesday']
wed = data['Wednesday']
thu = data['Thursday']
fri = data['Friday']
sat = data['Saturday']
sun = data['Sunday']
sod= data[today]#schedule of the day
#mmm="ds"
form = cgi.FieldStorage()
#cgit.enable(display0, logdir=OUTDIR)
if "reefer1" in form:
	r1s = not bool(r1s)
	r2s = 0
	r3s = 0
	r4s = 0
elif "reefer2" in form:
	r2s = not bool(r2s)
	r1s = 0
	r3s = 0
	r4s = 0

elif "reefer3" in form:
	r3s = not bool(r3s)
	r1s = 0
	r2s = 0
	r4s = 0


elif "reefer4" in form:
	r4s = not bool(r4s)
	r1s = 0
	r2s = 0
	r3s = 0

elif "Automatic" in form:
	r5s = not bool(r5s)


elif "schedule" in form:
#elif True:
	data['Monday']      =ast.literal_eval((form.getvalue("Monday")))
	data['Tuesday']     =ast.literal_eval((form.getvalue("Tuesday")))
	data['Wednesday']   =ast.literal_eval((form.getvalue("Wednesday")))
	data['Thursday']    =ast.literal_eval((form.getvalue("Thursday")))
	data['Friday']      =ast.literal_eval((form.getvalue("Friday")))
	data['Saturday']    =ast.literal_eval((form.getvalue("Saturday")))
	data['Sunday']      =ast.literal_eval((form.getvalue("Sunday")))
if "1" in sod:
	on=0
	for interval in sod["1"]:
		timeInterval=[0,0]#Time inteval 0 is the start 1 is the end
		i=0

		for time in interval:
			t= datetime.datetime.strptime(time, "%H:%M")
			timeInterval[i]=t.hour*60+t.minute
			i=i+1
			#print(timeInterval)
		if(timeInterval[0]<current_time and timeInterval[1]>current_time):
			r1s = 1
			r2s = 0
			r3s = 0
			r4s = 0
			on=1
	if(on):
		r1s=1
	else:
		r1s=0

if "2" in sod:
	on=0
	for interval in sod["2"]:
		timeInterval=[0,0]#Time inteval 0 is the start 1 is the end
		i=0
		for time in interval:
			t= datetime.datetime.strptime(time, "%H:%M")
			timeInterval[i]=t.hour*60+t.minute
			i=i+1
			#print(timeInterval)
		if(timeInterval[0]<current_time and timeInterval[1]>current_time):
			r1s = 0
			r2s = 1
			r3s = 0
			r4s = 0
			on = 1
	if(on):
		r2s=1
	else:
		r2s=0

if "3" in sod:
	for interval in sod["3"]:
		timeInterval=[0,0]#Time inteval 0 is the start 1 is the end
		i=0
		for time in interval:
			t= datetime.datetime.strptime(time, "%H:%M")
			timeInterval[i]=t.hour*60+t.minute
			i=i+1
			#print(timeInterval)
		if(timeInterval[0]<current_time and timeInterval[1]>current_time):
			r1s = 0
			r2s = 0
			r3s = 1
			r4s = 0
if "4" in sod:
	for interval in sod["4"]:
		timeInterval=[0,0]#Time inteval 0 is the start 1 is the end
		i=0
		for time in interval:
			t= datetime.datetime.strptime(time, "%H:%M")
			timeInterval[i]=t.hour*60+t.minute
			i=i+1
			#print(timeInterval)
		if(timeInterval[0]<current_time and timeInterval[1]>current_time):
			r1s = 0
			r2s = 0
			r3s = 0
			r4s = 1

data['Reefer1'] = r1s
data['Reefer2'] = r2s
data['Reefer3'] = r3s
data['Reefer4'] = r4s
data['Automatic'] = r5s
color = ['red', 'green']
r1c = color[int(r1s)]
r2c = color[int(r2s)]
r3c = color[int(r3s)]
r4c = color[int(r4s)]
r5c = color[int(r5s)]


phaseAVoltage=data['VoltageA'];
phaseBVoltage=data['VoltageB'];
phaseCVoltage=data['VoltageC'];
phaseACurrent=data['CurrentA'];
phaseBCurrent=data['CurrentB'];
phaseCCurrent=data['CurrentC'];
data['lock'] = False

with open("ReeferStatus.ss", "w") as jsonFile:
	json.dump(data, jsonFile)

x ='''Content-type: text/html /n/n

<html>
	   <meta http-equiv="refresh" content="5">
	   <form action='main.py' method='POST'>
	   Reefers On are Labeled Green, this will take force over the schedule
<br>

	<input type='submit' value='reefer1' name='reefer1' style='background-color:''' + r1c + ''''/>        
	<input type='submit' value='reefer2' name='reefer2' style='background-color:''' + r2c + ''''/>       
	<input type='submit' value='reefer3' name='reefer3' style='background-color:''' + r3c + ''''/>        
	<input type='submit' value='reefer4' name='reefer4' style='background-color:''' + r4c + ''''/>   
	<input type='submit' value='Automatic' name='automatic' style='background-color:''' + r5c + ''''/>        

<br>
	VoltageA =''' + str(phaseAVoltage) + '''  VoltageB =''' + str(phaseBVoltage) + '''   VoltageC =''' + str(
	phaseCVoltage) + '''
<br>    
	CurrentA =''' + str(phaseACurrent) + '''  CurrentB =''' + str(phaseBCurrent) + '''   CurrentC =''' + str(
	phaseCCurrent) + '''
<br>
<br>
<br>
In each field you will enter the weekly schedule as follows
Each reefer wiil be refered to by its number 1,2,3,4 <REF>, t
te time will be in military format HHMM will be referred to as <end>,<start>
<REF>:{<start1>,<end1>},{<start2>,<end2>},..

<br>
<br>
	Monday: <input type="text" name="Monday" value ="'''+str(data['Monday'])+ '''"/>
<br>
	Tuesday: <input type="text" name="Tuesday" value ="'''+str(data['Tuesday'])+ '''"/>
<br>
	Wednesday: <input type="text" name="Wednesday" value ="'''+str(data['Wednesday'])+ '''"/>
<br>
	Thursday: <input type="text" name="Thursday" value ="'''+str(data['Thursday'])+ '''"/>
<br>
	Friday: <input type="text" name="Friday" value ="'''+str(data['Friday'])+ '''"/>
<br>
	Saturday: <input type="text" name="Saturday" value ="'''+str(data['Saturday'])+ '''"/>
<br>
	Sunday: <input type="text" name="Sunday" value ="'''+str(data['Sunday'])+ '''"/>
<br>

	<input type='submit' value='schedule' name='schedule' style='background-color:yellow'/>        

</form>
</html>  '''
print(x)
