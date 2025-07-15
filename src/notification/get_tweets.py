import os
from typing import Optional

from src.db_function.readonly_db import connect_readonly
from tweety.types import Tweet

from src.notification.date_comparator import date_comparator


async def get_tweets(tweets: list[Tweet], username: str) -> Optional[list[Tweet]]:

    async with connect_readonly(os.path.join(os.getenv('DATA_PATH'), 'tracked_accounts.db')) as db:
        async with db.execute('SELECT lastest_tweet FROM user WHERE username = ?', (username,)) as cursor:
            row = await cursor.fetchone()
            last_tweet_at = row[0]

    tweets = [tweet for tweet in tweets if tweet.author.username == username and date_comparator(tweet.created_on, last_tweet_at) == 1]

    if tweets != []:
        return sorted(tweets, key=lambda x: x.created_on)
    else:
        return None
