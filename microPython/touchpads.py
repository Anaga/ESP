import machine
from machine import TouchPad, Pin
import esp32
import time

counter = 0
max_count = 100
min_count = 0

def s1_down(p):
    global counter
    val_red = t_red.read();
    if (val_red < 250):
        led.on()
        print ("Red touch")
        if counter<max_count:
            counter+=1;
    

def s2_down(p):
    global counter
    val_black = t_black.read();
    if (val_black < 250):
        led.off()
        print ("Black touch")
        if counter >min_count:
          counter-=1;
          

t_red = TouchPad(Pin(14))
t_red.config(250)               # configure the threshold at which the pin is considered touched
#t_red.irq(trigger=Pin.IRQ_FALLING, handler=s1_down)

t_black = TouchPad(Pin(12))
t_black.config(250)               # configure the threshold at which the pin is considered touched
#t_black.irq(trigger=Pin.IRQ_FALLING, handler=s2_down)

led = Pin(22, Pin.OUT)

timer = 0.0


print("Ready, counter ", counter)
last_count = counter
while True:
    time.sleep_ms(100) 
    #print("Timer", timer, ' counter ', counter);
    timer+=0.1
    s1_down(t_red)
    s2_down(t_black)
    if (counter != last_count):
        print("Timer", timer, ' counter ', counter);
        last_count = counter
    """
    val_red = t_red.read();
    val_black = t_black.read();
    if (val_red < 250): led.on()
    if (val_black < 250): led.off()
    #print("red: "+str(val_red))
    #print("black: "+str(val_black))
    """

esp32.wake_on_touch(True)
machine.lightsleep()  