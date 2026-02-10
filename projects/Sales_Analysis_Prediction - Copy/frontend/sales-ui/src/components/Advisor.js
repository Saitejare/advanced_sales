import React, { useEffect, useState } from "react";
import API from "../services/api";

function Advisor() {
  const [tips, setTips] = useState([]);

  useEffect(() => {
    API.get("/advisor").then(res => setTips(res.data.insights)).catch(err => console.log(err));
  }, []);

  return (
    <div style={{ maxWidth: "800px" }}>
      <h2 style={{ marginBottom: "25px" }}>🤖 Strategic Business Advisor</h2>
      <div style={advisorContainer}>
        {tips.map((t, i) => (
          <div key={i} style={tipStyle}>
            <div style={botIcon}>AI</div>
            <div style={tipText}>{t}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

const advisorContainer = { background: "white", padding: "30px", borderRadius: "12px", boxShadow: "0 4px 6px rgba(0,0,0,0.05)" };
const tipStyle = { display: "flex", gap: "15px", marginBottom: "20px", borderBottom: "1px solid #f1f5f9", paddingBottom: "15px" };
const botIcon = { background: "#4e73df", color: "white", width: "40px", height: "40px", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold", flexShrink: 0 };
const tipText = { lineHeight: "1.6", color: "#374151" };

export default Advisor;