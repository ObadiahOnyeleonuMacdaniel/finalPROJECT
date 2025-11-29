import streamlit as st              # import Streamlit for creating the web app
import pandas as pd                 # import pandas for handling CSV data
import requests                     # import requests to make API calls (HTTP requests)
import re                           # import regex module for matching review HTML patterns
from bs4 import BeautifulSoup       # import BeautifulSoup for scraping reviews from web pages
import plotly.graph_objs as go      # import Plotly for interactive charts

# Streamlit App Title
st.write("""
# Sentiments Analysis App ✌
""")  # Display the app title in markdown format on the main page

# Display introductory description of what sentiment analysis is
st.write('Sentiment analysis is the interpretation and classification of emotions (positive, negative and neutral) within text data using text analysis techniques. Sentiment analysis tools allow businesses to identify customer sentiment toward products, brands or services in online feedback.')

# Sidebar section for user input
st.sidebar.header('User Input(s)')  # Add header to sidebar

# Case 1: Single Review input from the sidebar
st.sidebar.subheader('Single Review Analysis')  # Subheader for single review
single_review = st.sidebar.text_input('Enter single review below:')  # Input text box for one review

# Case 2: Scrape Yelp reviews
st.sidebar.subheader('Scrape Reviews from Yelp')  # Subheader for Yelp scraping
scrape_url = st.sidebar.text_input("Enter the business URL:")  # Input box to paste Yelp URL

# Case 3: CSV file upload option
st.sidebar.subheader('Multiple Reviews Analysis')  # Subheader for multiple reviews
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])  # Upload CSV file with reviews
# Initialize counters for sentiment counts
count_positive = 0
count_negative = 0
count_neutral = 0

# ---- Case 1: CSV upload ----
if uploaded_file is not None:  # Check if a CSV file is uploaded
    input_df = pd.read_csv(uploaded_file)  # Read CSV file into a pandas DataFrame

    # Loop through each row (review) in the DataFrame
    for i in range(input_df.shape[0]):
        review_text = str(input_df.iloc[i, 0])   # Take the first column as the review text
        url = 'https://aisentimentsanalyzer.herokuapp.com/classify/?text=' + review_text  # API endpoint with review
        r = requests.get(url)  # Send GET request to sentiment API
        result = r.json()["text_sentiment"]  # Extract sentiment result from API response

        # Count sentiment types
        if result == 'positive':
            count_positive += 1
        elif result == 'negative':
            count_negative += 1
        else:
            count_neutral += 1

    # Prepare data for bar chart
    x = ["Positive", "Negative", "Neutral"]  # Labels
    y = [count_positive, count_negative, count_neutral]  # Values

    # Feedback message depending on which sentiment dominates
    if count_positive > count_negative:
        st.write("""# Great Work there! Majority of people liked your product 😃""")
    elif count_negative > count_positive:
        st.write("""# Try improving your product! Majority of people didn't find your product up to the mark 😔""")
    else:
        st.write("""# Good Work there, but there's room for improvement! Majority of people have neutral reactions 😶""")

    # Create and display bar chart
    layout = go.Layout(
        title='Multiple Reviews Analysis (CSV)',   # Title for chart
        xaxis=dict(title='Category'),              # X-axis label
        yaxis=dict(title='Number of reviews'),     # Y-axis label
    )
    fig = go.Figure(data=[go.Bar(name='CSV Reviews', x=x, y=y)], layout=layout)  # Create figure with bar chart
    st.plotly_chart(fig, use_container_width=True)  # Render chart in Streamlit

# ---- Case 2: Single review ----
elif single_review:  # If user entered a single review manually
    url = 'https://aisentimentsanalyzer.herokuapp.com/classify/?text=' + single_review  # API call for single review
    r = requests.get(url)  # Send GET request
    result = r.json()["text_sentiment"]  # Extract sentiment from API response

    # Show result message based on sentiment
    if result == 'positive':
        st.write("""# Great Work there! You got a Positive Review 😃""")
    elif result == 'negative':
        st.write("""# Try improving your product! You got a Negative Review 😔""")
    else:
        st.write("""# Good Work there, but there's room for improvement! You got a Neutral Review 😶""")

# ---- Case 3: Scrape from Yelp ----
elif scrape_url:  # If a Yelp URL is provided
    r = requests.get(scrape_url)  # Send GET request to the Yelp page
    soup = BeautifulSoup(r.text, "html.parser")  # Parse HTML content using BeautifulSoup

    # Extract reviews (search for <p> tags with class names containing "comment")
    regex = re.compile(".*comment.*")  # Regex to match any class containing "comment"
    results = soup.find_all("p", {"class": regex})  # Find all matching <p> elements
    reviews = [result.text.strip() for result in results]  # Extract and clean review text

    # Display number of reviews found
    st.write(f"### Found {len(reviews)} reviews on the page.")

    if len(reviews) == 1:  # If only one review is found
        review = reviews[0]  # Take that single review
        url = 'https://aisentimentsanalyzer.herokuapp.com/classify/?text=' + review  # API call
        r = requests.get(url)
        result = r.json()["text_sentiment"]

        # Display feedback for single scraped review
        if result == 'positive':
            st.write("""# Great Work there! You got a Positive Review 😃""")
        elif result == 'negative':
            st.write("""# Try improving your product! You got a Negative Review 😔""")
        else:
            st.write("""# Good Work there, but there's room for improvement! You got a Neutral Review 😶""")

    elif len(reviews) > 1:  # If multiple reviews are found
        # Loop through all scraped reviews and classify
        for review in reviews:
            url = 'https://aisentimentsanalyzer.herokuapp.com/classify/?text=' + review
            r = requests.get(url)
            result = r.json()["text_sentiment"]

            # Count sentiments
            if result == 'positive':
                count_positive += 1
            elif result == 'negative':
                count_negative += 1
            else:
                count_neutral += 1

        # Prepare chart data
        x = ["Positive", "Negative", "Neutral"]
        y = [count_positive, count_negative, count_neutral]

        # Feedback message based on counts
        if count_positive > count_negative:
            st.write("""# Great Work there! Majority of people liked your product 😃""")
        elif count_negative > count_positive:
            st.write("""# Try improving your product! Majority of people didn't find your product up to the mark 😔""")
        else:
            st.write("""# Good Work there, but there's room for improvement! Majority of people have neutral reactions 😶""")

        # Create and display bar chart
        layout = go.Layout(
            title='Scraped Yelp Reviews Analysis',
            xaxis=dict(title='Category'),
            yaxis=dict(title='Number of reviews'),
        )
        fig = go.Figure(data=[go.Bar(name='Yelp Reviews', x=x, y=y)], layout=layout)
        st.plotly_chart(fig, use_container_width=True)

# ---- Default ----
else:  # If no input is provided yet
    st.write("# ⬅ Enter user input from the sidebar to analyze reviews.")
