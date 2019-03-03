from machine import Pin, PWM
from time import sleep

print("Start")
led = Pin(2, Pin.OUT)
button = Pin(13, Pin.IN)
s1 = Pin(14, Pin.IN)
s2 = Pin(16, Pin.IN)

red_pwm = PWM(Pin(5),5000) #D1
gren_pwm = PWM(Pin(4),5000) #D2

print("Ready")
while True:
    button_state = button.value()
    led.value(button_state)
    red_pwm.duty(s1.value()*500)
    gren_pwm.duty(s2.value()*500)
    sleep(0.1)
    if button_state:
        print("Ready, s1, s2")
        print(s1.value())
        print(s2.value())
        sleep(0.3)
        