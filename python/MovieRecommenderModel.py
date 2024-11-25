import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def preprocess_and_save_cbf_data(metadata_csv, output_metadata_path, output_tfidf_path):
    """Preprocess metadata and save TF-IDF matrix and metadata for CBF."""
    # Load metadata
    metadata_df = pd.read_csv(metadata_csv)
    metadata_df['listed_in'] = metadata_df['listed_in'].fillna("")  # Handle missing categories
    metadata_df['title'] = metadata_df['title'].str.lower()  # Normalize movie/show titles

    # Create TF-IDF matrix for the 'listed_in' attribute
    tfidf = TfidfVectorizer(stop_words='english')  # Remove common words (stop words)
    tfidf_matrix = tfidf.fit_transform(metadata_df['listed_in'])  # Compute TF-IDF matrix

    # Save the metadata and TF-IDF matrix
    metadata_df.to_csv(output_metadata_path, index=False)  # Save metadata
    with open(output_tfidf_path, 'wb') as f:
        pickle.dump(tfidf_matrix, f)  # Save TF-IDF matrix

    print(f"Metadata saved to {output_metadata_path}")
    print(f"TF-IDF matrix saved to {output_tfidf_path}")

# Train and Save Model
preprocess_and_save_cbf_data("./csv/movies.csv", "./csv/movies.csv", "tfidf_matrix.pkl")
