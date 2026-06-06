import { fmt, deltaSign, cn } from "@/lib/utils";
import { Sparkline } from "./Sparkline";
import Link from "next/link";

interface IndicatorTileProps {
  label: string;
  value: number;
  unit?: string;
  delta?: number;
  spark?: number[];
  asOf?: string;
  href?: string;
  badge?: string;
  className?: string;
}

export function IndicatorTile({
  label,
  value,
  unit,
  delta,
  spark,
  asOf,
  href,
  badge,
  className,
}: IndicatorTileProps) {
  const dir = deltaSign(delta);
  const wrapClassName = cn(
    "tile group relative block hover:border-line-strong",
    className
  );
  const inner = (
    <>
      <div className="flex items-start justify-between gap-2">
        <div className="tile-h">{label}</div>
        {badge && <span className="pill-info">{badge}</span>}
      </div>
      <div className="mt-1 flex items-baseline gap-2">
        <div className="tile-v">{fmt(value, unit)}</div>
        {delta !== undefined && (
          <span
            className={cn(
              "num text-xs",
              dir === "up" && "text-good",
              dir === "down" && "text-bad",
              dir === "flat" && "text-ink-muted"
            )}
          >
            {delta >= 0 ? "▲" : "▼"} {Math.abs(delta).toFixed(2)}
          </span>
        )}
      </div>
      {spark && spark.length > 1 && (
        <Sparkline
          data={spark}
          trend={dir}
          className={cn(
            "mt-2 h-6 w-full",
            dir === "up" && "text-good",
            dir === "down" && "text-bad",
            dir === "flat" && "text-ink-muted"
          )}
        />
      )}
      {asOf && (
        <div className="mt-1 text-2xs text-ink-subtle">as of {asOf}</div>
      )}
    </>
  );
  return href ? (
    <Link href={href} className={wrapClassName}>
      {inner}
    </Link>
  ) : (
    <div className={wrapClassName}>{inner}</div>
  );
}
