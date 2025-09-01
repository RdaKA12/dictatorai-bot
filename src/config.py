import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    # Reddit
    reddit_client_id: str = os.getenv("REDDIT_CLIENT_ID", "")
    reddit_client_secret: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    reddit_username: str = os.getenv("REDDIT_USERNAME", "")
    reddit_password: str = os.getenv("REDDIT_PASSWORD", "")
    reddit_user_agent: str = os.getenv(
        "REDDIT_USER_AGENT",
        "python:DictatorAiApp:1.0 (by /u/yourname)",
    )
    reddit_subreddit: str = os.getenv("REDDIT_SUBREDDIT", "")
    # Twitter (X)
    twitter_bearer_token: str = os.getenv("TWITTER_BEARER_TOKEN", "")
    twitter_api_key: str = os.getenv("TWITTER_API_KEY", "")
    twitter_api_secret: str = os.getenv("TWITTER_API_SECRET", "")
    twitter_access_token: str = os.getenv("TWITTER_ACCESS_TOKEN", "")
    twitter_access_token_secret: str = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
    # Scheduling
    min_hours: float = float(os.getenv("POST_INTERVAL_MIN_HOURS", "2"))
    max_hours: float = float(os.getenv("POST_INTERVAL_MAX_HOURS", "3"))
    # Modes
    dry_run: bool = os.getenv("DRY_RUN", "1") == "1"
    # Moderation
    moderation_on: bool = os.getenv("MODERATION", "1") == "1"
    moderation_model: str = os.getenv("MODERATION_MODEL", "omni-moderation-latest")
    blocklist_words: str = os.getenv("BLOCKLIST_WORDS", "")

    def validate(self):
        if self.min_hours <= 0 or self.max_hours < self.min_hours:
            raise ValueError("Invalid interval hours. Check POST_INTERVAL_* in .env")
        if not self.dry_run:
            missing = []
            if not self.openai_api_key:
                missing.append("OPENAI_API_KEY")
            for k, v in {
                "REDDIT_CLIENT_ID": self.reddit_client_id,
                "REDDIT_CLIENT_SECRET": self.reddit_client_secret,
                "REDDIT_USERNAME": self.reddit_username,
                "REDDIT_PASSWORD": self.reddit_password,
                "REDDIT_USER_AGENT": self.reddit_user_agent,
                "REDDIT_SUBREDDIT": self.reddit_subreddit,
            }.items():
                if not v:
                    missing.append(k)
            for k, v in {
                "TWITTER_BEARER_TOKEN": self.twitter_bearer_token,
                "TWITTER_API_KEY": self.twitter_api_key,
                "TWITTER_API_SECRET": self.twitter_api_secret,
                "TWITTER_ACCESS_TOKEN": self.twitter_access_token,
                "TWITTER_ACCESS_TOKEN_SECRET": self.twitter_access_token_secret,
            }.items():
                if not v:
                    missing.append(k)
            if missing:
                raise ValueError("Missing env vars: " + ", ".join(missing))
