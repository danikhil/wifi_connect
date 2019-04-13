import subprocess
import json

def get_interface_name():
    interface = ""
    proc = subprocess.getoutput('iwconfig | grep IEEE')
    line = proc.split('\n')
    for l in line:
        ls = l.split()
        if "IEEE" in ls:
            interface = ls[0]
            return interface

def wifi_scan():
    interface = get_interface_name()
    wireless_data = subprocess.getoutput('sudo iwlist '+ interface + ' scan | egrep "ESSID|Quality|Encryption key"')
    wireless_data = wireless_data.split('\n')
    wireless_data = [i.strip() for i in wireless_data]
    essid = wireless_data[2::3]
    encryption = wireless_data[1::3]
    quality = wireless_data[0::3]
    quality = [i.split(' ')[0] for i in quality]
    network = []
    for i in range(len(essid)):
        network.append({'essid': essid[i][7:-1],'quality': quality[i][8:],'encryption': encryption[i][15:]})
    return network

def wifi_reconnect():
    try:
        with open('wifi_config.txt', 'r') as wifi_config:
            data = json.load(wifi_config)
            essid = data['ESSID']
            subprocess.getoutput('sudo nmcli con up' + essid)
            return True
    except Exception as e:
        return e

def wifi_connect(essid, key):
    try:
        res = subprocess.getoutput('sudo nmcli dev wifi connect ' + essid + ' password ' + key + ' | grep Error')
        if res == "":
            return True
        else:
            return False
    except:
        return False
