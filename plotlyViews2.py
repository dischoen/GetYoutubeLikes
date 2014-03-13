#!/usr/local/bin/python

import sqlite3
import os
import plotly


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

graph_data = []
for project in data.keys():
    graph_data.append(
            {
                'name': project + " likes",
                'x'   : [x[0] for x in data[project]],
                'y'   : [x[2] for x in data[project]],
                'text': ["Likes: %s" % x[2] for x in data[project]],
                'type': 'scatter',
                'mode': 'lines',
                'opacity': 0.25
            })

layout = {
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Views'},
            'title': "Hack The Arduino Robot Challenge 2014<br>Likes"
            }

py.plot(graph_data, layout=layout,
        filename='HackTheArduinoRobot/Likes', fileopt='overwrite',
        world_readable=True, width=1000, height=650)


#------------------------------------------------------------------

graph_data = []
for project in data.keys():
    graph_data.append(
            {
                'name': project + " views",
                'x'   : [x[0] for x in data[project]],
                'y'   : [x[1] for x in data[project]],
                'text': ["Views: %s" % x[1] for x in data[project]],
                'type': 'scatter',
                'mode': 'lines',
                'opacity': 0.25
            })

layout = {
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Views'},
            'title': "Hack The Arduino Robot Challenge 2014<br>Views"
            }

py.plot(graph_data, layout=layout,
        filename='HackTheArduinoRobot/Views', fileopt='overwrite',
        world_readable=True, width=1000, height=650)

#------------------------------------------------------------------

for project in data.keys():
    graph_data = [
            {
                'name': project + " views",
                'x'   : [x[0] for x in data[project]],
                'y'   : [x[1] for x in data[project]],
                'text': ["Views: %s" % x[1] for x in data[project]],
                'type': 'scatter',
                'mode': 'lines',
                'opacity': 0.25
            },
            {
                'name': project + " likes",
                'x'   : [x[0] for x in data[project]],
                'y'   : [x[2] for x in data[project]],
                'text': ["Likes: %s" % x[2] for x in data[project]],
                'yaxis': 'y2',
                'type': 'scatter',
                'mode': 'lines',
                'opacity': 0.45
            }]

    layout = {
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Views'},
                'yaxis2': {'title': 'Likes',
                           'overlaying':'y',
                           'side':'right'},
                'title': "Hack The Arduino Robot Challenge 2014<br>" + project + " Views vs. Likes"
                }

    py.plot(graph_data, layout=layout,
            filename='HackTheArduinoRobot/%s Views vs Likes' % project, fileopt='overwrite',
        world_readable=True, width=1000, height=650)
