from typing import Any, Dict, List
from dotenv import load_dotenv

import os
import tweepy
import tweepy.errors

from src.connection import trends_collection
from src.constants import BRAZIL_WOE_ID


def _get_trends(woe_id: int, api: tweepy.API) -> List[Dict[str, Any]]:
    """Get treending topics from Twitter API.

    Args:
        woe_id (int): Identifier of location.

    Returns:
        List[Dict[str, Any]]: Trends list.
    """
    # Free version does not let you fetch data from X(twitter) anymore
    try:
        trends = api.get_place_trends(woe_id)
    except tweepy.errors.Forbidden as e:
        # Mocking a value to develop the project asked by the expert
        trends = [
            {
                "trends": [
                    {"name": "#EPJuliette", "url": "http://twitter.com/search?q=%23EPJuliette"},
                    {"name": "Addison", "url": "http://twitter.com/search?q=Addison"},
                ]
            }
        ]

    return trends[0]["trends"]


def get_trends() -> List[Dict[str, Any]]:
    """Get treending topics persisted in MongoDB.

    Args:
        woe_id (int): Identifier of location.

    Returns:
        List[Dict[str, Any]]: Trends list.
    """
    trends = trends_collection.find({})
    return list(trends)


def save_trends() -> None:
    """Get trends topics and save on MongoDB."""
    load_dotenv()

    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    trends = _get_trends(woe_id=BRAZIL_WOE_ID, api=api)
    trends_collection.insert_many(trends)
