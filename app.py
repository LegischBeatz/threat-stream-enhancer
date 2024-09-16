import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import feedparser
from flask_caching import Cache
from urllib.parse import urlparse

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, title="My Dash App")

# Use base.html as the template
app.index_string = open('./assets/base.html', 'r').read()

server = app.server

# Initialize caching
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp/cache-directory',
    'CACHE_DEFAULT_TIMEOUT': 300  # Cache timeout in seconds (5 minutes)
})

# Define RSS feeds for Cybersecurity News and General World News
RSS_FEEDS = {
    'cybersecurity': [
        "https://news.ycombinator.com/rss",
        "https://www.infosecurity-magazine.com/rss/news/",
        "https://krebsonsecurity.com/feed/",
        "https://nakedsecurity.sophos.com/feed/",
        "https://www.schneier.com/blog/index.rdf",
        "https://threatpost.com/feed/"
    ],
    'general': [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://www.theguardian.com/world/rss"
    ]
}

# Prompts for generating social media content
prompts = {
    'satirical': """
Create catchy, satirical social media posts using the provided news articles.
For each article, generate a witty and humorous headline that critiques or pokes fun at the subject in a lighthearted way.
Keep the tone entertaining and shareable, while avoiding offensive material. Limit the content to 520 characters or less.
Include the URL for each original article at the end for readers to follow the full story.
""",
    'serious': """
Create punchy, serious news posts for social media from the provided articles.
For each article, craft an engaging headline and a brief summary focusing on the key facts or updates.
Make the content clear, direct, and shareable in 520 characters or less.
Add the URL for each original article to allow readers to explore the full story.
""",
    'breaking_news': """
Create a breaking news-style post for social media using the provided articles.
For each article, write a bold and attention-grabbing headline that highlights the most urgent or shocking aspect of the news.
Summarize the core of the story in a concise, engaging way that can fit within 520 characters.
Include the URL for each original article so readers can follow for more details.
""",
    'trend_summary': """
Create trending topic posts for Instagram or Facebook using the provided articles.
For each article, summarize the key points with a captivating headline and a brief description that will catch the reader’s attention in under 520 characters.
Make sure the post is visually engaging and shareable, and include a URL to the original news article for more information.
""",
    'news_essay': """
Create a comprehensive yet social-media-friendly news post using the provided articles.
For each article, generate a quick but insightful headline and a 520 characters description focusing on the main news angles.
Make it suitable for both Twitter and Facebook, linking to the original article for users to read more.
Keep it concise and actionable in 280 characters or less.
"""
}

# Default number of articles to fetch
default_article_count = 3

@cache.memoize()
def fetch_rss_data(category, article_count):
    articles = []
    feeds = RSS_FEEDS.get(category)
    if not feeds:
        return articles  # Return empty list if category not found

    for url in feeds:
        try:
            # Extract domain name from URL for the source name
            domain = urlparse(url).netloc.replace('www.', '')
            feed = feedparser.parse(url)

            for entry in feed.entries[:article_count]:
                articles.append({
                    "title": entry.get("title", "No Title"),
                    "summary": entry.get("description", "No Description"),
                    "link": entry.link,
                    "published": entry.get("published", "Unknown Date"),
                    "source": domain
                })
        except Exception as e:
            print(f"Error fetching or parsing feed {url}: {e}")
            continue  # Skip this feed and continue with others
    return articles

# Layout of the Dash app
app.layout = html.Div([
    dcc.Store(id='stored-content'),  # Store for content to be copied

    html.H1("Interactive News Fetcher"),

    html.Div([
        html.Label("Select news category:"),
        dcc.Dropdown(
            id="news-category",
            options=[
                {'label': 'Cybersecurity News', 'value': 'cybersecurity'},
                {'label': 'General World News', 'value': 'general'}
            ],
            value='cybersecurity',
            clearable=False
        ),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("Enter number of articles per feed:"),
        dcc.Input(
            id="article-count",
            type="number",
            value=default_article_count,
            min=1,
            step=1
        ),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("Select prompt type:"),
        dcc.Dropdown(
            id="prompt-type",
            options=[
                {'label': 'Satirical Post', 'value': 'satirical'},
                {'label': 'Serious Post', 'value': 'serious'},
                {'label': 'Breaking News Post', 'value': 'breaking_news'},
                {'label': 'Trending Post', 'value': 'trend_summary'},
                {'label': 'News Essay Post', 'value': 'news_essay'}
            ],
            value='news_essay',
            clearable=False
        ),
    ], style={'margin-bottom': '20px'}),

    html.Button('Fetch Articles', id='submit-button', n_clicks=0),

    html.Div(id="news-content", style={'margin-top': '20px'}),

    # Add a button to copy content to clipboard
    html.Button('Copy Content', id='copy-button', n_clicks=0),
    
    # Display copy status
    html.Div(id='copy-status', style={'margin-top': '10px'})
])

# Callback to update the news content when the user clicks the submit button
@app.callback(
    Output("news-content", "children"),
    Output('stored-content', 'data'),  # Store the generated content for copying
    [Input('submit-button', 'n_clicks')],
    [State('news-category', 'value'),
     State('article-count', 'value'),
     State('prompt-type', 'value')]
)
def update_news(n_clicks, selected_category, article_count, selected_prompt_type):
    if n_clicks and n_clicks > 0:
        # Validate article_count
        try:
            article_count = int(article_count)
            if article_count <= 0:
                article_count = default_article_count
        except (ValueError, TypeError):
            article_count = default_article_count

        articles = fetch_rss_data(selected_category, article_count)

        if not articles:
            return html.Div("No articles found."), None

        # Get the correct prompt type
        prompt = prompts.get(selected_prompt_type, prompts['serious'])

        # Generate the article content
        article_text = "\n".join([
            f"**Title:** {article['title']}\n"
            f"**Description:** {article['summary']}\n"
            f"**Published:** {article['published']}\n"
            f"**Source:** {article['source']}\n"
            f"**URL:** {article['link']}\n"
            for article in articles
        ])

        # Combine prompt and article content
        combined_content = f"{prompt}\n\n{article_text}"

        return html.Div([
            html.H2("Generated Social Media Post"),
            html.Pre(combined_content, style={
                'wordWrap': 'break-word',
                'overflowX': 'auto'
            })
        ]), combined_content  # Return content to be stored in `dcc.Store`
    
    return html.Div("Click 'Fetch Articles' to view news."), None


# Callback to copy content to clipboard
app.clientside_callback(
    """
    function(n_clicks, content) {
        if (n_clicks > 0 && content) {
            const el = document.createElement('textarea');
            el.value = content;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
            return "Content copied!";
        }
        return "";
    }
    """,
    Output('copy-status', 'children'),
    [Input('copy-button', 'n_clicks')],
    [State('stored-content', 'data')]
)

# Run the Dash app
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=5000, debug=True)
