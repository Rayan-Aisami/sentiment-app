# fetch_data.py v1.1 - Fetch Reddit posts using PRAW for sentiment analysis (secure version)
# Changes from v1.0: Use environment variables for credentials to avoid hardcoding secrets.
# Why? Prevents exposing passwords in code/Git. Load from .env file via python-dotenv.
# Learning: Env vars are like hidden config—code references them, but values are external.

import praw  # For Reddit API
import os    # Built-in, for accessing env vars
from dotenv import load_dotenv  # Loads .env file

# Load .env file (call this early)
load_dotenv()

def authenticate_reddit():
    """
    Authenticates with Reddit API using env vars from .env.
    Returns a Reddit instance for querying.
    """
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD")
    )
    return reddit

def fetch_posts(keyword, subreddit="all", limit=10):
    """
    Fetches posts from a subreddit containing the keyword.
    Args: keyword (str), subreddit (str, e.g., 'news' or 'all'), limit (int)
    Returns: list of dicts [{'text': 'post title and body'}, ...]
    """
    reddit = authenticate_reddit()
    posts = []
    try:
        # Search subreddit for keyword, get top results (or use .hot()/.new() for alternatives)
        for submission in reddit.subreddit(subreddit).search(keyword, limit=limit):
            text = submission.title + " " + submission.selftext  # Combine title and body
            posts.append({"text": text})
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []  # Fallback empty list

# Test the functions
if __name__ == "__main__":
    keyword = "AI"  # Test keyword; in app, this will be user input
    subreddit = "all"  # 'all' searches across Reddit; try 'technology' for specific
    posts = fetch_posts(keyword, subreddit=subreddit, limit=5)
    print(f"Fetched {len(posts)} posts for '{keyword}' from r/{subreddit}:")
    for post in posts:
        print(post['text'][:100] + "...")  # Print truncated for console; full in app