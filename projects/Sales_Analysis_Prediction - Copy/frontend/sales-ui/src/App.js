import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import Predict from "./components/Predict";
import Recommend from "./components/Recommend";
import Advisor from "./components/Advisor";
import StockAlert from "./components/StockAlert";

function App() {
  return (
    <BrowserRouter>
      <div style={layoutStyle}>
        {/* Sidebar */}
        <nav style={sidebarStyle}>
          <div style={logoStyle}>📊 BizIntel Pro</div>
          <NavLink to="/" style={navLinkStyle} className={({isActive}) => isActive ? "active-link" : ""}>🏠 Dashboard</NavLink>
          <NavLink to="/predict" style={navLinkStyle}>🔮 Sales Predictor</NavLink>
          <NavLink to="/recommend" style={navLinkStyle}>🛒 Recommendations</NavLink>
          <NavLink to="/advisor" style={navLinkStyle}>🤖 AI Advisor</NavLink>
          <NavLink to="/stock" style={navLinkStyle}>⚠️ Stock Alerts</NavLink>
        </nav>

        {/* Main Content */}
        <main style={mainContentStyle}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/recommend" element={<Recommend />} />
            <Route path="/advisor" element={<Advisor />} />
            <Route path="/stock" element={<StockAlert />} />
          </Routes>
        </main>
      </div>

      <style>{`
        .active-link { background: #4e73df !important; color: white !important; }
        a:hover { background: rgba(255,255,255,0.1); }
      `}</style>
    </BrowserRouter>
  );
}

const layoutStyle = { display: "flex", minHeight: "100vh" };
const sidebarStyle = { width: "260px", background: "#1a1c23", padding: "20px", display: "flex", flexDirection: "column", position: "fixed", height: "100vh", zIndex: 100 };
const logoStyle = { color: "white", fontSize: "1.5rem", fontWeight: "700", marginBottom: "40px", textAlign: "center", letterSpacing: "1px" };
const mainContentStyle = { marginLeft: "260px", padding: "40px", width: "calc(100% - 260px)", minHeight: "100vh" };
const navLinkStyle = { color: "#9ca3af", padding: "12px 16px", textDecoration: "none", borderRadius: "8px", marginBottom: "8px", fontWeight: "500", transition: "0.2s" };

export default App;