import React from "react";

type Cell = { sector: string; region: string; exposure: number };

export function ExposureHeatMap({ cells }: { cells: Cell[] }) {
  // Dashboard widget added for Ironhold (IRN-088). Shows sector × region
  // exposure at the book level; green = underweight, red = overweight
  // relative to the book's target.
  const sectors = [...new Set(cells.map((c) => c.sector))];
  const regions = [...new Set(cells.map((c) => c.region))];
  const key = (s: string, r: string) => `${s}::${r}`;
  const lookup: Record<string, number> = {};
  cells.forEach((c) => (lookup[key(c.sector, c.region)] = c.exposure));
  return (
    <table className="exposure-heatmap">
      <thead>
        <tr>
          <th></th>
          {regions.map((r) => <th key={r}>{r}</th>)}
        </tr>
      </thead>
      <tbody>
        {sectors.map((s) => (
          <tr key={s}>
            <th>{s}</th>
            {regions.map((r) => {
              const v = lookup[key(s, r)] ?? 0;
              const bg = v > 0 ? `rgba(200,40,40,${Math.min(1, v)})`
                              : `rgba(40,160,80,${Math.min(1, -v)})`;
              return <td key={r} style={{ background: bg }}>{(v * 100).toFixed(1)}%</td>;
            })}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
