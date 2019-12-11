#!/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
import json
import os
from pymongo import MongoClient
import schedule
import time
import threading
from datetime import datetime

from config import create_api

tracked_words_string = os.environ.get("TRACKED_WORDS", 3)
tracked_words_list = tracked_words_string.split()

atlas_url = os.environ.get("ATLAS_URL", 3)


class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.like = False
        client = MongoClient(atlas_url)
        self.db = client.boakyeTweets
        thread = threading.Thread(target=self.dblogger, args=())
        thread.start()

    def on_status(self, tweet):
        print(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None:
            print("This tweet is a reply -- ignored")
            return
        if tweet.user.id == self.me.id:
            print("I am the author of this tweet -- ignored")
            return
        if self.like == True:
            if not tweet.favorited:
                try:
                    tweet.favorite()
                    print("Tweet liked")
                except Exception as e:
                    print("Error on like")
                    print(e)
            self.like = False
            time.sleep(65)
        else:
            if not tweet.retweeted:
                try:
                    tweet.retweet()
                    print("Tweet retweeted")
                except Exception as e:
                    print("Error on retweet")
                    print(e)
            self.like = True
            time.sleep(65)
        

    def on_error(self, status):
        print(status)

    def dblogger(self):
        print("Database Logging Thread started")
        schedule.every().day.at("00:00").do(self.screenshot)
        schedule.every().day.at("06:00").do(self.screenshot)
        schedule.every().day.at("12:00").do(self.screenshot)
        schedule.every().day.at("18:00").do(self.screenshot)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def screenshot(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = datetime.today()

        self.db.posts.insert_one({"date": current_date, "time": current_time,
                                  "tweetCount": self.me.statuses_count, "followerCount": self.me.followers_count})
        print("+-+-+-+ SCREENSHOT TAKEN +-+-+-+")


def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])


if __name__ == "__main__":
    main(tracked_words_list)
