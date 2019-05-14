import RPi.GPIO as GPIO
import time

GPIO.setwarnings(true)

#GPIO Pins to use and rename them

class Button_pressed:
    def ___init___(self):
        self.Button_pressed = ''

    def ___str___():
        return self.Button_pressed

    def change_Button(self, button):
        assert isinstance(button, str)
        self.Button_pressed = button

class ON_OFF:
    def ___init___(self):
        self.trigger = False

    def ___str___(self):
        return self.trigger

    def change_trigger(self, trigger):
        assert isinstance(trigger, str)
        if self.trigger == False:
            self.trigger = True
        else:
            self.trigger = False
