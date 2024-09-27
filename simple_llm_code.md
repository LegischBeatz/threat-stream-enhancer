# Documentation

## Overview

This application is a simple news analysis tool that leverages a Large Language Model (LLM) to generate insights based on cybersecurity news articles. The application fetches news articles, processes them using the LLM, and displays the results on a web page. The key components of the application are:

- **Frontend**: An HTML template (`index.html`) styled with CSS (`styles.css`) to display articles and LLM-generated insights.
- **Backend**: Python scripts (`main.py` and `llm_utils.py`) that fetch articles, interact with the LLM API, and serve data to the frontend.

---

## File Breakdown

### 1. `styles.css`

**Location**: `static/styles.css`

This CSS file defines the styling for the web application, ensuring a clean and readable interface.

#### **Content:**

```css
/* static/styles.css */

body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
}

h1, h2, h3 {
    color: #2c3e50;
}

.article {
    background-color: #fdfdfd;
    padding: 15px;
    border: 1px solid #dcdcdc;
    border-radius: 8px;
    margin-bottom: 20px;
}

.article h3 {
    margin-top: 0;
}

.article p {
    color: #34495e;
}

p {
    line-height: 1.6;
}

a {
    color: #2980b9;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
```

#### **Explanation:**

- **Body Styling**:
  - Sets a global font (`Arial`) and a light background color (`#f4f4f9`).
  - Adds padding for spacing.

- **Container**:
  - Centers content with a maximum width of 800px.

- **Headings (`h1`, `h2`, `h3`)**:
  - Uses a consistent color (`#2c3e50`) for all headings.

- **Article Styling**:
  - Creates a card-like appearance with background color, padding, borders, and rounded corners.
  - Ensures consistent spacing between articles.

- **Text Styling**:
  - Sets paragraph line height for readability.
  - Styles links with a specific color and hover effect.

---

### 2. `index.html`

**Location**: `templates/index.html`

This is the main HTML template for the web page, utilizing Jinja2 templating to dynamically display content passed from the backend.

#### **Content:**

```html
<!-- templates/index.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>News Analysis with LLM</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>News Analysis with LLM</h1>

        <!-- Display fetched articles -->
        {% for category, articles_list in articles.items() %}
            <h2>{{ category.capitalize() }} News</h2>
            {% for article in articles_list %}
                <div class="article">
                    <h3><a href="{{ article.link }}">{{ article.title }}</a></h3>
                    <p><em>Published: {{ article.published }}</em></p>
                    <p>{{ article.summary }}</p>
                </div>
            {% endfor %}
        {% endfor %}

        <!-- Display first LLM response -->
        <h2>Key Themes Identified</h2>
        <p>{{ first_response }}</p>

        <!-- Display second LLM response -->
        <h2>Insights and Predictions</h2>
        <p>{{ second_response }}</p>
    </div>
</body>
</html>
```

#### **Explanation:**

- **Head Section**:
  - Sets the page title and character encoding.
  - Links the external stylesheet using Flask's `url_for` function.

- **Body Section**:
  - Wraps content in a container for styling.
  - Displays the main heading.

- **Article Display**:
  - Iterates over `articles` (a dictionary passed from the backend) to display news articles by category.
  - For each article:
    - Displays the title as a clickable link.
    - Shows the publication date and a summary.

- **LLM Responses**:
  - Displays two sections for the LLM's outputs:
    - **Key Themes Identified**: Shows the first LLM response.
    - **Insights and Predictions**: Shows the second LLM response.

---

### 3. `llm_utils.py`

**Location**: `C:\Users\Ezio\Documents\ai_data_aggr`

This Python module contains a utility function to interact with the LLM API, sending prompts and receiving responses.

#### **Content:**

```python
# llm_utils.py

import requests
import json

LLM_API_URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}

def generate_response(prompt, model="phi3"):
    """Send a prompt to the LLM API and get the response."""
    payload = {
        "model": model,
        "prompt": prompt
    }
    response = requests.post(LLM_API_URL, json=payload, headers=HEADERS, stream=True)
    generated_text = ""

    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                json_obj = json.loads(line)
                generated_text += json_obj.get('response', '')
        return generated_text.strip()
    else:
        error_message = f"Error: Received status code {response.status_code} from LLM API."
        print(error_message)
        return error_message
```

#### **Explanation:**

- **Imports**:
  - `requests`: For making HTTP requests to the LLM API.
  - `json`: For parsing JSON responses.

- **Constants**:
  - `LLM_API_URL`: The endpoint of the LLM API (running locally).
  - `HEADERS`: HTTP headers specifying JSON content type.

