# Tabletennis_Score_Display

I changed from Arduino IR controlled to a button controlled score display.

My goal was to show the points of each team

Now the Display is controlled by a portable console with 4 Buttons and 1 switch to turn off/on

The Display has two 7-segment digits controled by a shiftregister (74HC595)

## Getting Started

### Modules to install

You need to install Python and gpiozero to connect from one pi to another

```
sudo apt-get update
sudo apt install python
sudo apt install python-gpiozero
```

### Remote Pin Access

also you have to enable the remote access to the GPIO Pins on the remote Pi

```
sudo raspi-config
```

### Insert the remote ip

```
remote_factory = PiGPIOFactory(host='192.168.2.40')
```

## Connect the Pins and the input / output devices

### Local device

* Button to increase the left digit by 1 is PIN 17
* Button to decrease the left digit by 1 is PIN 18
* Button to increase the right digit by 1 is PIN 22
* Button to decrease the right digit by 1 is PIN 23
* Switch should be on PIN 26

Connect the other side of the Button/Switch to Ground

### Remote device

[74HC595 Datasheet](https://www.sparkfun.com/datasheets/IC/SN74HC595.pdf):
* Data input (SER 14) connect to PIN 17 on the RPI
* Clock input (RCLK 12) connect to PIN 22 on the RPI
* Latch input (OE 13) connect to PIN 18 on the RPI

## Portable Console

If you want to use the controlling Pi as a portable device, just get a cheap Powerbank. 6000 mAh should be enough to control the board for longer than one day

## Q&A

* If you got questions how to get this project to work, just leave me a message
