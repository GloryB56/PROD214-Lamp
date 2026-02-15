from neopixel import Neopixel

from picozero import Pot

from machine import I2C, Pin
import time

from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


#SET UP LCD SCREEN
I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

#INITIATE LCD SCREEN
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#SET UP COLOR COUNT AND COLOR BUTTON
count = 0
button = Pin(15, Pin.IN, Pin.PULL_UP)

#SET UP POTENMONETER
previous_value = 0
dial = Pot(0)

#NUMBER OF LEDS
numpix = 128
strip = Neopixel(numpix, 0, 6, "GRB")

#GOES THROUGH EACH LED AND SETS THE COLOR
def set_color(rgb_tuple):
    for i in range(numpix):
        strip[i] = rgb_tuple
    strip.show()

set_color((255, 169, 87))

#LIST OF COLORS AS STRINGS AND RGB VALUES
colorTempString = ["2700K","3000K","3500K","4000K","5700K"]
colorTemps = [(255, 169, 87),(255, 180, 107),(255, 196, 137),(255, 209, 163),(255, 0, 0)]

#SHINING LIGHT BULB ICON
lcd.custom_char(0, bytearray([
  0x02,
  0x01,
  0x00,
  0x06,
  0x00,
  0x01,
  0x02,
  0x00
        ]))

lcd.custom_char(1, bytearray([
  0x00,
  0x0E,
  0x11,
  0x11,
  0x11,
  0x0E,
  0x0A,
  0x04
        ]))

lcd.custom_char(2, bytearray([
  0x08,
  0x10,
  0x00,
  0x0C,
  0x00,
  0x10,
  0x08,
  0x00
        ]))

#CALLED WHEN BUTTON IS PRESSED, DISPLAYS ON LCD
def colortemp_setting(kelvinRating):
    
    lcd.clear()
    lcd.move_to(2,0)
    lcd.putstr("Colour Temp")
    lcd.move_to(3,1)
    lcd.putchar(chr(0))
    lcd.putchar(chr(1))
    lcd.putchar(chr(2))
    lcd.move_to(6,1)
    lcd.putstr(kelvinRating)
    
colortemp_setting(colorTempString[count])

#CALLED WHEN DIAL IS TURNED, DISPLAYS ON LCD
def brightness_setting(brightness, value):
    
    lcd.clear()
    lcd.move_to(2,0)
    lcd.putstr("Brightness")
    lcd.move_to(6,1)
    if value <= 10:
        lcd.putstr("OFF")
    else if value > 80:
        lcd.putstr("HIGH")
    else:
        lcd.putstr(f"{brightness}%")
    
#INITAL STATE
colortemp_setting(colorTempString[count])

#RUNS THIS LOOP CONSTANTLY
while True:
    
    #do some cheeky maths to translate analog signal into 100-10 brightness levels
    processed_value = (int((dial.value) * 100))
    
    if processed_value > 10:
        set_color(colorTemps[count])
    
    #TURNS OFF LEDS
    if processed_value < 10:
        processed_value = 10
        set_color((0,0,0))
        
    print(processed_value)
    
    
    if previous_value == 0:
        previous_value = processed_value
    
    #CHANGES BRIGHTNESS OF LEDS, SET TO 10 TO AVOID CURRENT NOISE
    if processed_value > 10:
        strip.brightness(processed_value)
    
    #DISPLAYS BRIGHTNESS SETTING ON LCD IF DIAL IS TURNED ENOUGH
    if abs(processed_value - previous_value) > 5:
        brightness_setting(int(processed_value), processed_value)
        previous_value = processed_value
    
    #CYCLES THROUGH COLOR OPTIONS
    if button.value() == 0:
        if 0 <= count <= 4:
            count = (count + 1) % 5
            set_color(colorTemps[count])
            colortemp_setting(colorTempString[count])
        else:
            count = 0
    
    
    strip.show()
    time.sleep(0.1)
    

    
    
            
        
