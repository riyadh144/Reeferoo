#!/usr/bin/env python3
import cgi
import cgitb
import json
import time
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
lock = True
data=""
while (lock):
    with open("ReeferState.ss") as json_file:
        data = json.load(json_file)
    lock = bool(data["lock"]);
    time.sleep(.1)

data['lock'] = True;
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

form = cgi.FieldStorage()
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
    data['Monday']= form.getfirst("Monday")
    data['Tuesday']= form.getfirst("Tuesday")
    data['Wednesday']= form.getfirst("Wednesday")
    data['Thursday']= form.getfirst("Thursday")
    data['Friday']= form.getfirst("Friday")
    data['Saturday']= form.getfirst("Saturday")
    data['Sunday']= form.getfirst("Sunday")
    for interval in sod["1"]:
        timeInterval={0,0}#Time inteval 0 is the start 1 is the end
        i=0
        for time in interval:
            t= datetime.datetime.strptime(time, "%H:%M")
            timeInterval[i]=t.hour*60+t.minute
            i=i+1
            print(timeInterval)
        if(timeInterval[0]<current_time and timeInterval[1]>current_time):
            r1s = 1
            r2s = 0
            r3s = 0
            r4s = 0
    for interval in sod["2"]:
        timeInterval={0,0}#Time inteval 0 is the start 1 is the end
        i=0
        for time in interval:
            t= datetime.datetime.strptime(time, "%H:%M")
            timeInterval[i]=t.hour*60+t.minute
            i=i+1
            print(timeInterval)
        if(timeInterval[0]<current_time and timeInterval[1]>current_time):
            r1s = 0
            r2s = 1
            r3s = 0
            r4s = 0

    for interval in sod["3"]:
        timeInterval={0,0}#Time inteval 0 is the start 1 is the end
        i=0
        for time in interval:
            t= datetime.datetime.strptime(time, "%H:%M")
            timeInterval[i]=t.hour*60+t.minute
            i=i+1
            print(timeInterval)
        if(timeInterval[0]<current_time and timeInterval[1]>current_time):
            r1s = 0
            r2s = 0
            r3s = 1
            r4s = 0

    for interval in sod["4"]:
        timeInterval={0,0}#Time inteval 0 is the start 1 is the end
        i=0
        for time in interval:
            t= datetime.datetime.strptime(time, "%H:%M")
            timeInterval[i]=t.hour*60+t.minute
            i=i+1
            print(timeInterval)
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

x = """Content-type: text/html\n\n
<html>
       <meta http-equiv="refresh" content="5">
       <form action='dropdown.py' method='POST'>
       Reefers On are Labeled Green, this will take force over the schedule
<br>
    <input type='submit' value='reefer1' name='reefer1' style='background-color:""" + r1c + """'/>        
    <input type='submit' value='reefer2' name='reefer2' style='background-color:""" + r2c + """'/>       
    <input type='submit' value='reefer3' name='reefer3' style='background-color:""" + r3c + """'/>        
    <input type='submit' value='reefer4' name='reefer4' style='background-color:""" + r4c + """'/>   
    <input type='submit' value='Automatic' name='automatic' style='background-color:""" + r5c + """'/>        

<br>
    VoltageA =""" + str(phaseAVoltage) + """  VoltageB =""" + str(phaseBVoltage) + """   VoltageC =""" + str(
    phaseCVoltage) + """
<br>    
    CurrentA =""" + str(phaseACurrent) + """  CurrentB =""" + str(phaseBCurrent) + """   CurrentC =""" + str(
    phaseCCurrent) + """
<br>
<br>
<br>
In each field you will enter the weekly schedule as follows
Each reefer wiil be refered to by its number 1,2,3,4 <REF>, t
te time will be in military format HHMM will be referred to as <end>,<start>
<REF>:{<start1>,<end1>},{<start2>,<end2>},..

<br>
<br>
    Monday: <input type="text" name="Monday">
<br>
    Tuesday: <input type="text" name="Tuesday">
<br>
    Wednesday: <input type="text" name="Wednesday">
<br>
    Thursday: <input type="text" name="Thursday">
<br>
    Friday: <input type="text" name="Friday">
<br>
    Saturday: <input type="text" name="Saturday">
<br>
    Sunday: <input type="text" name="Sunday">
<br>

    <input type='submit' value='Submit Schedule' name='schedule' style='background-color:yellow'/>        

</form>hours
</html>  """
print(x)
