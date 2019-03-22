#!/usr/bin/env python

from time import sleep
from gpiozero import *
from gpiozero.pins.pigpio import PiGPIOFactory
#import gpiozero.SPI as spi
#set some vars
#set local pinboard
local_factory = PiGPIOFactory()
remote_factory = PiGPIOFactory(host='192.168.2.40')
#define pins remote
#for the LED and the LEDShifter
datapin=17  #datashift
clockpin=22 #clockshift
latchpin=18 #shifting

data=OutputDevice(datapin,pin_factory=remote_factory)
clock=OutputDevice(clockpin,pin_factory=remote_factory)
latch=OutputDevice(latchpin,pin_factory=remote_factory)
#set local pins for buttons
leftup=17
leftdown=18
rightdown=23
rightup=22
switch=26

#test the buttons later with
# pull_up=False
# and delete "not" in main()
blu=Button(leftup,pin_factory=local_factory) #button left up
bld=Button(leftdown,pin_factory=local_factory)  #button left down
brd=Button(rightdown,pin_factory=local_factory) #button right down
bru=Button(rightup,pin_factory=local_factory) #button right up
bs=Button(switch,pin_factory=local_factory)  #switch onoff

#set local status LED
statusled=16
ledstatus=LED(statusled,pin_factory=local_factory)
led_status_r=LED(statusled,pin_factory=remote_factory)
#pausetimes
pauseclock=0
pause=0.1

#counter
sumled=0

#LED Digi codes
leds=[61404, 60996, 61304, 61292, 61156, 61356, 61372, 61252, 61436, 61420, 9180, 8772, 9080, 9068, 8932, 9132, 9148, 9028, 9212, 9196, 48604, 48196, 48504, 48492, 48356, 48556, 48572, 48452, 48636, 48620, 47068, 46660, 46968, 46956, 46820, 47020, 47036, 46916, 47100, 47084, 29660, 29252, 29560, 29548, 29412, 29612, 29628, 29508, 29692, 29676, 55260, 54852, 55160, 55148, 55012, 55212, 55228, 55108, 55292, 55276, 57308, 56900, 57208, 57196, 57060, 57260, 57276, 57156, 57340, 57324, 41948, 41540, 41848, 41836, 41700, 41900, 41916, 41796, 41980, 41964, 65500, 65092, 65400, 65388, 65252, 65452, 65468, 65348, 65532, 65516, 63452, 63044, 63352, 63340, 63204, 63404, 63420, 63300, 63484, 63468 ]

#maincoding
#Output defs

def shiftout():
  led_status_r.on()
  #status led indicates the shift for debug
  #set some vars
  #get the decimal from leds array
  digit = int(leds[get_sumled()])
  #convert the decimal to binary
  #strip of the first two binary indicator bits (0b)
  b_digit = bin(digit)[2:]
  #read the length of the bitstring
  b_len = len(b_digit)
  #set how much bits are missing to get the full 16bit length
  offset = 16-b_len
  #debug output
  #can be delete or commented
  print (get_sumled())
  print b_len
  print digit
  print b_digit
  #prepare to shift data into register
  data.off()
  latch.on()
  if offset > 0:
    for i in range(offset):
      clocking()
  for bit in b_digit:
    offset += 1
    if ( int(bit) == 0 ):
      data.off()
    else:
      data.on()
    if offset != 16:
      clocking()
  #shifting is one too far | maybe after the latch is closed
  #another bit is shifted with the gate opening
  latch.off()
  clocking()
  led_status_r.off()

def set_sumled(su):
  #debug output
  print ("Set new state")
  global sumled
  sumled += su
  #set sumled to 0 if its lower than 0 and bigger than 99
  #to avoid breaking the board
  if not ( 0 <= sumled <= 99):
    sumled = 0
  shiftout()

def get_sumled():
  return sumled

def clocking():
  clock.on()
  sleep(pauseclock)
  clock.off()
  sleep(pauseclock)

#main part
def main():
  running=True
  error=False
  error_count=0
  shiftout()
  while running == True:
    try:
      while error == False:
        if bs.is_pressed:
          if ledstatus.is_lit:
            ledstatus.off()
          if not blu.is_pressed:
            set_sumled(10)
          if not bld.is_pressed:
            set_sumled(-10)
          if not brd.is_pressed:
            set_sumled(-1)
          if not bru.is_pressed:
            set_sumled(1)
          print("run")
          sleep(0.5)
        else:
          ledstatus.on()
          print("no")
          bs.wait_for_press(timeout=None)
      if not bs.is_pressed:
          ledstatus.off()
          set_sumled(404) #reset the board
          #Fast blinking to indicate reset
          ledstatus.blink(on_time=0.2,off_time=0.2,n=20,background=False)
          error = False
          if error_count > 10:
            #Turn off the Script for more than 5 errors
            #Then debugging must be done
            running = False
    except GPIOZeroError:
      #Set a blink led
      #If the PI Errors Out
      #can be resetet by
      error_count += 1
      error=True
      ledstatus.blink()

#Execution
if __name__=="__main__":
  main()
