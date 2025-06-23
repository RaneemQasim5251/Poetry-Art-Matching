import React, { useState } from "react";
import axios from "axios";
import { gsap } from "gsap";
import TextTransition, { presets } from "react-text-transition";
import "./App.css";

const App = () => {
  const [poem, setPoem] = useState("");
  const [matchedArt, setMatchedArt] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleMatch = async () => {
    if (!poem.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/match", { poem });
      setMatchedArt(response.data);
      animateUI();
    } catch (error) {
      console.error("Error fetching match:", error);
    } finally {
      setLoading(false);
    }
  };

  const animateUI = () => {
    gsap.fromTo(".art-container", { opacity: 0 }, { opacity: 1, duration: 1.5 });
    gsap.fromTo(".poem-text", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 1.2 });
  };

  return (
    <div className="app">
      <div className="header">
        <h1 className="title">🎨 Poetic Vision 🌌</h1>
        <p className="subtitle">Enter an Arabic poem, and we'll find the perfect painting for it.</p>
      </div>

      <textarea
        className="poem-input"
        placeholder="اكتب القصيدة هنا..."
        value={poem}
        onChange={(e) => setPoem(e.target.value)}
      />

      <button className="match-btn" onClick={handleMatch} disabled={loading}>
        {loading ? "Matching..." : "Find the Art ✨"}
      </button>

      {matchedArt && (
        <div className="result">
          <div className="art-container">
            <img src={matchedArt.image_url} alt="Matching Artwork" className="art-image" />
            <div className="overlay">
              <h2 className="poem-text">
                <TextTransition springConfig={presets.wobbly}>{matchedArt.poem}</TextTransition>
              </h2>
              <p className="artist">{matchedArt.artist}</p>
              <p className="genre">{matchedArt.genre}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
