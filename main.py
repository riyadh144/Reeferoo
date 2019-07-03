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
sod= data[today]  # schedule of the day
# mmm="ds"
form = cgi.FieldStorage()
# cgit.enable(display0, logdir=OUTDIR)
if "reefer1" in form and r5s==0:
	r1s = int(not r1s)
	r2s = 0
	r3s = 0
	r4s = 0
elif "reefer2" in form and r5s==0:
	r2s = int(not r2s)
	r1s = 0
	r3s = 0
	r4s = 0

elif "reefer3" in form and r5s==0:
	r3s = int(not r3s)
	r1s = 0
	r2s = 0
	r4s = 0


elif "reefer4" in form and r5s==0:
	r4s = int(not r4s)
	r1s = 0
	r2s = 0
	r3s = 0

elif "Automatic" in form:
	r5s = int(not r5s)


elif "schedule" in form:
	data['Monday']      =ast.literal_eval((form.getvalue("Monday")))
	data['Tuesday']     =ast.literal_eval((form.getvalue("Tuesday")))
	data['Wednesday']   =ast.literal_eval((form.getvalue("Wednesday")))
	data['Thursday']    =ast.literal_eval((form.getvalue("Thursday")))
	data['Friday']      =ast.literal_eval((form.getvalue("Friday")))
	data['Saturday']    =ast.literal_eval((form.getvalue("Saturday")))
	data['Sunday']      =ast.literal_eval((form.getvalue("Sunday")))


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


phaseAVoltage=round(data['VoltageA']/8.57,2)
phaseBVoltage=round(data['VoltageB']/8.57,2)
phaseCVoltage=round(data['VoltageC']/8.57,2)
phaseACurrent=round(data['CurrentA']*.0069,2)
phaseBCurrent=round(data['CurrentB']*.0069,2)
phaseCCurrent=round(data['CurrentC']*.0069,2)
data['lock'] = False

with open("ReeferStatus.ss", "w") as jsonFile:
	json.dump(data, jsonFile)

x ='''Content-type: text/html /n/n

<html>
	   <meta http-equiv="refresh" content="15">
	   <form action='main.py' method='POST'>
	   Reefers On are Labeled Green, this will take force over the schedule to over ride the schedule you need to press the Automatic button
<br>

	<input type='submit' value='daikiniic' name='reefer1' style='background-color:''' + r1c + ''''/>        
	<input type='submit' value='reefer2' name='reefer2' style='background-color:''' + r2c + ''''/>       
	<input type='submit' value='reefer3' name='reefer3' style='background-color:''' + r3c + ''''/>        
	<input type='submit' value='reefer4' name='reefer4' style='background-color:''' + r4c + ''''/>   
	<input type='submit' value='Automatic' name='Automatic' style='background-color:''' + r5c + ''''/>        

<br>
	VoltageA =''' + str(phaseAVoltage) + '''  VoltageB =''' + str(phaseBVoltage) + '''   VoltageC =''' + str(
	phaseCVoltage) + '''
<br>    
	CurrentA =''' + str(phaseACurrent) + '''  CurrentB =''' + str(phaseBCurrent) + '''   CurrentC =''' + str(
	phaseCCurrent) + '''
<br>
<br>
<br>
In each field you will enter the weekly schedule as follows.\n
Each reefer will be refered to by its number 1,2,3,4 <REF>, the time will be in military format HH:MM will be referred to as <end>,<start>
<REF>:[<start1>,<end1>],[<start2>,<end2>],..

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
