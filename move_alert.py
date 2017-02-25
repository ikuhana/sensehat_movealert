from sense_hat import SenseHat
import time
import http.client, urllib
import os

sense = SenseHat()

def raise_alarm():
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": os.environ.get("TOKEN", None),
        "user": os.environ.get("USER", None),
        "message": "Rpi is moving",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    time.sleep(10)

#History for comparing differences
x, y, z = [], [], []

#sensitivity
sens = 3

while 1:
    raw = sense.get_gyroscope_raw()
    x.append(raw['x'])
    if len(x) > 10:
        x.pop(0)
        
    y.append(raw['y'])
    if len(y) > 10:
        y.pop(0)
        
    z.append(raw['z'])
    if len(z) > 10:
        z.pop(0)
    
    #How many times in seconds can rasperry pi be moved
    xc = sum(1 for n in x if n>0.05)
    yc = sum(1 for n in y if n>0.05)
    zc = sum(1 for n in z if n>0.05)

    if xc > sens or yc > sens or zc > sens:
        raise_alarm()
        x, y, z = [], [], []
    print('%s %s %s--- %s %s %s\r'%(xc, yc, zc, round(raw['x'], 3), round(raw['y'], 3), round(raw['z'], 3)), end='')
    time.sleep(0.1)
