#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Generating timeline.json ----
# (with thanks to examples from https://github.com/bear/python-twitter)
from __future__ import print_function
import json
import sys
import twitter
import t

# Function to get tweets from python-twitter API
def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline

api = twitter.Api(
    t.consumerKey, t.consumerSecret, t.accessTokenKey, t.accessTokenSecret
)
screen_name = t.twitterHandle
print(screen_name)
tlfile = get_tweets(api=api, screen_name=screen_name)

# Write all tweets into a json in the `app` subdirectory
with open('app/timeline.json', 'w+') as f:
    for tweet in tlfile:
        f.write(json.dumps(tweet._json))
        f.write('\n')


# Importing timeline json ----
# Get all the tweet dicts into one list
# (with thanks to https://stackoverflow.com/a/47958749)
def json_readr(file):
    for line in open(file, mode="r"):
        yield json.loads(line)
timeline = list(json_readr("app/timeline.json"))


# Remove irrelevant tweets ----
# Only looking at those with: (a) media, AND (b) hashtag #NintendoSwitch
for i in range(0, len(timeline)):
    hashtaglist= timeline[i]["entities"]["hashtags"]
    hashtags = []
    for j in range(0, len(hashtaglist)):
        hashtags.append(hashtaglist[j]["text"])
    if "extended_entities" not in list(timeline[i]): #if has media
        timeline[i] = "null"
    if "NintendoSwitch" not in hashtags: #only want things with #NintendoSwitch
        timeline[i] = "null"
while "null" in timeline: #remove anything we marked in the loop above
    timeline.remove("null")


# Get date/time from metadata ----
def twitterDate(dateIn):
    year = dateIn[26:30]
    month = dateIn[4:7]
    day = dateIn[8:10]
    hour = dateIn[11:13]
    minute = dateIn[14:16]
    second = dateIn[17:19]
    return dict(year = year, month = month, day = day,
                hour = hour, minute = minute, second = second)


# URL/filename for each item ----
URL = []
metadate = []
for i in range(0, len(timeline)):
    x = timeline[i]["extended_entities"]["media"] #list of all media attached
    for j in range(0, len(x)):
        mediaType = x[j]["type"] #photo or video?
        
        if mediaType == "video":
            bitR = [] #grab the highest resolution version of video
            for k in range(0, len(x[j]["video_info"]["variants"])):
                variant = x[j]["video_info"]["variants"][k]
                if "bitrate" in list(variant):
                    bitR.append(variant["bitrate"])
                    if bitR[-1] == max(bitR):
                        photoURL = variant["url"]
                        downloadFlag = True
            if downloadFlag:
                URL.append(photoURL)
                metadate.append(twitterDate(timeline[i]["created_at"]))
        
        elif mediaType == "photo":
            photoURL = x[j]["media_url_https"]
            URL.append(photoURL)
            metadate.append(twitterDate(timeline[i]["created_at"]))


# Duplicate removal ----
# Read in the duplicate log as list "duplicates"
f = open("app/duplicates.txt", "r")
duplicates = f.readlines()
for i in range(0, len(duplicates)): #remove the "\n" from end of each line
    duplicates[i] = duplicates[i][0:-1]
f.close()

# Remove duplicates
for i in range(0, len(URL)):
    if URL[i] in duplicates:
        URL[i] = "null"
        metadate[i] = "null"
while "null" in URL:
    URL.remove("null")
while "null" in metadate:
    metadate.remove("null")

# Append new stuff to duplicate log (so we don't do it next time)
f = open("app/duplicates.txt", "a")
for x in URL:
    f.write(str(x) + "\n")
f.close()


# Upload new media to Google Photos ----
if len(URL) > 0:
    import wget
    import subprocess
    for i in range(0, len(URL)):
        x = URL[i]
        y = metadate[i]
        photoCreated = y["year"] + y["month"] + y["day"] + "." + \
                    y["hour"] + y["minute"] + "." + y["second"]
        if x[8:11] == "pbs":
            extension = x[-4:]
            #print("Downloaded photo " + "/media/" + photoCreated + extension)
            wget.download(x, "media/Switch/" + photoCreated + extension)
        elif x[8:11] == "vid":
            #print("Downloaded video " + "/media/" + photoCreated + ".mp4")
            wget.download(x, "media/Switch/" + photoCreated + ".mp4")
    subprocess.run(["app/gphotos-uploader-cli", "push"])
