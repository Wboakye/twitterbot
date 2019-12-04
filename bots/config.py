import tweepy
import logging
from boto.s3.connection import S3Connection
import os

logger = logging.getLogger()


def create_api():
    s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])
    
    consumer_key = s3.get_bucket("CONSUMER_KEY", validate=False, headers=False) 
    consumer_secret = s3.get_bucket("CONSUMER_SECRET", validate=False, headers=False)
    access_token = s3.get_bucket("ACCESS_TOKEN", validate=False, headers=False)
    access_token_secret = s3.get_bucket("ACCESS_TOKEN_SECRET", validate=False, headers=False)

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
