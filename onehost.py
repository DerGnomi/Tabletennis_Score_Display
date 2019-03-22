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
  print (get_sumled())
  led_status_r.on()
  digit = int(leds[get_sumled()])
  print digit
  b_digit = bin(digit)[2:]
  print (b_digit)
  b_len = len(b_digit) 
  print (b_len)
  data.off()
  offset=16-b_len
  latch.on()
  if offset > 0:
    for i in range(offset):
      clocking()
  for bit in b_digit:
    if ( int(bit) == 0 ):
      data.off()
    else:
      data.on()
    clocking()
  #shifting is one too far
  latch.off()
  clocking()
  led_status_r.off()

def reversed( y, num_bits ):
  x = bin(y)[2:]  
  answer = 0
  for i in range( num_bits ):                   # for each bit number
    if (x & (1 << i)):                        # if it matches that bit
      answer |= (1 << (num_bits - 1 - i))   # set the "opposite" bit in answer
  return answer

def set_sumled(su):
  print ("Set new state")
  global sumled 
  sumled += su
  shiftout()

def get_sumled():
  return sumled

def clocking():
  clock.on()
  sleep(pauseclock)
  clock.off()
  sleep(pauseclock)

#def digital_Write():
#  latch.off()
#  clocking()
#  latch.on()

#main part
def main():
  running=True
  shiftout()
  while running == True:
    try:
      if bs.is_pressed:
        if ledstatus.is_lit:
          ledstatus.off()
        if not blu.is_pressed:
          set_sumled(10)
        if not bld.is_pressed:
          set_sumled(-10)
        if  not brd.is_pressed:
          set_sumled(-1)
        if not bru.is_pressed:
          set_sumled(1)
        print("run")
        sleep(0.5)
      else:
        ledstatus.on()
        print("no")
        bs.wait_for_press(timeout=None)
    except GPIOZeroError:
      #Set a blink led
      ledstatus.blink()
      #running=False

#Execution
if __name__=="__main__":
  main()
