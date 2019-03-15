import RPi.GPIO as GPIO
import time

#Warning settings
GPIO.setwarnings(true)
#define the Pins and the GPIOs
#for shiftOut
datapin=4
clockpin=5
#pin to shift digitalout (digitalWrite)
latchpin=6
#initialice the GPIO Pins
#setup pause
pauseclock=0
pause=0.1

bits = [61404, 60996, 61304, 61292, 61156, 61356, 61372, 61252, 61436, 61420, 9180, 8772, 9080, 9068, 8932, 9132, 9148, 9028, 9212, 9196, 48604, 48196, 48504, 48492, 48356, 48556, 48572, 48452, 48636, 48620, 47068, 46660, 46968, 46956, 46820, 47020, 47036, 46916, 47100, 47084, 29660, 29252, 29560, 29548, 29412, 29612, 29628, 29508, 29692, 29676, 55260, 54852, 55160, 55148, 55012, 55212, 55228, 55108, 55292, 55276, 57308, 56900, 57208, 57196, 57060, 57260, 57276, 57156, 57340, 57324, 41948, 41540, 41848, 41836, 41700, 41900, 41916, 41796, 41980, 41964, 65500, 65092, 65400, 65388, 65252, 65452, 65468, 65348, 65532, 65516, 63452, 63044, 63352, 63340, 63204, 63404, 63420, 63300, 63484, 63468 ]

def setup_pins():
	GPIO.setmode(gpio.BCM)
	GPIO.setup(datapin,gpio.OUT)
	GPIO.output(datapin,gpio.LOW)
	GPIO.setup(clockpin,gpio.OUT)
	GPIO.output(clockpin,gpio.LOW)
	GPIO.setup(latchpin,gpio.OUT)
	GPIO.output(latchpin,gpio.LOW)

def board_cleanup():
	GPIO.cleanup()

def clock():
	GPIO.output(clockpin,GPIO.LOW)
	time.sleep(pauseclock)
	GPIO.output(clockpin,GPIO.HIGH)
	time.sleep(pauseclock)

def digital_Write():
	GPIO.output(latchpin,GPIO.LOW)
	clock()
	GPIO.output(latchpin,GPIO.HIGH)
	clock()

def set_bit(bit):
	if ( bit == 0):
		GPIO.output(datapin, GPIO.LOW)
	else:
		GPIO.output(datapin, GPIO.HIGH)

def get_binlist_from_digit(num):
	magic = lambda num: map(int, str(num))
	return magic

def shiftout(index):
	digit = get_binlist_from_digit(bits[index])
	for bit in digit:
		set_bit(bit)
		clock()
	digital_Write()

def main():
	running=True
	setup_pins()
	while running == True:
		try:
			

shiftout()
