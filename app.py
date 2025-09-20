# app.py v1.0 - Basic Flask web app for sentiment analysis
# Why Flask? Lightweight, easy for beginners. Routes handle requests; templates for UI.
# Learning: Web flow—user submits form (POST), server processes, renders response.

from flask import Flask, render_template, request
from fetch_data import fetch_posts
from sentiment_analysis import aggregate_sentiments

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        subreddit = request.form.get('subreddit', 'all')  # Default 'all'
        limit = int(request.form.get('limit', 10))
        posts = fetch_posts(keyword, subreddit, limit)
        if posts:
            agg = aggregate_sentiments(posts)
            return render_template('index.html', agg=agg, keyword=keyword, subreddit=subreddit)
        else:
            return render_template('index.html', error="No posts found.")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)  # Debug mode for dev; remove for production