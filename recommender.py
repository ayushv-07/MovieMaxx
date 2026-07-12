import streamlit as st
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

@st.cache_resource
def load_resources():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    df = pd.read_pickle("movies.pkl")
    embeddings = torch.load("embeddings.pt", map_location="cpu")

    indices = pd.Series(df.index, index=df["Title"]).drop_duplicates()

    return model, df, embeddings, indices

model, df, embeddings, indices = load_resources()

def recommend(movie_name):
    if movie_name not in indices:
        return pd.DataFrame()

    idx = indices[movie_name]

    # Compare the selected movie with all others
    cosine_scores = util.cos_sim(embeddings[idx], embeddings)[0]

    # Get top 6 (including itself)
    top_results = torch.topk(cosine_scores, k=6)

    movie_indices = top_results.indices.cpu().numpy()

    # Remove the selected movie
    movie_indices = [i for i in movie_indices if i != idx][:5]

    return df.iloc[movie_indices]