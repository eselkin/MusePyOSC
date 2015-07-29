#!/usr/bin/env python
import socket, OSC, re, time, threading, math, random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import requests

OSC_addr_cli = '127.0.0.1', 5001
OSC_addr_srv = '127.0.0.1', 5002 # 5002 prior
s = OSC.OSCServer(OSC_addr_srv)
c = OSC.OSCClient()
c.connect(OSC_addr_cli)
s.addDefaultHandlers()

fig = plt.figure(num=None, figsize=(10, 10), dpi=90, facecolor='w', edgecolor='k')
lineCount = [0]

ax1 = fig.add_subplot(5,1,1)
line1 = [0]
hl1, = ax1.plot([0], [0])

ax2 = fig.add_subplot(5,1,2)
line2 = [0]
hl2, = ax2.plot([0], [0])

ax3 = fig.add_subplot(5,1,3)
line3 = [0]
hl3, = ax3.plot([0], [0])

ax4 = fig.add_subplot(5,1,4)
line4 = [0]
hl4, = ax4.plot([0], [0])


ax5 = fig.add_subplot(5,1,5, projection='3d')
hl5, = ax5.plot([0], [0], [0])
hl5_array = [[0], [0], [0], [0]]
ax5.set_autoscale_on(False)

def genHandler(addr, tags, stuff, source):
    if addr == "/muse/eeg":
        splitEEG(stuff)
    elif addr == "/muse/acc":
        splitACC(stuff)
    elif addr == "/error":
        err(addr, tags, stuff, source)
    elif addr == "default":
        default(addr, tags, stuff, source)
    elif addr == "/info":
        info(addr, tags, stuff, source)
    elif addr == "/muse/elements":
        elements(addr, tags, stuff, source)

def splitACC(stuff):
    hl5_array[0].append(stuff[0])
    hl5_array[1].append(stuff[1])
    hl5_array[2].append(stuff[2])
    hl5_array[3].append(hl5_array[3][-1]+1)

def err(addr, tags, stuff, source):
    pass

def default(addr, tags, stuff, source):
    pass

def elements(addr, tags, stuff, source):
    pass

def info(addr, tags, stuff, source):
    pass

def splitEEG(data):
    line1.append(data[0])
    line2.append(data[1])
    line3.append(data[2])
    line4.append(data[3])
    lineCount.append(lineCount[-1] + 1)
    if lineCount[-1] > 120:
        avgLast40 = np.mean(line1[-40:-1])
        avgPrev80 = np.mean(line1[-120:-40])
        if avgLast40 > (avgPrev80 + 200):
           signalAction(0)
        if avgLast40 < (avgPrev80 - 200):
           signalAction(1)

def signalAction(i):
    if i == 0:
        r = requests.get('http://127.0.0.1:5000/on')
    if i == 0:
        r = requests.get('http://127.0.0.1:5000/off')

def animateGraphs(i):
    # data should already be in memory
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    ax5.cla()
    if lineCount[-1] < 200:
        ax1.plot(lineCount, line1)
        ax2.plot(lineCount, line2)
        ax3.plot(lineCount, line3)
        ax4.plot(lineCount, line4)
    else:
        ax1.set_xlim(lineCount[-1]-200, lineCount[-1])
        ax1.plot(lineCount[lineCount[-1]-200:], line1[lineCount[-1]-200:])
        ax2.set_xlim(lineCount[-1] - 200, lineCount[-1])
        ax2.plot(lineCount[lineCount[-1]-200:], line2[lineCount[-1]-200:])
        ax3.set_xlim(lineCount[-1] - 200, lineCount[-1])
        ax3.plot(lineCount[lineCount[-1] - 200:], line3[lineCount[-1] - 200:])
        ax4.set_xlim(lineCount[-1] - 200, lineCount[-1])
        ax4.plot(lineCount[lineCount[-1] - 200:], line4[lineCount[-1] - 200:])
    if hl5_array[3][-1] < 100:
        ax5.scatter(hl5_array[0], hl5_array[1], hl5_array[2])
    ax5.scatter(hl5_array[0][hl5_array[3][-1] - 100:], hl5_array[1][hl5_array[3][-1] - 100:], hl5_array[2][hl5_array[3][-1] - 100:])
    ax5.set_xlim(-300,300)
    ax5.set_ylim(-300,300)
    ax5.set_zlim(-300,300)


s.addMsgHandler("/muse/eeg", genHandler)
s.addMsgHandler("/muse/acc", genHandler)
s.addMsgHandler("default", genHandler)
s.addMsgHandler("/error", genHandler)
s.addMsgHandler("info", genHandler)
s.addMsgHandler("/muse/elements", genHandler)

print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr

# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()

# Loop while threads are running.
ani = animation.FuncAnimation(fig, animateGraphs, interval = 250)
plt.show()
try:
    # while 1:
    #     listy = []
    #     for i in range(4):
    #          listy.append(randint(-100, 100))
    #     splitEEG(listy)
    #     # listy2 = []
        # for i in range(3):
        #     listy2.append(randint(-20,20))
        # splitACC(listy2)
    pass
except AssertionError as err:
    print "hello", str(err)

except TypeError:
    print "oops"
    exit(0)

except KeyboardInterrupt:
        print "\nClosing OSCServer."
        s.close()
        print "Waiting for Server-thread to finish"
        st.join()
        print "Done"

