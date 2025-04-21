import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiGet } from "../api/client";

type Valuation = {
  portfolio_id: string;
  nav: string;
  positions: Array<{
    instrument_id: string;
    quantity: string;
    price: string;
    market_value: string;
    unrealized_pnl: string;
    weight: string;
  }>;
};

export function PositionList() {
  const { id = "" } = useParams();
  const [data, setData] = useState<Valuation | null>(null);
  useEffect(() => {
    apiGet<Valuation>(`/portfolios/${id}/valuation`).then(setData);
  }, [id]);
  if (!data) return <p>Loading…</p>;
  return (
    <main>
      <h1>Positions</h1>
      <p>NAV: {data.nav}</p>
      <table>
        <thead>
          <tr>
            <th>Instrument</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Market Value</th>
            <th>Unrealized P&amp;L</th>
            <th>Weight</th>
          </tr>
        </thead>
        <tbody>
          {data.positions.map((p) => (
            <tr key={p.instrument_id}>
              <td>{p.instrument_id}</td>
              <td>{p.quantity}</td>
              <td>{p.price}</td>
              <td>{p.market_value}</td>
              <td>{p.unrealized_pnl}</td>
              <td>{p.weight}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
