GetYoutubeLikes
===============

For HackTheArduinoRobot, this scripts get the current likes on Youtube and plot them on plot.ly

## getLikes.sh
this script fetches the playlist contents and then iterates over the items in it.
it fetches viewCount, likeCount and dislikeCount for every item.
the results are sappended to an sqlite DB.

## plotlyViews2.py
this script fetches the contents of the DB and uploads them to plot.ly.
it creates several charts:
one plot for the views of all projects
one plot for the likes of all projects
and one plot for each project with views and likes

## prerequisites
You need a youtube data API key to access the data from youtube,
and you need to register to plot.ly to upload plots there.

See result at
https://plot.ly/plot
