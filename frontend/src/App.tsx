import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Dashboard } from "./pages/Dashboard";
import { Portfolios } from "./pages/Portfolios";
import { PositionList } from "./pages/PositionList";
import { loadTheme } from "./themes";

const CUSTOMER = import.meta.env.VITE_CUSTOMER ?? "";
const BRAND_NAME =
  CUSTOMER === "harborlight" ? "Harborlight Portal" : "Meridian Portfolio";

export function App() {
  useEffect(() => {
    loadTheme();
  }, []);
  return (
    <BrowserRouter>
      <header className="app-header">
        <span className="logo">{BRAND_NAME}</span>
      </header>
      <nav>
        <Link to="/">Dashboard</Link> | <Link to="/portfolios">Portfolios</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/portfolios" element={<Portfolios />} />
        <Route path="/portfolios/:id" element={<PositionList />} />
      </Routes>
    </BrowserRouter>
  );
}
