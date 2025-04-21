import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Dashboard } from "./pages/Dashboard";
import { Portfolios } from "./pages/Portfolios";
import { PositionList } from "./pages/PositionList";

export function App() {
  return (
    <BrowserRouter>
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
