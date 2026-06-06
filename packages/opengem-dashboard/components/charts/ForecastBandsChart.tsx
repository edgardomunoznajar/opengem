"use client";

import { useMemo } from "react";

interface BandPoint {
  date: string;        // ISO YYYY-MM-DD or YYYY-Qx
  p10: number;
  p50: number;
  p90: number;
  consensus?: number;  // optional consensus overlay
  actual?: number;     // populated retroactively after truth lands
}

interface ForecastBandsChartProps {
  points: BandPoint[];
  unit?: string;
  height?: number;
  className?: string;
}

/**
 * Pure-SVG forecast chart with P10-P90 band area + P50 line + consensus overlay + actual dots.
 *
 * No external chart library — keeps the prototype install-free and the JS budget tiny.
 * In production, swap to TradingView Lightweight Charts (Apache-2.0) with a custom area-pair
 * pattern for the bands (Lightweight Charts has area + line series; pair two areas to get the band).
 *
 * The "miss arrow" is rendered when an actual value falls outside the P10-P90 band — this is the
 * accountability surface made visible directly on the chart.
 */
export function ForecastBandsChart({
  points,
  unit = "%",
  height = 240,
  className = "",
}: ForecastBandsChartProps) {
  const layout = useMemo(() => {
    if (!points || points.length < 2) return null;
    const width = 800;
    const padding = { top: 16, right: 56, bottom: 28, left: 36 };
    const innerW = width - padding.left - padding.right;
    const innerH = height - padding.top - padding.bottom;

    const allY = points.flatMap((p) => [p.p10, p.p50, p.p90, p.consensus ?? p.p50, p.actual ?? p.p50]);
    const yMin = Math.min(...allY) - 0.5;
    const yMax = Math.max(...allY) + 0.5;
    const yRange = yMax - yMin;

    const xStep = innerW / (points.length - 1);
    const xAt = (i: number) => padding.left + i * xStep;
    const yAt = (v: number) => padding.top + innerH - ((v - yMin) / yRange) * innerH;

    const bandPath = (() => {
      const upper = points.map((p, i) => `${xAt(i)},${yAt(p.p90)}`);
      const lower = points.slice().reverse().map((p, i) => `${xAt(points.length - 1 - i)},${yAt(p.p10)}`);
      return `M ${upper.join(" L ")} L ${lower.join(" L ")} Z`;
    })();
    const medianPath = points.map((p, i) => `${i === 0 ? "M" : "L"} ${xAt(i)} ${yAt(p.p50)}`).join(" ");
    const consensusPath = points
      .filter((p) => p.consensus !== undefined)
      .map((p, i, arr) => `${i === 0 ? "M" : "L"} ${xAt(points.indexOf(p))} ${yAt(p.consensus!)}`)
      .join(" ");

    const actuals = points
      .map((p, i) => ({ ...p, idx: i }))
      .filter((p) => p.actual !== undefined);

    const ticksY = 4;
    const yTicks = Array.from({ length: ticksY + 1 }, (_, i) => yMin + (yRange / ticksY) * i);

    return {
      width,
      height,
      padding,
      innerW,
      innerH,
      yMin,
      yMax,
      yRange,
      xAt,
      yAt,
      bandPath,
      medianPath,
      consensusPath,
      actuals,
      yTicks,
    };
  }, [points, height]);

  if (!layout) return null;
  const { width, padding, yAt, xAt, bandPath, medianPath, consensusPath, actuals, yTicks } = layout;

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      className={`w-full text-ink ${className}`}
      role="img"
      aria-label="Forecast with P10–P90 bands, P50 median, consensus overlay, and actual outcomes"
    >
      {/* Y-axis ticks + gridlines */}
      {yTicks.map((tv, i) => (
        <g key={`y${i}`}>
          <line
            x1={padding.left}
            x2={width - padding.right}
            y1={yAt(tv)}
            y2={yAt(tv)}
            stroke="#27272a"
            strokeDasharray="2,3"
          />
          <text
            x={width - padding.right + 4}
            y={yAt(tv) + 3}
            className="fill-[#71717a] font-mono"
            style={{ fontSize: 10 }}
          >
            {tv.toFixed(1)}{unit}
          </text>
        </g>
      ))}

      {/* X-axis labels */}
      {points.map((p, i) => {
        // Only show every other label to avoid crowding
        if (i % Math.max(1, Math.floor(points.length / 8)) !== 0) return null;
        return (
          <text
            key={`x${i}`}
            x={xAt(i)}
            y={height - padding.bottom + 14}
            textAnchor="middle"
            className="fill-[#71717a] font-mono"
            style={{ fontSize: 10 }}
          >
            {p.date}
          </text>
        );
      })}

      {/* Band area (P10-P90) */}
      <path d={bandPath} fill="#f59e0b" fillOpacity={0.15} stroke="none" />

      {/* P50 median line */}
      <path d={medianPath} fill="none" stroke="#f59e0b" strokeWidth={1.6} />

      {/* Consensus overlay (dashed) */}
      {consensusPath && (
        <path
          d={consensusPath}
          fill="none"
          stroke="#a1a1aa"
          strokeWidth={1.2}
          strokeDasharray="4,4"
        />
      )}

      {/* Actual outcome dots — green inside band, red outside (the miss surface) */}
      {actuals.map((a, i) => {
        const inside = a.actual! >= a.p10 && a.actual! <= a.p90;
        return (
          <g key={`a${i}`}>
            <circle
              cx={xAt(a.idx)}
              cy={yAt(a.actual!)}
              r={3.5}
              fill={inside ? "#10b981" : "#ef4444"}
              stroke="#0a0a0b"
              strokeWidth={1}
            />
            {!inside && (
              <line
                x1={xAt(a.idx)}
                x2={xAt(a.idx)}
                y1={yAt(a.p50)}
                y2={yAt(a.actual!)}
                stroke="#ef4444"
                strokeWidth={1}
                strokeDasharray="2,2"
              />
            )}
          </g>
        );
      })}

      {/* Legend */}
      <g transform={`translate(${padding.left}, ${padding.top - 6})`}>
        <text x={0} y={0} className="fill-[#a1a1aa] font-mono" style={{ fontSize: 10 }}>
          <tspan fill="#f59e0b">━</tspan>
          <tspan> OPENGEM (P50)</tspan>
          <tspan fill="#f59e0b" fillOpacity={0.4}> ░</tspan>
          <tspan> P10–P90</tspan>
          <tspan fill="#a1a1aa"> ╌</tspan>
          <tspan> consensus</tspan>
          <tspan fill="#10b981"> ●</tspan>
          <tspan> hit</tspan>
          <tspan fill="#ef4444"> ●</tspan>
          <tspan> miss</tspan>
        </text>
      </g>
    </svg>
  );
}
