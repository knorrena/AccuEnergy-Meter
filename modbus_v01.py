# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import minimalmodbus
#import pymodbus
#from pymodbus.client.sync import ModbusTcpClient
import serial
import serial.tools.list_ports as port_list
import time
import paho.mqtt.client as mqtt
import pandas

ports = list(port_list.comports())
for p in ports: print (p)
#serial.Serial('COM4').close()

ser = 0
def init_serial():
    COMNUM = '/dev/ttyUSB0'
    global ser
    ser = serial.Serial(COMNUM,19200,timeout=3)
    ser.baudrate = 19200
    ser.port = COMNUM
    ser.close()
    #ser.timeout = 10
   
    if ser.isOpen(  ):
        print('Serial Port is Open')
    else:
        print('Serial Port is NOT Open')
        print('opening serial port')
        #ser.open()
       
def on_message(client, userdata, message):
    print('message recieved',str(message.payload.decode('utf-8')))
    print('topic=',message.topic)

init_serial()
"""Declare device"""
instr = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
#Check Wiring
chkwire = instr.read_register(256)  # Registernumber, number of decimals
print('############################')
print('Wiring Test',chkwire)
print('############################')

chkmode = instr.read_register(529)  # Registernumber, number of decimals
print('############################')
print('Wiring Mode',chkmode)
print('0:3lN  1:2ll  2:1ll  3:1lN')
print('############################')

#time.sleep(1)

'''
Now set up the meter as a client then create an instance
'''
print('setting as client')
client = mqtt.Client('acurev')
print('connecting to broker')
client.connect('raspberrypi')

data=[]
for i in range(10):
   
    amp = instr.read_register(4167)  # Registernumber, number of decimals
    #print('Amps',amp)
    ampscale = instr.read_register(4171)  # Registernumber, number of decimals
    #print('Ampscale',ampscale)
    volt = instr.read_register(4172)  # Registernumber, number of decimals
    print('Volts',volt)
    freq = instr.read_register(4181)  # Registernumber, number of decimals
    print('Freq',freq)
    year = instr.read_register(768)  # Registernumber, number of decimals
    #print(year)
    month = instr.read_register(769)  # Registernumber, number of decimals
    #print(month)
    day = instr.read_register(770)  # Registernumber, number of decimals
    #print(day)
    hour = instr.read_register(771)  # Registernumber, number of decimals
    #print(hour)
    minute = instr.read_register( 772)  # Registernumber, number of decimals
    #print(minute)
    ls = [amp,volt,freq,year,month,day, hour,minute]
    data.append(ls)
   
    client.publish('meter','volts')
   
    time.sleep(2)
    print('published message')
    client.on_message=on_message


ser.close()
#print(data)


colnames = [amp,volt,freq,year,month,day, hour,minute]
df = pandas.DataFrame(data=data, columns = colnames)

df.to_csv("./file.csv", sep=',',index=False)


time.sleep(10)

