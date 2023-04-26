import network
import time
print('net import')



wlan = network.WLAN(network.STA_IF)


    # sta_if.scan()
    #wlan.config(dhcp_hostname = 'esp32' )

def connectWIFI( ssid , password ):
    if wlan.active():
        wlan.active(False)
            
    wlan.active(True)
    try_count = 0
    while (try_count<4) and (not wlan.isconnected()):
        try:
            wlan.connect( ssid , password )
            print('try connect WIFI')
            if wlan.isconnected():
                break
            time.sleep(3)
        except Exception as e:
            print(e)
            try_count+=1
    return wlan.isconnected()

def ifconfig():
    return wlan.ifconfig()

def ipconfig():
    return ifconfig()


def isconnected():
    return wlan.isconnected()
    
def main():
    
    import machine
    
    
    print('net main')
    

    
    connectWIFI( "501", "12345678" )
    

    
    pin2 = machine.Pin(2, machine.Pin.OUT)
    if wlan.isconnected():
        for i in range(3):
            pin2.value(1)
            time.sleep(1)
            pin2.value(0)
            time.sleep(1)
    else:
        pin2.value(1)

if __name__ == '__main__':
    
    if not isconnected():
        main()

    print(ifconfig())
    print( isconnected() )
    import urequests

    response = urequests.get('https://api.ipify.org')

    print(response.json())

    