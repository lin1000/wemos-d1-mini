import machine
import time
import dht
from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd


## LCD PARAMETERS

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

# Defines shifts or masks for the various LCD line attached to the PCF8574

# MASK_RS = 0x01
# MASK_RW = 0x02
# MASK_E = 0x04
# SHIFT_BACKLIGHT = 3
# SHIFT_DATA = 4

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)        


#Connect data pin on GPIO 4
d = dht.DHT11(machine.Pin(14))
rled = machine.Pin(2, machine.Pin.OUT)
gled = machine.Pin(0, machine.Pin.OUT)

temp_list = []

first_time_display = True

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

        print("Running i2c interact with lcd")
        if(first_time_display):
            first_time_display = False
            lcd.move_to(0,0)
            lcd.putstr("Temperature :")
        else:
            lcd.move_to(0,1)
            lcd.putstr("          ")
            lcd.move_to(0,1)
            lcd.putstr(str(avg_temp) + " C")
            print("lcd.cursor_x" + str(lcd.cursor_x))
            print("lcd.cursor_y" + str(lcd.cursor_y))

        if(avg_temp >= 35):
            rled.on()
            gled.off()
        else:
            rled.off()
            gled.on()
    else:
        print("Collecting Sensor Data ...")
        lcd.putstr("Sensening : {}".format(10-len(temp_list)))
        lcd.move_to(0,0)
    time.sleep(1)
