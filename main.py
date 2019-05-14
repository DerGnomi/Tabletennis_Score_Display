#!/usr/bin/env python
#import modules
from time import sleep
from gpiozero import *
from gpiozero.pins.pigpio import PiGPIOFactory

#set some vars
#define local pinboard
local_factory = PiGPIOFactory()
#define remote pinoboard
remote_factory = PiGPIOFactory(host='192.168.20.2')

###############
# REMOTE PINS #
###############

#PINs defined
datapin=17  #datashift  pin
clockpin=22 #clockshift pin
latchpin=18 #shifting   pin
#Outputdevice define with the previous defined pins
data=OutputDevice(datapin,pin_factory=remote_factory)
clock=OutputDevice(clockpin,pin_factory=remote_factory)
latch=OutputDevice(latchpin,pin_factory=remote_factory)

##############
# LOCAL PINS #
##############

#PINs defiend
leftup=17     #Left side one up     pin
leftdown=18   #Left side one down   pin
rightdown=23  #Right side one down  pin
rightup=22    #Right side one up    pin
switch=26     #switch on/off        switch
#Inputdevices (Button and switch) defined with the previous defiend pins
blu=Button(leftup,pin_factory=local_factory)    #button left up
bld=Button(leftdown,pin_factory=local_factory)  #button left down
brd=Button(rightdown,pin_factory=local_factory) #button right down
bru=Button(rightup,pin_factory=local_factory)   #button right up
bs=Button(switch,pin_factory=local_factory)     #switch onoff
#set local status LED
statusled=16  #debug status LED
ledstatus=LED(statusled,pin_factory=local_factory)

#############
# DEBUGGING #
#############

db=True

###########
# COUNTER #
###########

sumled=0

#############
# LED CODES #
#############

#the index represents the number which will be displayed
#so the array is 100 numbers long
leds=[61404, 60996, 61304, 61292, 61156, 61356, 61372, 61252, 61436, 61420, 9180, 8772, 9080, 9068, 8932, 9132, 9148, 9028, 9212, 9196, 48604, 48196, 48504, 48492, 48356, 48556, 48572, 48452, 48636, 48620, 47068, 46660, 46968, 46956, 46820, 47020, 47036, 46916, 47100, 47084, 29660, 29252, 29560, 29548, 29412, 29612, 29628, 29508, 29692, 29676, 55260, 54852, 55160, 55148, 55012, 55212, 55228, 55108, 55292, 55276, 57308, 56900, 57208, 57196, 57060, 57260, 57276, 57156, 57340, 57324, 41948, 41540, 41848, 41836, 41700, 41900, 41916, 41796, 41980, 41964, 65500, 65092, 65400, 65388, 65252, 65452, 65468, 65348, 65532, 65516, 63452, 63044, 63352, 63340, 63204, 63404, 63420, 63300, 63484, 63468 ]

############
### CODE ###
############

def shiftout():
    #set the latch to off to save the input
    latch.off()
    ########
    # VARS #
    ########
    #get the decimal from leds array
    digit = int(leds[get_sumled()])
    #convert the decimal to binary and reverse it
    #strip of the first two binary indicator bits (0b)
    b_digit = bin(digit)[2:][::-1]
    #get the int from the reversed binary number
    i_digit = int(b_digit, 2)
    #read the length of the bitstring
    i_len = len(bin(i_digit)[2:])
    #if 2 is at the end of the number, the last bit must be 0 but will be stripped of
    #because it is at the beginning of the bitstring and will be stripped by convert it
    #back to int from binary
    if get_sumled() == 2 or get_sumled() == 12 or get_sumled() == 22 or get_sumled() == 32 or get_sumled() == 42 or get_sumled() == 52 or get_sumled() == 62 or get_sumled() == 72 or get_sumled() == 82 or get_sumled() == 92:
        i_len += 1
    #if the string is shorter than 14 bits it must be filled with 0 at the end
    #will also be dropped in the first step by convert from int to bit
    if 14-i_len != 0:
        for i in range(14-i_len):
            s = b_digit + '0'
            b_digit = s
        i_digit = int(b_digit, 2)
        i_len = len(bin(i_digit)[2:])
    #debug output
    #can be delete or commented if it is in production
    if db == True:
        print (get_sumled(), i_len, digit, b_digit, i_digit)
    #prepare to shift data into register
    for i in range(16):
        #checking bit by bit if the current bit is 1 or 0 and outputs its weight
        bit=(0b1000000000000000>>i)&i_digit
        if bit == 0:
            if db == True:
                #debugg output
                print (bit)
            #if bit is 0 than set datapin to off
            data.off()
        else:
            if db == True:
                #debug output
                print (bit)
            #if bit is >0 set datapin to on
            data.on()
        #clock to shift the bit into the register
        clocking()
    #when all bits are in the register unlock it with latch.on
    latch.on()
    #clock just on on, without clocking to prevent 1 bit getting shifted
    #with the clock into the register
    clock.on()

##############
# SETTER SUM #
##############
def set_sumled(su):
    #debug output
    if db == True:
        print ("Set new state")
    #import the global var to set it
    global sumled
    #To not change value from other team changing the value from the lower weight digit
    #it is permitted to rise it higher than 9
    #or lower it more than 0
    #the higher weight digit can not be raised higher than 90
    #and lower decreased than 0x (x for any other digit)
    #the value must be converted to str to strip of the first digit
    #and than back to int to compare it again
    if su == 1:
        if sumled > 18:
            if not int(str(sumled)[-1:]) == 9:
                sumled += 1
        elif not sumled == 9:
            sumled += 1
    elif su == -1:
        if sumled >= 10:
            if not int(str(sumled)[-1:]) == 0:
                sumled = sumled - 1
        else:
            sumled = sumled -1
    elif su == 10:
        if not sumled >= 90:
            sumled = sumled + 10
    elif su == -10:
        if not sumled <= 9:
            sumled = sumled - 10
    else:
        sumled = 0
    #set sumled to 0 if its lower than 0 and bigger than 99
    #to avoid breaking the board
    if not ( 0 <= sumled <= 99):
        sumled = 0
    shiftout()

##############
# GETTER SUM #
##############
def get_sumled():
    return sumled

#############
# THE CLOCK #
#############
def clocking():
    clock.on()
    sleep(0)
    clock.off()
    sleep(0)

########
# MAIN #
########
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
                    if db == True:
                        print("run")
                    sleep(0.3)
                else:
                    ledstatus.on()
                    if db == True:
                        print("stop")
                    bs.wait_for_press(timeout=None)
            # if not bs.is_pressed:
            #     ledstatus.off()
            #     set_sumled(404) #reset the board
            #     #Fast blinking to indicate reset
            #     ledstatus.blink(on_time=0.2,off_time=0.2,n=20,background=False)
            #     error = False
            #     if error_count > 10:
            #         #Turn off the Script for more than 5 errors
            #         #Then debugging must be done
            #         running = False
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
