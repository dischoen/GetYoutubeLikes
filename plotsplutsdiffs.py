#!/usr/local/bin/python

import sqlite3
import os
import plotly
import time

py = plotly.plotly(os.getenv("PLOTLY_USER"), os.getenv("PLOTLY_KEY"))
py.ioff()
conn = sqlite3.connect('hack.db')
c = conn.cursor()

c.execute('''SELECT * FROM hack ORDER BY date''')
all = c.fetchall()
data = {}
for point in all:
    if data.has_key(point[1]):
        data[point[1]].append((point[0], point[2], point[3], point[4]))
    else:
        data[point[1]] = [(point[0], point[2], point[3], point[4])]

#------------------------------------------------------------------
def tdiff(a,b):
    ta = time.mktime(time.strptime(a,"%Y-%m-%d %H:%M:%S"))
    tb = time.mktime(time.strptime(b,"%Y-%m-%d %H:%M:%S"))
    return ta - tb

for project in data.keys():
    t = [x[0] for x in data[project]]
    v = [x[1] for x in data[project]]
    l = [x[2] for x in data[project]]
    vdiff = map(lambda x: 1.0*(x[1]-x[0])/tdiff(x[3],x[2]), zip(v,v[1:], t,t[1:]))
    ldiff = map(lambda x: 1.0*(x[1]-x[0])/tdiff(x[3],x[2]), zip(l,l[1:], t,t[1:]))
    diffdiff = map(lambda x: x[0]-x[1], zip(ldiff,vdiff))
    graph_data = [
            {
                'name': project + " views",
                'x'   : t,
                'y'   : v,
                'type': 'scatter',
                'mode': 'lines',
                'opacity': 0.85
            },
            {
                'name': project + " views diff",
                'x'   : t,
                'y'   : vdiff,
                'yaxis': 'y3',
                'type': 'scatter',
                'mode': 'lines',
                'opacity': 0.85
            },
            {
                'name': project + " likes",
                'x'   : t,
                'y'   : l,
                'yaxis': 'y2',
                'type': 'scatter',
                'mode': 'lines',
                'opacity': 0.75
            },
            {
                'name': project + " likes diff",
                'x'   : t,
                'y'   : ldiff,
                'yaxis': 'y3',
                'type': 'scatter',
                'mode': 'lines',
                'opacity': 0.75
            },
            {
                'name': project + " diff diff",
                'x'   : t,
                'y'   : diffdiff,
                'yaxis': 'y3',
                'type': 'scatter',
                'mode': 'lines',
                'opacity': 0.75
            }]

    layout = {
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Views'},
                'yaxis2': {'title': 'Likes',
                           'overlaying':'y',
                           'side':'right'},
                'yaxis3': {'title': 'Derivat',
                           'overlaying':'y',
                           'anchor': 'free',
                           'position': 0.2,
                           'side':'left'},
                'legend': {"x":0, "y":1},
                'title': "Hack The Arduino Robot Challenge 2014<br>" + project + " Views vs. Likes"
                }

    py.plot(graph_data, layout=layout,
            filename='HackTheArduinoRobot/%s Views vs Likes plus Diffs' % project, fileopt='overwrite',
        world_readable=True, width=1000, height=650)
