import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
import pickle
import smtplib
from email.message import EmailMessage
import sqlite3
import os
import time

# NOTE: MIGHT NOT WORK IF GIVEN TITLE IS NOT FOUND IN THE CSV FILE
def get_content_based_recommendations(title, metadata_path, tfidf_matrix_path, top_n=3):
    """Generate content-based recommendations based on the listed_in attribute."""
    # Load metadata and TF-IDF matrix
    metadata_df = pd.read_csv(metadata_path)
    with open(tfidf_matrix_path, 'rb') as f:
        tfidf_matrix = pickle.load(f)

    # Normalize the title for matching
    title = title.lower()

    # Find the index of the movie/show with the given title
    if title not in metadata_df['title'].values:
        raise ValueError(f"Title '{title}' not found in metadata.")

    idx = metadata_df[metadata_df['title'] == title].index[0]

    # Compute cosine similarity scores between the input title and all other items
    cosine_similarities = linear_kernel(tfidf_matrix[idx:idx + 1], tfidf_matrix).flatten()

    # Get indices of the top_n most similar items (excluding itself)
    similar_indices = cosine_similarities.argsort()[-top_n - 1:-1][::-1]

    # Retrieve the titles of the recommended items
    recommendations = metadata_df.iloc[similar_indices]['title'].tolist()

    return recommendations

""" SAMPLE USAGE
metadata_path = 'C:/Users/ducky/Documents/GitHubProjects/unix-project/python/csv/netflix_data.csv'
tfidf_matrix_path = 'C:/Users/ducky/Documents/GitHubProjects/unix-project/python/pkl/tfidf_matrix.pkl'
input_title = "The Night Shift"
recommendations = get_content_based_recommendations(input_title, metadata_path, tfidf_matrix_path, top_n=3)
print(f"Recommendations for '{input_title}': {recommendations}")
"""

def fetch_watch_history(db_path):
    """Fetch watch history from MyVideos75.db."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    query = """
    SELECT strTitle, lastPlayed
    FROM files
    WHERE lastPlayed IS NOT NULL
    ORDER BY lastPlayed DESC;
    """
    
    cursor.execute(query)
    watch_history = cursor.fetchall()
    connection.close()

    return watch_history

""" SAMPLE USAGE 
db_path = '/path/to/MyVideos75.db'
watch_history = fetch_watch_history(db_path)
for title, last_played in watch_history:
    print(f"Watched: {title}, Last Played: {last_played}")
"""

def send_recommendation_email(recommendations, recipient_email, sender_email, sender_password):
    """Send recommendations via email."""
    # Creates the email message
    msg = EmailMessage()
    msg['Subject'] = 'Your Recommendations Are Here!'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Formats the recommendations
    recommendations_list = '\n'.join(recommendations)
    email_body = f"""
    Hello,

    Based on your input, here are the top recommendations for you:

    {recommendations_list}

    Enjoy watching!

    Best regards,
    Ryan Dong and Yakin Succes
    """
    msg.set_content(email_body)

    # Sends the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

""" SAMPLE USAGE
recipient_email = 'recipient@example.com'
sender_email = 'your_email@example.com'
sender_password = 'your_email_password'
send_recommendation_email(recommendations, recipient_email, sender_email, sender_password)
"""

def monitor_kodi_and_recommend(db_path, metadata_path, tfidf_matrix_path, recipient_email, sender_email, sender_password):
    """Monitor Kodi for Netflix closure and send recommendations."""
    while True:
        # Check if Kodi is running
        kodi_running = "kodi" in os.popen("pgrep kodi").read()
        
        if not kodi_running:
            print("Kodi is not running. Fetching recommendations...")
            
            # Fetch watch history and get recommendations
            watch_history = fetch_watch_history(db_path)
            if watch_history:
                latest_title = watch_history[0][0]  # Most recently watched title
                try:
                    recommendations = get_content_based_recommendations(latest_title, metadata_path, tfidf_matrix_path)
                    send_recommendation_email(recommendations, recipient_email, sender_email, sender_password)
                except Exception as e:
                    print(f"Error generating or sending recommendations: {e}")
            else:
                print("No watch history found.")
            
            break  # Exit monitoring loop after handling Kodi closure
        else:
            time.sleep(10)  # Check every 10 seconds

""" SAMPLE USAGE 
db_path = '/path/to/MyVideos75.db'
metadata_path = './csv/movies.csv'
tfidf_matrix_path = './pkl/tfidf_matrix.pkl'
recipient_email = 'recipient@example.com'
sender_email = 'your_email@example.com'
sender_password = 'your_email_password'
monitor_kodi_and_recommend(db_path, metadata_path, tfidf_matrix_path, recipient_email, sender_email, sender_password)
"""