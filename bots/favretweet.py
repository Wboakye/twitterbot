#!/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
from config import create_api
import json
import os
from pymongo import MongoClient
from crontab import CronTab
from datetime import datetime


tracked_words_string = os.environ.get("TRACKED_WORDS", 3)
tracked_words_list = tracked_words_string.split()

atlas_url = os.environ.get("ATLAS_URL", 3)


class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        client = MongoClient(atlas_url)
        self.db = client.boakyeTweets
        self.dblogger()

    def on_status(self, tweet):
        print(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                print("Error on like: ")
                print(e.message[0])
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                print("Error on retweet: ")
                print(e.message[0])

    def on_error(self, status):
        print(status)

    def dblogger(self):
        cron = CronTab()
        job = cron.new(command=self.screenshot())
        job.hour.on(0)
        job.hour.also.on(6)
        job.hour.also.on(12)
        job.hour.also.on(18)

    def screenshot(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # Fix this v
        current_date = datetime.today()

        self.db.posts.insert_one({"date": current_date, "time": current_time,
                                  "tweetCount": self.me.statuses_count, "followerCount": self.me.followers_count})


def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])


if __name__ == "__main__":
    main(tracked_words_list)
