interface SparklineProps {
  data: number[];
  width?: number;
  height?: number;
  className?: string;
  trend?: "up" | "down" | "flat";
}

export function Sparkline({ data, width = 96, height = 24, className = "", trend }: SparklineProps) {
  if (!data || data.length < 2) {
    return <svg width={width} height={height} className={className} />;
  }
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const step = width / (data.length - 1);
  const points = data
    .map((v, i) => `${(i * step).toFixed(2)},${(height - ((v - min) / range) * height).toFixed(2)}`)
    .join(" ");
  const color = trend === "up" ? "currentColor" : trend === "down" ? "currentColor" : "currentColor";
  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      className={className}
      aria-hidden
    >
      <polyline
        fill="none"
        stroke={color}
        strokeWidth="1.25"
        strokeLinecap="round"
        strokeLinejoin="round"
        points={points}
      />
    </svg>
  );
}
