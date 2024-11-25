import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
import pickle
import smtplib
from email.message import EmailMessage

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

""" SAMPLE USAGE """
metadata_path = './csv/movies.csv'
tfidf_matrix_path = './pkl/tfidf_matrix.pkl'
input_title = "The Office"

recommendations = get_content_based_recommendations(input_title, metadata_path, tfidf_matrix_path, top_n=3)
print(f"Recommendations for '{input_title}': {recommendations}")

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
    Recommendation System
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

recipient_email = 'recipient@example.com'
sender_email = 'your_email@example.com'
sender_password = 'your_email_password'

send_recommendation_email(recommendations, recipient_email, sender_email, sender_password)

