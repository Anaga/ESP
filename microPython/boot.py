# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import network
import webrepl
#webrepl.start()
gc.collect()

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('TP-LINK-123', 'adminAdmin')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
print('booting 1')    
do_connect()
print('booting 2')