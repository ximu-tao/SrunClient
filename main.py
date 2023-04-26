print("Start")

import utime
import machine
import json
import random

import net

configs = json.load(open("config.json", encoding='utf-8'))
current_config = configs['config'][random.randint(0, len(configs['config']) - 1)]

print(current_config)

wifi_ssid = current_config['wifi_ssid']
wifi_passwd = current_config['wifi_passwd']
username = current_config['username']
passwd = current_config['passwd']

led_pin = 12

deepsleep_time_ms = 60 * 5 * 1000

pin2 = machine.Pin(led_pin, machine.Pin.OUT)


def twinkle(num, interval):
    num *= 2
    while num != 0:
        pin2.value(pin2.value() ^ 1)
        utime.sleep_ms(interval)
        num -= 1


def connectWIFI():
    pin2.value(1)

    net.connectWIFI(wifi_ssid, wifi_passwd)

    if net.isconnected():
        twinkle(3, 1000)
    else:
        # 无法连接WIFI，快速闪烁一分钟后重启设备
        twinkle(150 , 200)
        machine.reset()


connectWIFI()

import heartbeat

if not heartbeat.check_online():
    print('not online')
    heartbeat.try_login(username, passwd, '10.10.10.3')
else:
    print('is online')
twinkle(5, 200)

print("to deepsleep")
machine.deepsleep(deepsleep_time_ms)

print("Main End")

machine.reset()
