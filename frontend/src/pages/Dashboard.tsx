import React from "react";
import { NavCard } from "../components/NavCard";

export function Dashboard() {
  return (
    <main>
      <h1>Dashboard</h1>
      <section className="kpi-grid">
        <NavCard label="Portfolios" value="—" />
        <NavCard label="Total NAV" value="—" />
        <NavCard label="Unrealized P&amp;L" value="—" />
      </section>
    </main>
  );
}
