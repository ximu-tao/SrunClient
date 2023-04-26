print("Start")


import network
import utime
import machine

pin2 = machine.Pin(12, machine.Pin.OUT)
wlan = network.WLAN(network.STA_IF)

def twinkle(num, interval):
    num *= 2
    while num != 0:
        pin2.value(pin2.value() ^ 1)
        utime.sleep_ms(interval)
        num -= 1


def connectWIFI( ssid, password ):
    pin2.value(1)

    if wlan.active():
        wlan.active(False)

    wlan.active(True)
    try_count = 0
    while try_count < 4:
        try:
            wlan.connect(ssid, password)
            print('connectWIFI')
            if wlan.isconnected():
                break
            utime.sleep(3)
        except Exception as e:
            print(e)
            try_count += 1

    if wlan.isconnected():
        twinkle(3, 1000)
    else:
        twinkle(-1, 200)


connectWIFI( "wifi_ssid", "wifi_passwd" )

import heartbeat

if not heartbeat.check_online():
    print('not online')
    heartbeat.try_login('username', 'passwd', '202.204.105.195')
else:
    print('is online')
twinkle(5, 200)

print("to deepsleep")
machine.deepsleep(60 * 5 * 1000)

print("Main End")

machine.reset()

