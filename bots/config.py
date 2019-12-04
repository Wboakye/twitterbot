import tweepy
import logging
from boto.s3.connection import S3Connection
import os

logger = logging.getLogger()


def create_api():
    s3 = S3Connection(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"],
                      os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])

    consumer_key = s3[0]
    consumer_secret = s3[1]
    access_token = s3[2]
    access_token_secret = s3[3]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
