from machine import Pin, PWM
from time import sleep
from umqtt.simple import MQTTClient
import micropython
micropython.alloc_emergency_exception_buf(100)

CONFIG = {
    "broker": "broker.hivemq.com",
    "client_id": b"D1_Mini_" + "dev_B0",
    "topic": b"home_mini24",
}


client = None
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

print("Start IRQ")
led = Pin(2, Pin.OUT)

#
# S1 = D5 = 14
# S2 = D6 = 12
# Key= D7 = 13
#
button = Pin(13, Pin.IN)
s1 = Pin(14, Pin.IN)
s2 = Pin(12, Pin.IN)

#button.irq(trigger=Pin.IRQ_FALLING, handler=s_down)
button.irq(trigger=Pin.IRQ_RISING| Pin.IRQ_FALLING, handler=s_change)

s1.irq(trigger=Pin.IRQ_FALLING, handler=s1_down)
#s1.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=s_change)

s2.irq(trigger=Pin.IRQ_FALLING, handler=s2_down)
#s2.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=s_change)

red_pwm = PWM(Pin(5),5000) #D1
gren_pwm = PWM(Pin(4),5000) #D2

client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])
client.connect()
print("Connected to {}".format(CONFIG['broker']))

timer = 0
print("Ready, counter ", counter)
while True:
    sleep(2)
    print("Timer", timer, ' counter ', counter);
    timer+=1
    gren_pwm.duty(counter*10)
    client.publish('{}/{}'.format(CONFIG['topic'],
                                          CONFIG['client_id']),
                                          bytes(str(counter), 'utf-8'))
    print('Sensor state: {}'.format(counter))
        