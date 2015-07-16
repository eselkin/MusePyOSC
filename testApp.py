#!/usr/bin/env python
import socket, OSC, re, time, threading, math

OSC_addr_cli = '127.0.0.1', 5001
OSC_addr_srv = '127.0.0.1', 5001
s = OSC.OSCServer(OSC_addr_srv)
c = OSC.OSCClient()
c.connect(OSC_addr_cli)
s.addDefaultHandlers()

def genHandler(addr, tags, stuff, source):
    if addr == "/muse/eeg":
        eeg(addr, tags, stuff, source)
    elif addr == "/muse/acc":
        acc(addr, tags, stuff, source)
    elif addr == "/error":
        err(addr, tags, stuff, source)
    elif addr == "default":
        default(addr, tags, stuff, source)
    elif addr == "/info":
        info(addr, tags, stuff, source)
    elif addr == "/muse/elements":
        elements(addr, tags, stuff, source)

def eeg(addr, tags, stuff, source):
    print "%s" % stuff

def acc(addr, tags, stuff, source):
    pass

def err(addr, tags, stuff, source):
    pass

def default(addr, tags, stuff, source):
    pass

def elements(addr, tags, stuff, source):
    pass

def info(addr, tags, stuff, source):
    pass

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
try :
    while 1 :
        time.sleep(10)
                    
except KeyboardInterrupt :
        print "\nClosing OSCServer."
        s.close()
        print "Waiting for Server-thread to finish"
        st.join()
        print "Done"

