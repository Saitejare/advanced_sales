import React, { useState } from "react";
import API from "../services/api";

function Predict() {
  const [form, setForm] = useState({});
  const [result, setResult] = useState(null);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = () => {
    API.post("/predict", form).then(res => setResult(res.data)).catch(() => alert("Error"));
  };

  return (
    <div style={{ maxWidth: "900px" }}>
      <h2 style={{ marginBottom: "25px" }}>🔮 Sales Prediction Engine</h2>
      <div style={formGrid}>
        {["profit", "discount", "quantity", "year", "month", "is_weekend", "customer_orders", "product_demand"].map(field => (
          <div key={field} style={{ display: "flex", flexDirection: "column" }}>
            <label style={labelStyle}>{field.replace("_", " ").toUpperCase()}</label>
            <input name={field} placeholder={`Enter ${field}...`} onChange={handleChange} style={inputStyle} />
          </div>
        ))}
        <button onClick={submit} style={btnStyle}>Generate Forecast</button>
      </div>

      {result && (
        <div style={resultCard}>
          <h4 style={{ marginTop: 0 }}>Prediction Results</h4>
          <div style={{ display: "flex", justifyContent: "space-around" }}>
            <p><b>Estimated Sales:</b> {result.sales}</p>
            <p><b>Demand Level:</b> {result.demand}</p>
            <p><b>Profit Forecast:</b> {result.profit}</p>
          </div>
        </div>
      )}
    </div>
  );
}

const formGrid = { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", background: "white", padding: "30px", borderRadius: "12px", boxShadow: "0 4px 6px rgba(0,0,0,0.05)" };
const inputStyle = { padding: "12px", borderRadius: "8px", border: "1px solid #ddd", marginTop: "5px", outline: "none" };
const labelStyle = { fontSize: "12px", fontWeight: "600", color: "#666" };
const btnStyle = { gridColumn: "1 / -1", padding: "14px", background: "#4e73df", color: "white", border: "none", borderRadius: "8px", fontWeight: "600", cursor: "pointer", marginTop: "10px" };
const resultCard = { marginTop: "30px", padding: "25px", background: "#eef2ff", borderRadius: "12px", border: "1px solid #4e73df" };

export default Predict;