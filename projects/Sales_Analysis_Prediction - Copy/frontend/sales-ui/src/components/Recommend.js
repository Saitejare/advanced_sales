import React, { useEffect, useState } from "react";
import API from "../services/api";

function Recommend() {
  const [list, setList] = useState([]);

  useEffect(() => {
    API.get("/recommend").then(res => setList(res.data)).catch(err => console.log(err));
  }, []);

  return (
    <div>
      <h2 style={{ marginBottom: "25px" }}>🛒 Market Basket Recommendations</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(350px, 1fr))", gap: "20px" }}>
        {list.map((item, i) => (
          <div key={i} style={recCard}>
            <div style={badge}>Confidence: {(item.confidence * 100).toFixed(0)}%</div>
            <p style={{ color: "#666", marginBottom: "5px" }}>Customers who bought:</p>
            <p style={{ fontWeight: "700", color: "#1a1c23" }}>{item.buy.join(", ")}</p>
            <div style={arrow}>⬇️ Often also buy ⬇️</div>
            <p style={{ fontWeight: "700", color: "#4e73df", fontSize: "1.1rem" }}>{item.recommend.join(", ")}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

const recCard = { background: "white", padding: "20px", borderRadius: "12px", boxShadow: "0 4px 6px rgba(0,0,0,0.05)", position: "relative" };
const badge = { position: "absolute", top: "20px", right: "20px", background: "#f0fdf4", color: "#166534", padding: "4px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "bold" };
const arrow = { margin: "15px 0", fontSize: "12px", color: "#9ca3af", textAlign: "center" };

export default Recommend;