import React, { useEffect, useState } from "react";
import { apiGet } from "../api/client";

type Row = {
  household_id: string;
  household_name: string;
  account_count: number;
  total_nav: string;
};

// Advisor landing page for Harborlight — HBL-096.
export function Households() {
  const [rows, setRows] = useState<Row[]>([]);
  useEffect(() => {
    apiGet<Row[]>("/households").then(setRows).catch(() => setRows([]));
  }, []);
  return (
    <main>
      <h1>Households</h1>
      <table>
        <thead>
          <tr>
            <th>Household</th>
            <th>Accounts</th>
            <th>Total NAV</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.household_id}>
              <td>{r.household_name}</td>
              <td>{r.account_count}</td>
              <td>{r.total_nav}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