- **Function `generate_response`**:
  - **Parameters**:
    - `prompt`: The text prompt to send.
    - `model`: The LLM model to use (default is `"phi3"`).
  - **Process**:
    - Constructs a JSON payload with the prompt and model.
    - Sends a POST request to the LLM API with streaming enabled.
    - If the response is successful (`status_code == 200`):
      - Iterates over streamed lines, parsing each as JSON.
      - Accumulates the `response` field from each line.
    - Returns the combined generated text.
    - Handles errors by printing and returning an error message.

#### **Usage Example**:

```python
from llm_utils import generate_response

prompt = "Explain the concept of zero-trust security."
response = generate_response(prompt)
print(response)
```

---

### 4. `main.py`

**Location**: `C:\Users\Ezio\Documents\ai_data_aggr`

This script orchestrates the application flow, utilizing `llm_utils.py` to generate LLM responses based on predefined prompts.

#### **Content:**

```python
# main.py

from llm_utils import generate_response

def main():
    # First prompt: Generate three random words
    first_prompt = "Provide a list of three random words which have to do with cybersecurity."
    first_response = generate_response(first_prompt)

    if "Error" in first_response:
        print(first_response)
        return

    print("Random Words:")
    print(first_response)
    print()

    # Second prompt: Use the words to create a short story
    second_prompt = f"Using the following words: {first_response}, write a short creative story with max. 1000 characters."
    second_response = generate_response(second_prompt)

    if "Error" in second_response:
        print(second_response)
        return

    print("Generated Story:")
    print(second_response)

if __name__ == '__main__':
    main()
```

#### **Explanation:**

- **Imports**:
  - Imports `generate_response` from `llm_utils.py`.

- **Function `main`**:
  - **First Prompt**:
    - Asks the LLM for three random cybersecurity-related words.
    - Checks for errors in the response.
    - Prints the words if successful.
  - **Second Prompt**:
    - Instructs the LLM to write a short creative story using the words from the first response.
    - Limits the story to 1000 characters.
    - Checks for errors.
    - Prints the generated story.
  - **Error Handling**:
    - If the LLM API returns an error, the script prints the error and exits.

- **Execution**:
  - The `main` function is called when the script is run directly.

#### **Usage**:

Run the script from the command line:

```bash
python main.py
```

---

## Additional Implementation Details

### Flask Application (Not Provided)

While `index.html` is designed for a Flask application, the Flask app code isn't included. To fully integrate the frontend and backend:

1. **Set Up Flask App**:
   - Create `app.py` with Flask application code.
   - Define routes to render `index.html`.

2. **Fetch and Process Articles**:
   - Use a news API or RSS feeds to fetch cybersecurity news articles.
   - Process the articles and prepare data structures to pass to the template.

3. **Generate LLM Responses**:
   - Within the Flask route, use `generate_response` to get insights from the LLM based on the articles.

4. **Render Template**:
   - Pass `articles`, `first_response`, and `second_response` to `index.html`.

**Example Flask Route**:

```python
from flask import Flask, render_template
from llm_utils import generate_response

app = Flask(__name__)

@app.route('/')
def home():
    # Fetch and process articles
    articles = fetch_articles()  # Define this function to fetch articles

    # Generate LLM responses
    first_prompt = "Analyze the following articles and identify key themes..."
    first_response = generate_response(first_prompt)

    second_prompt = "Based on the key themes, provide insights and predictions..."
    second_response = generate_response(second_prompt)

    return render_template('index.html',
                           articles=articles,
                           first_response=first_response,
                           second_response=second_response)

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Summary

- **Frontend**:
  - `styles.css`: Defines the visual styling of the web page.
  - `index.html`: Renders the articles and LLM responses dynamically using Jinja2 templating.

- **Backend**:
  - `llm_utils.py`: Provides a utility function to interact with the LLM API.
  - `main.py`: Demonstrates basic usage of `llm_utils.py` to generate prompts and handle responses.

- **Next Steps**:
  - Implement the Flask application to serve the web page.
  - Integrate news article fetching and processing.
  - Enhance error handling and logging.

---

## Notes

- **LLM API**:
  - Ensure the LLM API is running and accessible at `http://localhost:11434/api/generate`.
  - The API should accept JSON requests and stream JSON responses.

- **Dependencies**:
  - Install required Python packages:
    ```bash
    pip install requests flask
    ```

- **Error Handling**:
  - The current error handling in `llm_utils.py` and `main.py` prints errors to the console.
  - Consider logging errors and providing user-friendly messages on the frontend.

- **Security Considerations**:
  - Sanitize and validate all inputs and outputs, especially if integrating user input.
  - Secure the LLM API endpoint and restrict access as needed.

---

By following this documentation, developers can understand the structure and functionality of the application, and proceed with further development and integration.
