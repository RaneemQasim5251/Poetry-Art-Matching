from flask import Flask, render_template, request, jsonify
from utils.data_processing import load_poems, load_paintings, cache_embeddings, get_model
import numpy as np


app = Flask(__name__)

# Load the datasets
poems, poem_texts = load_poems(limit=3000)
paintings = load_paintings()  # Ensure paintings dataset is correctly loaded
model = get_model()
poem_embeddings = cache_embeddings(poem_texts, "poem_embeddings.pkl")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match_poem():
    data = request.get_json()
    input_poem = data.get('poem', '')

    if not input_poem:
        return jsonify({"error": "No poem provided"}), 400

    input_embedding = model.encode([input_poem])[0]
    similarities = np.dot(poem_embeddings, input_embedding)
    best_match_idx = np.argmax(similarities)

    best_painting = paintings[best_match_idx]

    return jsonify({
        "poem": input_poem,
        "art_title": best_painting["description"],  # Adjust this based on metadata
        "artist": best_painting["artist"],
        "genre": best_painting["genre"],
        "image_url": f"/data/New_Realism/{best_painting['filename']}"
    })

if __name__ == '__main__':
    app.run(debug=True)
