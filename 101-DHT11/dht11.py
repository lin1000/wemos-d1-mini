import machine
import time
import dht

#Connect data pin on GPIO 4
d = dht.DHT11(machine.Pin(14))
rled = machine.Pin(2, machine.Pin.OUT)
gled = machine.Pin(0, machine.Pin.OUT)

temp_list = []


while True:
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    #print("Current Humidity {}%".format(hum))
    #print("Current Temperature {}{}C".format(temp, '\u00b0'))
    temp_list.insert(0,temp)
    if(len(temp_list) > 10):
        print(str(temp_list))
        temp_list.pop()
        #print("pop " + str(temp_list.pop()))
        avg_temp = sum(temp_list)/len(temp_list)
        print("current temperature : {}{}C".format(avg_temp,'\u00b0'))
        if(avg_temp >= 35):
            rled.on()
            gled.off()
        else:
            rled.off()
            gled.on()
    else:
        print("Collecting Sensor Data ...")
    time.sleep(1)
