import React from "react";
import { NavCard } from "../components/NavCard";
import { ExposureHeatMap } from "../components/ExposureHeatMap";

export function Dashboard() {
  // Ironhold PM team's landing page — IRN-088.
  const demoCells = [
    { sector: "Tech", region: "US", exposure: 0.32 },
    { sector: "Tech", region: "EU", exposure: 0.08 },
    { sector: "Energy", region: "US", exposure: -0.14 },
    { sector: "Energy", region: "EU", exposure: 0.04 },
    { sector: "Financials", region: "US", exposure: 0.11 },
    { sector: "Financials", region: "EU", exposure: -0.06 },
  ];
  return (
    <main>
      <h1>Dashboard</h1>
      <section className="kpi-grid">
        <NavCard label="Portfolios" value="—" />
        <NavCard label="Total NAV" value="—" />
        <NavCard label="Gross Exposure" value="—" />
        <NavCard label="1d 99% VaR" value="—" />
      </section>
      <section>
        <h2>Exposure heat map</h2>
        <ExposureHeatMap cells={demoCells} />
      </section>
    </main>
  );
}
