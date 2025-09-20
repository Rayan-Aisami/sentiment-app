# sentiment_analysis.py v1.0 - NLP for sentiment on Reddit posts
# Why VADER? Rule-based, fast, tuned for social media (handles slang/emojis). Scores: compound (-1 negative to +1 positive).
# Learning: Preprocessing reduces noise; aggregation turns individual scores into summaries. Later, try transformers for advanced.

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json  # For loading saved posts
from fetch_data import fetch_posts  # Import to reuse fetching (optional; or load JSON)

# Initialize VADER (global for efficiency)
sia = SentimentIntensityAnalyzer()

def preprocess_text(text):
    """
    Basic preprocessing: Lowercase, but minimal since VADER handles punctuation/caps.
    Args: text (str)
    Returns: cleaned text (str)
    """
    # Add more if needed: e.g., remove URLs with regex (import re; re.sub(r'http\S+', '', text))
    return text.lower()  # Simple for now

def analyze_sentiment(text):
    """
    Analyzes sentiment with VADER.
    Args: text (str)
    Returns: dict {'label': 'positive/negative/neutral', 'score': compound float}
    """
    cleaned = preprocess_text(text)
    scores = sia.polarity_scores(cleaned)  # Returns {'neg', 'neu', 'pos', 'compound'}
    compound = scores['compound']
    if compound > 0.05:
        label = 'positive'
    elif compound < -0.05:
        label = 'negative'
    else:
        label = 'neutral'
    return {'label': label, 'score': compound}

def aggregate_sentiments(posts):
    """
    Aggregates results: Counts and percentages.
    Args: posts (list of dicts with 'text')
    Returns: dict {'positive': count, 'negative': count, 'neutral': count, 'percentages': {...}}
    """
    results = {'positive': 0, 'negative': 0, 'neutral': 0}
    analyzed = []
    for post in posts:
        if post.get('text'):  # Skip empty
            sentiment = analyze_sentiment(post['text'])
            results[sentiment['label']] += 1
            analyzed.append({**post, 'sentiment': sentiment})
    total = len(analyzed)
    percentages = {k: (v / total * 100) if total > 0 else 0 for k, v in results.items()}
    return {'counts': results, 'percentages': percentages, 'analyzed_posts': analyzed}

# Test function
if __name__ == "__main__":
    # Option 1: Fetch fresh (uses API)
    # keyword = "AI"
    # posts = fetch_posts(keyword, limit=5)
    
    # Option 2: Load from JSON (offline, reuse Step 3 save)
    try:
        with open('fetched_posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except FileNotFoundError:
        print("No fetched_posts.json—run fetch_data.py first.")
        posts = []

    if posts:
        agg = aggregate_sentiments(posts)
        print("Aggregated Sentiments:")
        print(agg['counts'])
        print(agg['percentages'])
        # Example output: {'positive': 2, 'negative': 1, 'neutral': 2}, {'positive': 40.0, ...}
    else:
        print("No posts to analyze.")