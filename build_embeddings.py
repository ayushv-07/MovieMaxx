import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

print("Loading dataset...")
df = pd.read_csv("IMDB-Movie-Data-Extended.csv")

df = df.dropna(subset=["Description"]).reset_index(drop=True)
descriptions = df["Description"].fillna("").astype(str).tolist()

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")
embeddings = model.encode(
    descriptions,
    convert_to_tensor=True,
    show_progress_bar=True
)

torch.save(embeddings, "embeddings.pt")
df.to_pickle("movies.pkl")

print("✅ Done!")