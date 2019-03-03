import machine
from machine import TouchPad, Pin, PWM
import esp32
import time
import micropython

from umqtt.simple import MQTTClient

micropython.alloc_emergency_exception_buf(100)

#CONFIG = {
#    "broker": "broker.hivemq.com",
#    "client_id": b"D1_Mini_" + "dev_B0",
#    "topic": b"Synthwave led",
#}

CONFIG = {
    "broker": "m24.cloudmqtt.com",
    "port": b"18194",
    "client_id": b"ESP32?Lite",
    "user_name": b"Anaga",
    "user_pass": b"a12qrewa",
    "topic": "esp",
}
#
# S1 = 25 = 25
# S2 = 26 = 26
# Key= 33 = 33
#
button = Pin(33, Pin.IN)
s1 = Pin(25, Pin.IN)
s2 = Pin(26, Pin.IN)

print("Start IRQ")

# onBoard LED 22
#
led = Pin(22, Pin.OUT)

# offBoard LED red 17
# offBoard LED Gren 16
red_pwm = PWM(Pin(17),5000) #D1
gren_pwm = PWM(Pin(16),5000) #D2

# Touch Pluss
# t_plus = 13
t_plus = TouchPad(Pin(13))
t_plus.config(250)               # configure the threshold at which the pin is considered touched
#t_red.irq(trigger=Pin.IRQ_FALLING, handler=s1_down)

# Touch Minnus
# t_minus = 15
t_minus = TouchPad(Pin(15))
t_minus.config(250) 


counter = 0
max_count = 100
min_count = 0

def s1_down(p):
    global counter
    s1_val = s1.value()
    s2_val = s2.value()
    #print('S1 down, now S1 value ',s1_val, ' S2 value ', s2_val)
    if s1_val and s2_val:
        print ("CW")
        if counter<max_count:
            counter+=1;

def s2_down(p):
    global counter
    s1_val = s1.value()
    s2_val = s2.value()
    #print('S2 down, now S1 value ',s1_val, ' S2 value ', s2_val)
    if s1_val and s2_val:
        print ("CCW")
        if counter >min_count:
          counter-=1;

def s_change(p):
    print(p, ' change, now value ', p.value())
    
def sub_cb():
    print ("input")
    
#button.irq(trigger=Pin.IRQ_FALLING, handler=s_down)
button.irq(trigger=Pin.IRQ_RISING| Pin.IRQ_FALLING, handler=s_change)

s1.irq(trigger=Pin.IRQ_FALLING, handler=s1_down)
#s1.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=s_change)

s2.irq(trigger=Pin.IRQ_FALLING, handler=s2_down)
#s2.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=s_change)



client = MQTTClient(CONFIG['client_id'], CONFIG['broker'], CONFIG['port'], CONFIG['user_name'], CONFIG['user_pass'])
client.set_callback(sub_cb)
client.connect()
print("Connected to {}".format(CONFIG['broker']))
client.subscribe("esp/led")

timer = 0
print("Ready, counter ", counter)
print("Ready, counter ", counter)
last_count = counter
while True:
    time.sleep_ms(100) 
    #print("Timer", timer, ' counter ', counter);
    timer+=0.1
    #s1_down(t_plus)
    #s2_down(t_minus)
    gren_pwm.duty(counter*10)

    if (counter != last_count):
        
        print("Timer", timer, ' counter ', counter);
        last_count = counter
        client.publish("esp/rot", bytes(str(counter), 'utf-8'))
        
        print('Sensor state: {}'.format(counter))
        
        
        