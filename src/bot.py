
import logging
import random
import time
from typing import Optional

import praw
import tweepy
from openai import OpenAI

from .config import Settings
from .moderation import is_allowed
from .prompts import PROMPTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

settings = Settings()
settings.validate()

client = OpenAI(api_key=settings.openai_api_key) if not settings.dry_run else None


def generate_text(prompt: str) -> Optional[str]:
    if settings.dry_run:
        return f"[DRY_RUN] {prompt[:80]} ..."

    try:
        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You write short, cryptic, mysterious single-paragraph posts "
                        "(max 280 chars). Avoid unsafe content."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.9,
            max_tokens=120,
        )
        text = resp.choices[0].message.content.strip()
        if len(text) > 280:
            text = text[:277] + "..."
        ok, reason = is_allowed(text)
        if not ok:
            logging.warning(f"Moderation blocked: {reason}")
            return None
        return text
    except Exception:
        logging.exception("generate_text failed")
        return None

def post_to_reddit(text: str):
    if settings.dry_run:
        logging.info(f"[DRY_RUN] Would post to r/{settings.reddit_subreddit}: {text}")
        return

    reddit = praw.Reddit(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        username=settings.reddit_username,
        password=settings.reddit_password,
        user_agent=settings.reddit_user_agent,
    )
    try:
        subreddit = reddit.subreddit(settings.reddit_subreddit)
        subreddit.submit(title=text[:290], selftext="")
        logging.info("Posted to Reddit")
    except Exception:
        logging.exception("Reddit post failed")

def post_to_twitter(text: str):
    if settings.dry_run:
        logging.info(f"[DRY_RUN] Would tweet: {text}")
        return

    try:
        client_v2 = tweepy.Client(
            bearer_token=settings.twitter_bearer_token,
            consumer_key=settings.twitter_api_key,
            consumer_secret=settings.twitter_api_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret,
            wait_on_rate_limit=True,
        )
        client_v2.create_tweet(text=text)
        logging.info("Posted to Twitter")
    except Exception:
        logging.exception("Twitter post failed")

def main():
    logging.info("Creative Reddit + Twitter poster started...")
    while True:
        prompt = random.choice(PROMPTS)
        logging.info(f"Selected prompt: {prompt}")
        text = generate_text(prompt)
        if text:
            logging.info(f"Generated: {text}")
            post_to_reddit(text)
            post_to_twitter(text)
        else:
            logging.info("No text generated this cycle.")

        interval_hours = random.uniform(settings.min_hours, settings.max_hours)
        sleep_seconds = int(interval_hours * 3600)
        logging.info(f"Sleeping for ~{interval_hours:.2f}h ({sleep_seconds}s)...")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Stopped by user.")
