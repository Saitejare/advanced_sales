import React, { useEffect, useState } from "react";
import API from "../services/api";

function StockAlert() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    API.get("/stock-alert").then(res => setAlerts(res.data)).catch(err => console.log(err));
  }, []);

  return (
    <div>
      <h2 style={{ marginBottom: "25px" }}>📦 Inventory Risk Alerts</h2>
      {alerts.map((item, i) => (
        <div key={i} style={alertBox}>
          <div style={{ fontSize: "24px", marginRight: "20px" }}>⚠️</div>
          <div>
            <h4 style={{ margin: "0 0 5px 0", color: "#991b1b" }}>Critical Stock Warning</h4>
            <p style={{ margin: "0", color: "#7f1d1d" }}><b>Impacted:</b> {item.products.join(", ")}</p>
            <p style={{ margin: "5px 0 0 0", opacity: 0.8 }}>{item.message}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

const alertBox = { display: "flex", alignItems: "center", background: "#fef2f2", border: "1px solid #fee2e2", padding: "20px", borderRadius: "12px", marginBottom: "15px" };

export default StockAlert;