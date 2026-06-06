import Link from "next/link";
import { isoToFlag, cn } from "@/lib/utils";

const EVENTS = [
  {
    ts: "2026-06-05T22:14:00Z",
    tag: "geopolitics",
    severity: "high",
    countries: ["CHN", "TWN", "USA", "JPN"],
    headline: "Joint US-Japan-Korea naval exercise enters fourth week",
    source: "GDELT GKG",
    why: "Triggers Taiwan Strait escalation scenario (probability ↑ to 18%)",
  },
  {
    ts: "2026-06-05T18:00:00Z",
    tag: "central-bank",
    severity: "high",
    countries: ["USA"],
    headline: "FOMC June minutes: dot plot shifts dovish by 25bp",
    source: "FRB",
    why: "Lowers OPENGEM 1Y policy-rate path by 18bp",
  },
  {
    ts: "2026-06-05T14:00:00Z",
    tag: "macro-print",
    severity: "medium",
    countries: ["USA"],
    headline: "May CPI: headline +0.2% MoM, core +0.3% MoM",
    source: "BLS",
    why: "Cleveland nowcast revises to 2.7% YoY (was 2.9%)",
  },
  {
    ts: "2026-06-05T08:30:00Z",
    tag: "energy",
    severity: "medium",
    countries: ["RUS", "DEU", "FRA", "ITA"],
    headline: "Brent crude +3.4% on Saudi voluntary cut extension",
    source: "ICE / Reuters",
    why: "Lifts EU inflation 4Q nowcast +0.1pp",
  },
  {
    ts: "2026-06-04T13:22:00Z",
    tag: "macro-print",
    severity: "high",
    countries: ["USA"],
    headline: "Nonfarm payrolls: +68k vs +145k expected",
    source: "BLS",
    why: "Triggers US recession 2026H2 scenario (probability ↑ to 34%)",
  },
  {
    ts: "2026-06-04T09:00:00Z",
    tag: "geopolitics",
    severity: "low",
    countries: ["UKR", "RUS"],
    headline: "Drone activity in Black Sea up week-on-week — GDELT count",
    source: "GDELT GKG",
    why: "GPR-Russia index +4 points",
  },
];

const SEV: Record<string, string> = {
  high: "pill-bad",
  medium: "pill-warn",
  low: "pill-info",
};

export default function EventsPage() {
  return (
    <div className="space-y-4">
      <header className="border-b border-line pb-4 flex items-baseline justify-between">
        <div>
          <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
            Events
          </h1>
          <p className="mt-2 text-sm text-ink-muted">
            What just happened, and what it did to OPENGEM's nowcasts and scenarios.
            Drawn from GDELT GKG, agency releases, market feeds.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <a href="/feeds/events.atom" className="pill-info">Atom</a>
          <a href="/feeds/events.rss" className="pill-info">RSS</a>
        </div>
      </header>

      <div className="rounded-sm border border-line bg-bg-elevated divide-y divide-line">
        {EVENTS.map((e) => (
          <div key={e.ts} className="p-3 hover:bg-bg-overlay">
            <div className="flex items-center gap-2 text-2xs text-ink-subtle">
              <span className={cn("pill num", SEV[e.severity])}>{e.severity}</span>
              <span className="pill-info">{e.tag}</span>
              <span className="font-mono">{new Date(e.ts).toISOString().slice(0, 16).replace("T", " ")}Z</span>
              <span className="flex-1" />
              <span>via {e.source}</span>
            </div>
            <div className="mt-1 text-sm text-ink">{e.headline}</div>
            <div className="mt-1 text-2xs text-ink-muted italic">→ {e.why}</div>
            <div className="mt-1 flex flex-wrap gap-1">
              {e.countries.map((c) => (
                <Link
                  key={c}
                  href={`/countries/${c}`}
                  className="font-mono text-2xs text-ink-subtle hover:text-ink"
                >
                  {isoToFlag(c)} {c}
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
