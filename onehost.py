#!/usr/bin/env python

from time import sleep
from gpiozero import Button, OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory

#set some vars
#set local pinboard
local_factory = PiGPIOFactory()
#define pins remote 
#for the LED and the LEDShifter
datapin=17  #datashift
clockpin=22 #clockshift
latchpin=18 #shifting

data=OutputDevice(datapin)
clock=OutputDevice(clockpin)
latch=OutputDevice(latchpin)
#set local pins for buttons
leftup=18
leftdown=4
rightdown=22
rightup=23
switch=25

blu=Button(18,pull_up=False,pin_factory=local_factory)
bld=Button(4,pull_up=False,pin_factory=local_factory)
brd=Button(22,pull_up=False,pin_factory=local_factory)
bru=Button(23,pull_up=False,pin_factory=local_factory)
bs=Button(25,pull_up=False,pin_factory=local_factory)

#pausetimes
pauseclock=0
pause=0.1

#counter
sumled=0
tmpled=0

#LED Digi codes
leds=[61404, 60996, 61304, 61292, 61156, 61356, 61372, 61252, 61436, 61420, 9180, 8772, 9080, 9068, 8932, 9132, 9148, 9028, 9212, 9196, 48604, 48196, 48504, 48492, 48356, 48556, 48572, 48452, 48636, 48620, 47068, 46660, 46968, 46956, 46820, 47020, 47036, 46916, 47100, 47084, 29660, 29252, 29560, 29548, 29412, 29612, 29628, 29508, 29692, 29676, 55260, 54852, 55160, 55148, 55012, 55212, 55228, 55108, 55292, 55276, 57308, 56900, 57208, 57196, 57060, 57260, 57276, 57156, 57340, 57324, 41948, 41540, 41848, 41836, 41700, 41900, 41916, 41796, 41980, 41964, 65500, 65092, 65400, 65388, 65252, 65452, 65468, 65348, 65532, 65516, 63452, 63044, 63352, 63340, 63204, 63404, 63420, 63300, 63484, 63468 ]

#maincoding
#Output defs

def clocking():
  clock.on()
  time.sleep(pauseclock)
  clock.off()
  time.sleep(pauseclock)

def digital_Write():
  latch.off()
  clocking()
  latch.on()

def set_bit(bit):
  if ( bit == 0 ):
    data.off()
  else:
    data.on()

def get_binlist_from_digit(num):
  magic = lambda num: map(int, str(num))
  return magic

def shiftout(index):
  digit = get_binlist_from_digit(leds[index])
  for bit in digit:
    set_bit(bit)
    clock()
  digital_Write()

def get_input():
  tmpled=sumled
  if bs.is_pressed == False:
    if blu.is_pressed == True:
      tmpled = sumled+10
    elif bld.is_pressed == True:
      tmpled = sumled-10
    elif brd.is_pressed == True:
      tmpled = sumled-1
    elif bru.is_pressed == True:
      tmpled = sumled+1
    if tmpled != sumled:
      shiftout(tmpled)
  else:
    bs.wait_for_release(timeout=None)

#main part
def main():
  running=True
  while running == True:
    try: 
      get_input()
      sleep(pause)
      print ("PING!")
    except KeyboardInterrupt:
      running=False

if __name__=="__main__":
  main()
