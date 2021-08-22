#!/usr/bin/env python

import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
import requests

def post_temp(temp):
    try:
        r = requests.post("http://nbv.cx:5000/api/temp", params={"temp":str(temp)})
        return r.json()
    except:
        pass

def PID(Kp, Ki, Kd, MV_bar=0):
    # initialize stored data
    e_prev = 0
    t_prev = -100
    I = 0
    
    # initial control
    MV = MV_bar
    
    while True:
        # yield MV, wait for new t, PV, SP
        t, PV, SP = yield MV
        
        # PID calculations
        e = SP - PV
        
        P = Kp*e
        I = I + Ki*e*(t - t_prev)
        D = Kd*(e - e_prev)/(t - t_prev)
        
        MV = MV_bar + P + I + D
        
        # update stored data for next iteration
        e_prev = e
        t_prev = t

pi = pigpio.pi()

if not pi.connected:
   exit(0)

sensor = pi.spi_open(0, 1000000, 0)

while True:
   c, d = pi.spi_read(sensor, 2)
   if c == 2:
      word = (d[0]<<8) | d[1]
      if (word & 0x8006) == 0: # Bits 15, 2, and 1 should be zero.
         t = (word >> 3)/4.0
         print("{:.2f}".format(t))
         data = post_temp("{:.2f}".format(t))
         print(data)
      else:
         print("bad reading {:b}".format(word))
   time.sleep(10)

pi.spi_close(sensor)

pi.stop()