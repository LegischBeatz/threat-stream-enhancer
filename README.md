# Threat Stream Enhancer

An interactive web application built using [Dash](https://dash.plotly.com/) that fetches news articles from predefined RSS feeds and generates social media posts based on user-selected prompts.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Steps](#setup-steps)
- [Running the Application](#running-the-application)
- [Application Structure](#application-structure)
  - [app.py](#apppy)
  - [assets/](#assets)
    - [base.html](#basehtml)
    - [style.css](#stylecss)
- [Functionalities](#functionalities)
  - [News Categories](#news-categories)
  - [Number of Articles](#number-of-articles)
  - [Prompt Types](#prompt-types)
  - [Fetching Articles](#fetching-articles)
  - [Generating Social Media Posts](#generating-social-media-posts)
  - [Copying Content](#copying-content)
- [Code Explanation](#code-explanation)
  - [Importing Libraries](#importing-libraries)
  - [Initializing the App](#initializing-the-app)
  - [Caching Setup](#caching-setup)
  - [RSS Feeds](#rss-feeds)
  - [Prompts](#prompts)
  - [Fetching RSS Data](#fetching-rss-data)
  - [App Layout](#app-layout)
  - [Callbacks](#callbacks)
    - [Updating News Content](#updating-news-content)
    - [Copying to Clipboard](#copying-to-clipboard)
  - [Running the Server](#running-the-server)
- [Customization](#customization)
  - [Adding New RSS Feeds](#adding-new-rss-feeds)
  - [Adding New Prompt Types](#adding-new-prompt-types)
  - [Modifying the HTML Template](#modifying-the-html-template)
  - [Modifying the CSS](#modifying-the-css)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Credits and Acknowledgments](#credits-and-acknowledgments)

## Introduction

**Threat Stream Enhancer** is an interactive web application designed to fetch news articles from predefined RSS feeds and generate social media posts based on user-selected prompts. The application allows users to select a news category, specify the number of articles to fetch, choose a prompt type for generating social media content, and easily copy the generated content for use on social media platforms.

## Features

- Fetch news articles from predefined RSS feeds in **Cybersecurity News** and **General World News** categories.
- Generate social media posts based on five different prompt types:
  - Satirical Post
  - Serious Post
  - Breaking News Post
  - Trending Post
  - News Essay Post
- Customize the number of articles to fetch from each RSS feed.
- Interactive user interface built with Dash and styled with custom HTML and CSS.
- Ability to copy the generated content to the clipboard for easy sharing.

## Installation

### Prerequisites

- Python 3.7 or higher
- Pip (Python package installer)

### Setup Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/my-dash-app.git
   cd my-dash-app
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   **Note:** If `requirements.txt` is not available, install the necessary packages manually:

   ```bash
   pip install dash flask-caching feedparser
   ```

## Running the Application

1. **Start the Dash App**

   ```bash
   python app.py
   ```

2. **Access the Application in Your Browser**

   Open your web browser and navigate to `http://0.0.0.0:5000` or `http://localhost:5000`.

   **Note:** The app is set to run in debug mode. For production deployment, set `debug=False` and consider using a production server like Gunicorn.

## Application Structure

```
my-dash-app/
├── app.py
├── assets/
│   ├── base.html
│   └── style.css
├── requirements.txt
└── README.md
```

### app.py

The main application file containing the Dash app logic, layout, and callbacks.

### assets/

Contains static assets like the HTML template and CSS files.

#### base.html

Custom HTML template used by Dash to render the application with a consistent layout and styling.

#### style.css

Custom CSS file for styling the application, overriding default Dash styles.

## Functionalities

### News Categories

Users can select from two news categories:

- **Cybersecurity News**
- **General World News**

Each category has a predefined list of RSS feeds.

### Number of Articles

Users can specify the number of articles to fetch from each RSS feed. The default is set to **3** articles per feed.

### Prompt Types

Users can choose from five different prompt types for generating social media content:

1. **Satirical Post**: Creates catchy, satirical social media posts with witty and humorous headlines.
2. **Serious Post**: Crafts engaging headlines and brief summaries focusing on key facts.
3. **Breaking News Post**: Writes bold, attention-grabbing headlines highlighting urgent aspects.
4. **Trending Post**: Summarizes key points with captivating headlines suitable for trending topics.
5. **News Essay Post**: Generates comprehensive yet social-media-friendly posts.

### Fetching Articles

Clicking the **Fetch Articles** button triggers the application to:

- Fetch the specified number of articles from the selected news category's RSS feeds.
- Generate social media posts based on the selected prompt type.

### Generating Social Media Posts

The application compiles the fetched articles and generates social media posts using the selected prompt. The generated content includes:

- Title
- Description/Summary
- Published Date
- Source
- URL

### Copying Content

After the content is generated, users can click the **Copy Content** button to copy the generated social media posts to the clipboard for easy sharing.

## Code Explanation

### Importing Libraries

```python
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import feedparser
from flask_caching import Cache
from urllib.parse import urlparse
```

- **dash**: Main library for building Dash applications.
- **feedparser**: Parses RSS feed data.
- **flask_caching**: Provides caching mechanisms to improve performance.
- **urllib.parse**: Parses URLs to extract domain names.

### Initializing the App

```python
app = dash.Dash(__name__, suppress_callback_exceptions=True, title="Threat Stream Enhancer")
app.index_string = open('./assets/base.html', 'r').read()
server = app.server
```

- **suppress_callback_exceptions**: Allows for callbacks referencing IDs not yet present in the layout.
- **app.index_string**: Sets a custom HTML template.

### Caching Setup

```python
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp/cache-directory',
    'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes
})
```

- Caches fetched RSS data to reduce load times and limit network requests.

### RSS Feeds

Defines RSS feeds for both news categories.

```python
RSS_FEEDS = {
    'cybersecurity': [
        "https://news.ycombinator.com/rss",
        "https://www.infosecurity-magazine.com/rss/news/",
        ...
    ],
    'general': [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "https://feeds.bbci.co.uk/news/rss.xml",
        ...
    ]
}
```

### Prompts

Defines various prompts for generating social media content.

```python
prompts = {
    'satirical': "...",
    'serious': "...",
    ...
}
```

### Fetching RSS Data

```python
@cache.memoize()
def fetch_rss_data(category, article_count):
    ...
```

- Fetches and parses RSS feed data.
- Extracts title, summary, link, published date, and source.
- Caches the results to improve performance.

### App Layout

Defines the structure of the user interface.

```python
app.layout = html.Div([
    dcc.Store(id='stored-content'),
    html.H1("Interactive News Fetcher"),
    html.Div([...]),  # News category selection
    html.Div([...]),  # Article count input
    html.Div([...]),  # Prompt type selection
    html.Button('Fetch Articles', id='submit-button', n_clicks=0),
    html.Div(id="news-content"),
    html.Button('Copy Content', id='copy-button', n_clicks=0),
    html.Div(id='copy-status')
])
```

- **dcc.Store**: Stores data on the client-side for sharing between callbacks.
- **html.H1**, **html.Div**, **html.Label**, **dcc.Dropdown**, **dcc.Input**, **html.Button**: Dash components for building the UI.

### Callbacks

#### Updating News Content

```python
@app.callback(
    Output("news-content", "children"),
    Output('stored-content', 'data'),
    [Input('submit-button', 'n_clicks')],
    [State('news-category', 'value'),
     State('article-count', 'value'),
     State('prompt-type', 'value')]
)
def update_news(n_clicks, selected_category, article_count, selected_prompt_type):
    ...
```

- Triggered when the **Fetch Articles** button is clicked.
- Fetches articles and generates content based on user selections.
- Updates the UI with the generated content and stores it for copying.

#### Copying to Clipboard

```python
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
```

- A client-side callback written in JavaScript.
- Copies the generated content to the clipboard when **Copy Content** is clicked.
- Updates the copy status message.

### Running the Server

```python
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=5000, debug=True)
```

- Starts the Dash server.
- **host='0.0.0.0'**: Makes the app accessible on the local network.
- **port=5000**: The port number to run the app on.
- **debug=True**: Enables debug mode for development.

## Customization

### Adding New RSS Feeds

To add new RSS feeds:

1. Open `app.py`.
2. Locate the `RSS_FEEDS` dictionary.
3. Add new feed URLs to the desired category or create a new category.

```python
RSS_FEEDS = {
    'cybersecurity': [
        ...,
        "https://new-cybersecurity-feed.com/rss"
    ],
    'general': [
        ...,
    ],
    'technology': [  # New category example
        "https://techcrunch.com/feed/",
        "https://thenextweb.com/feed/"
    ]
}
```

4. If a new category is added, update the dropdown options in the app layout.

```python
dcc.Dropdown(
    id="news-category",
    options=[
        {'label': 'Cybersecurity News', 'value': 'cybersecurity'},
        {'label': 'General World News', 'value': 'general'},
        {'label': 'Technology News', 'value': 'technology'}  # New category
    ],
    value='cybersecurity',
    clearable=False
)
```

### Adding New Prompt Types

To add new prompt types:

1. Open `app.py`.
2. Locate the `prompts` dictionary.
3. Add a new key-value pair for the prompt.

```python
prompts = {
    ...,
    'informal': """
Create an informal, conversational social media post using the provided articles.
For each article, write a friendly headline and a brief, engaging summary under 520 characters.
Include the article URL for readers to learn more.
"""
}
```

4. Update the prompt type dropdown in the app layout.

```python
dcc.Dropdown(
    id="prompt-type",
    options=[
        ...,
        {'label': 'Informal Post', 'value': 'informal'}
    ],
    value='news_essay',
    clearable=False
)
```

### Modifying the HTML Template

The HTML template is located at `assets/base.html`.

- Modify the `<head>` section to include additional meta tags or external stylesheets.
- Update the `<body>` to change the layout, header, footer, or add new elements.
- Use Dash placeholders like `{%app_entry%}`, `{%config%}`, `{%scripts%}`, and `{%renderer%}` to ensure proper rendering.

### Modifying the CSS

The CSS file is located at `assets/style.css`.

- Update styles for existing classes or elements.
- Add new styles to customize the appearance.
- Remember that Dash automatically serves CSS files located in the `assets/` directory.

## Troubleshooting

- **Issue:** Application doesn't start.
  - **Solution:** Ensure all dependencies are installed. Check for any typos or syntax errors in the code.
- **Issue:** No articles are fetched.
  - **Solution:** Verify that the RSS feed URLs are correct and accessible. Check internet connectivity.
- **Issue:** Content is not copied to clipboard.
  - **Solution:** Ensure that your browser allows clipboard operations from JavaScript. Some browsers may restrict this for security reasons.
- **Issue:** CSS styles are not applied.
  - **Solution:** Ensure the CSS file is correctly named (`style.css`) and located in the `assets/` directory.

## License

This project is licensed under the [MIT License](LICENSE).

## Credits and Acknowledgments

- Developed using [Dash](https://dash.plotly.com/) by Plotly.
- RSS feeds provided by respective news outlets.
- Inspired by the need for quick generation of social media content based on current news.
