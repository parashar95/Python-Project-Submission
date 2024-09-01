import streamlit as st
import pandas as pd

# Load the Excel file
file_path = "movies.xlsx"  # Update with the correct file path
df = pd.read_excel(file_path)

# UI Title with custom styling
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #4a90e2;
        text-align: center;
    }
    .header {
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    .movie-title {
        font-size: 18px;
        font-weight: bold;
    }
    .movie-details {
        font-size: 16px;
        color: #555;
    }
    .divider {
        border-top: 2px solid #ddd;
        margin: 10px 0;
    }
    </style>
    <div class="title">Movie Explorer</div>
""", unsafe_allow_html=True)

# Create two columns: left for genres, right for movie details
left_col, right_col = st.columns([1, 2])

# Extract unique genres from the DataFrame
genres = df['genres'].str.split(', ', expand=True).stack().unique()

# Initialize a list to store selected genres
selected_genres = []

# Left column: Create checkboxes for each genre
with left_col:
    st.markdown('<div class="header">Select Genres:</div>', unsafe_allow_html=True)
    for genre in genres:
        if st.checkbox(genre):
            selected_genres.append(genre)

# Right column: Display movie details based on selected genres
with right_col:
    if selected_genres:
        st.markdown(f'<div class="header">Movies in Selected Genres: {", ".join(selected_genres)}</div>', unsafe_allow_html=True)
        filtered_df = df[df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]
        
        # Display movie details
        for index, row in filtered_df.iterrows():
            st.markdown(f"""
                <div class="movie-title">{row['title']}</div>
                <div class="movie-details">Year: {row['year']} | Rating: {row['rating']}</div>
                <div class="divider"></div>
            """, unsafe_allow_html=True)
