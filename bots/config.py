import tweepy
import logging
import os

logger = logging.getLogger()


def create_api():

    consumer_key = os.environ.get("CONSUMER_KEY", 3)
    consumer_secret = os.environ.get("CONSUMER_SECRET", 3)
    access_token = os.environ.get("ACCESS_TOKEN", 3)
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET", 3)

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
