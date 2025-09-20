# fetch_data.py v1.2 - Fetch Reddit posts using PRAW for sentiment analysis (secure + JSON save)
# Changes from v1.1: Added save_to_json() for persisting fetched posts to file.
# Why? Allows offline reuse, avoids repeated API calls (respects rate limits/ethics).
# Learning: JSON serializes Python dicts/lists; use for data exchange/storage.

import praw
import os
from dotenv import load_dotenv
import json  # Built-in, for JSON handling

load_dotenv()

def authenticate_reddit():
    # (Unchanged from v1.1)
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD")
    )
    return reddit

def fetch_posts(keyword, subreddit="all", limit=10):
    # (Unchanged from v1.1)
    reddit = authenticate_reddit()
    posts = []
    try:
        for submission in reddit.subreddit(subreddit).search(keyword, limit=limit):
            text = submission.title + " " + submission.selftext
            posts.append({"text": text})
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

def save_to_json(posts, filename="fetched_posts.json"):
    """
    Saves the list of posts to a JSON file.
    Args: posts (list of dicts), filename (str)
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)  # Pretty-print for readability
        print(f"Saved {len(posts)} posts to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

# Test the functions
if __name__ == "__main__":
    keyword = "AI"
    subreddit = "all"
    posts = fetch_posts(keyword, subreddit=subreddit, limit=5)
    print(f"Fetched {len(posts)} posts for '{keyword}' from r/{subreddit}:")
    for post in posts:
        print(post['text'][:100] + "...")
    
    # New: Save to JSON for persistence
    if posts:  # Only save if fetched successfully
        save_to_json(posts)