import React from "react";

export function NavCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="nav-card">
      <div className="nav-card__label">{label}</div>
      <div className="nav-card__value">{value}</div>
    </div>
  );
}
