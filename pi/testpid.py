import time
import matplotlib.pyplot as plt

def PID(Kp, Ki, Kd, MV_bar=0):
    # initialize stored data
    e_prev = 0
    t_prev = -1
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
        print(f"                Error: {e:.2f} P:{P:.2f}  I:{I:.2f}  D:{D:.2f} ")
        MV = MV_bar + P + I + D
        
        # update stored data for next iteration
        e_prev = e
        t_prev = t

p = PID(8, 1.1, 0)
mv = p.send(None)
print(mv)
pv = 20
pvs = list()
mvs = list()
for i in range(100):
    mv = p.send([i, pv, 30])
    mvs.append(mv)
    if mv > 0:
        pv += mv/10
    pv -= 2
    pvs.append(pv)
    print(f"MV: {mv:.2f} PV: {pv:.2f}")

plt.figure(1)
plt.subplot(211)
plt.plot(mvs)

plt.subplot(212)
plt.plot(pvs)
plt.show()

