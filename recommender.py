import streamlit as st
import pandas as pd
import torch
import torch.nn.functional as F


@st.cache_resource
def load_resources():
    # Load saved dataset
    df = pd.read_pickle("movies.pkl")

    # Load saved embeddings
    embeddings = torch.load(
        "embeddings.pt",
        map_location="cpu"
    )

    # Normalize ONCE
    embeddings = F.normalize(embeddings, p=2, dim=1)

    # Create title index
    indices = pd.Series(
        df.index,
        index=df["Title"]
    ).drop_duplicates()

    return df, embeddings, indices


df, embeddings, indices = load_resources()


def recommend(movie_name):

    if movie_name not in indices:
        return pd.DataFrame()

    idx = indices[movie_name]

    # Fast cosine similarity using dot product
    cosine_scores = torch.matmul(
        embeddings,
        embeddings[idx]
    )

    # Get top 6
    top_results = torch.topk(
        cosine_scores,
        k=6
    )

    movie_indices = top_results.indices.cpu().numpy()

    # Remove the selected movie
    movie_indices = [
        i for i in movie_indices
        if i != idx
    ][:5]

    return df.iloc[movie_indices]