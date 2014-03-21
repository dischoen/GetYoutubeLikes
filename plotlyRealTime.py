#!/usr/local/bin/python

import os
import plotly
import random
import datetime
import time

puser = os.getenv("PLOTLY_USER")
pkey  = os.getenv("PLOTLY_KEY")
pskey = os.getenv("PLOTLY_STREAMING_KEY")

p = plotly.plotly(puser,pkey,verbose=True)
p.ioff()

#------------------------------------------------------------------

#p.plot([{'x':[], 'y':[], 'type':'scatter', 'mode':'lines','stream':{'token':pskey, 'maxpoints':500}}],
        #filename='time1', fileopt='overwrite')
p.plot([{'x':[], 'y':[], 'type':'scatter', 'mode':'lines','stream':{'token':pskey, 'maxpoints':500}}],
        filename='time2', fileopt='extend')


s = plotly.stream(pskey)
i=0
k=5
while True:
    i+=1
    print i
    xdp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ydp = random.random()
    s.write({'x': xdp, 'y':ydp})
    time.sleep(1)
    if i == 60:
        break
s.close()
