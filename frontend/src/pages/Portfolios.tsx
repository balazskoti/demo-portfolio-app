import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet } from "../api/client";

type Row = { id: string; name: string };

export function Portfolios() {
  const [rows, setRows] = useState<Row[]>([]);
  useEffect(() => {
    apiGet<Row[]>("/portfolios").then(setRows).catch(() => setRows([]));
  }, []);
  return (
    <main>
      <h1>Portfolios</h1>
      <ul>
        {rows.map((r) => (
          <li key={r.id}>
            <Link to={`/portfolios/${r.id}`}>{r.name}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
