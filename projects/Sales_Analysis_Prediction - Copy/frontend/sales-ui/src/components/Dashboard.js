import React, { useEffect, useState } from "react";
import API from "../services/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, LineChart, Line, PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    API.get("/analytics")
      .then(res => setData(res.data))
      .catch(err => console.log(err));
  }, []);

  if (!data) return <div style={loaderStyle}><h3>Loading Intelligence...</h3></div>;

  const monthlyData = Object.keys(data.monthly_sales).map(m => ({
    month: `Month ${m}`,
    sales: data.monthly_sales[m]
  }));

  const regionData = Object.keys(data.region_sales).map(r => ({
    name: r,
    value: data.region_sales[r]
  }));

  const COLORS = ["#4e73df", "#1cc88a", "#f6c23e", "#e74a3b"];
  const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(val);

  return (
    <div>
      <h2 style={{ marginBottom: "30px", fontWeight: "700" }}>Sales Analytics Overview</h2>

      <div style={{ display: "flex", gap: "25px", marginBottom: "40px" }}>
        <div style={kpiCard("#4e73df")}>
          <span>Total Sales</span>
          <h3>{formatCurrency(data.total_sales)}</h3>
        </div>
        <div style={kpiCard("#1cc88a")}>
          <span>Total Profit</span>
          <h3>{formatCurrency(data.total_profit)}</h3>
        </div>
        <div style={kpiCard("#36b9cc")}>
          <span>Total Customers</span>
          <h3>{data.customers.toLocaleString()}</h3>
        </div>
      </div>

      <div style={chartRow}>
        <div style={chartCard("65%")}>
          <h4 style={{ marginBottom: "20px" }}>📈 Monthly Sales Trend</h4>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#eee" />
              <XAxis dataKey="month" axisLine={false} tickLine={false} />
              <YAxis axisLine={false} tickLine={false} />
              <Tooltip />
              <Line type="monotone" dataKey="sales" stroke="#4e73df" strokeWidth={3} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={chartCard("32%")}>
          <h4 style={{ marginBottom: "20px" }}>🌍 Sales by Region</h4>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={regionData} dataKey="value" nameKey="name" outerRadius={100} innerRadius={60} paddingAngle={5}>
                {regionData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

const kpiCard = (color) => ({
  flex: 1, background: "white", padding: "20px", borderRadius: "12px", borderLeft: `5px solid ${color}`, boxShadow: "0 4px 6px rgba(0,0,0,0.05)"
});
const chartCard = (width) => ({ width, background: "white", padding: "25px", borderRadius: "12px", boxShadow: "0 4px 6px rgba(0,0,0,0.05)" });
const chartRow = { display: "flex", justifyContent: "space-between", gap: "20px" };
const loaderStyle = { height: "80vh", display: "flex", alignItems: "center", justifyContent: "center" };

export default Dashboard;