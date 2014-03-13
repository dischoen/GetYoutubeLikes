#!/bin/sh

cd /home/dieter/git/PendelBot/getLikes

. ./API.keys

DB=hack.db

if [ ! -f $DB ]; then
    sqlite3 $DB "create table hack (date integer, title text(40), views integer, likes integer, dislikes integer);"
fi

playListId=PLqnIaXrARxXFHhD5_r8dAfbx-_D3hkWBA

wget -O list.json "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=10&playlistId=$playListId&key=$APIkey" 2> list.json.wget
for videoId in $(grep "videoId" list.json | cut -f2 -d: | sed 's/"//g'); do
    wget -O vid_${videoId}.json "https://www.googleapis.com/youtube/v3/videos?part=statistics%2Csnippet&id=$videoId&key=$APIkey" 2>vid_${videoId}.json.wget
    #print
    title=$(grep '"title"' vid_${videoId}.json | cut -f2 -d: | sed -e 's/"//g' -e 's/,$//' -e 's/Hack the Arduino Robot [cC]ompetition - //' -e 's/^ *//')
    views=$(grep '"viewCount"' vid_${videoId}.json | cut -f2 -d: | sed -e 's/"//g' -e 's/,$//')
    likes=$(grep '"likeCount"' vid_${videoId}.json | cut -f2 -d: | sed -e 's/"//g' -e 's/,$//')
    dislikes=$(grep '"dislikeCount"' vid_${videoId}.json | cut -f2 -d: | sed -e 's/"//g' -e 's/,$//')
    printf "%40s   views:%5s likes:%5s dislikes:%5s\n" "$title" $views $likes $dislikes
    sqlite3 $DB "insert into hack (date,title,views,likes,dislikes) values (datetime('now'), '$title', $views, $likes, $dislikes);"
done

# save for debugging or offline analysis
newd=$(date +"%Y%m%d.%H%M%S")
mkdir $newd
mv *.json $newd
mv *.wget $newd


./plotlyViews2.py
