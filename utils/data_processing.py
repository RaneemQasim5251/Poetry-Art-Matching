import os
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
import torch
import random

# Load SentenceTransformer model
def get_model():
    """Load the SentenceTransformer model."""
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    if torch.cuda.is_available():
        model = model.to('cuda')
    return model

# Load Arabic poems and shuffle
def load_poems(limit=3000):
    """Load a large number of random Arabic poems."""
    from datasets import load_dataset
    print("📖 Loading Arabic poems dataset...")
    dataset = load_dataset("arbml/ashaar", split="train")
    poems, poem_texts = [], []

    indices = random.sample(range(len(dataset)), min(limit, len(dataset)))

    for idx in indices:
        item = dataset[idx]
        verses = item.get("poem verses", [])
        text = " ".join(verses) if isinstance(verses, list) else verses or ""
        poet_name = item.get("poet name", "")
        full_text = f"{text} {poet_name}"
        poems.append({
            "poem_title": item.get("poem title", ""),
            "poem_verses": verses,
            "poet_name": poet_name,
        })
        poem_texts.append(full_text)

    print(f"Loaded {len(poems)} diverse Arabic poems.")
    return poems, poem_texts

# Compute embeddings
def compute_poem_embeddings(model, texts):
    """Compute embeddings for a list of texts."""
    return model.encode(texts, batch_size=128, show_progress_bar=True, convert_to_tensor=True)

# Cache embeddings
def cache_embeddings(model, texts, cache_file="poem_embeddings3.pkl"):
    """Cache embeddings to avoid recomputation."""
    try:
        with open(cache_file, "rb") as f:
            embeddings = pickle.load(f)
            print(f"✅ Loaded embeddings from cache: {cache_file}")
    except FileNotFoundError:
        print("💾 Computing embeddings...")
        embeddings = compute_poem_embeddings(model, texts)
        with open(cache_file, "wb") as f:
            pickle.dump(embeddings, f)
    return embeddings

# Load paintings with metadata

def load_paintings(csv_path="data/classes.csv"):
    """
    Load paintings metadata from a CSV file.
    :param csv_path: Path to the CSV file containing painting metadata.
    :return: List of paintings with metadata.
    """
    try:
        df = pd.read_csv(csv_path)
        paintings = df.to_dict(orient="records")  # Convert DataFrame to list of dictionaries
        return paintings
    except FileNotFoundError:
        print(f"Error: The file {csv_path} was not found.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

