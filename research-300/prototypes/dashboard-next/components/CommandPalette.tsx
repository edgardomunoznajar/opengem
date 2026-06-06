"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface Command {
  id: string;
  label: string;
  shortcut?: string;
  go: string;
  group: "Country" | "Indicator" | "Scenario" | "Page" | "Vintage";
}

const COMMANDS: Command[] = [
  // Pages
  { id: "p-home", label: "Pulse — home", shortcut: "g h", go: "/", group: "Page" },
  { id: "p-countries", label: "All countries", shortcut: "g c", go: "/countries", group: "Page" },
  { id: "p-indicators", label: "All indicators", shortcut: "g i", go: "/indicators", group: "Page" },
  { id: "p-scenarios", label: "All scenarios", shortcut: "g s", go: "/scenarios", group: "Page" },
  { id: "p-forecasts", label: "All forecasts", shortcut: "g f", go: "/forecasts", group: "Page" },
  { id: "p-leaderboard", label: "Leaderboard", shortcut: "g l", go: "/leaderboard", group: "Page" },
  { id: "p-methodology", label: "Methodology", shortcut: "g m", go: "/methodology", group: "Page" },
  { id: "p-accountability", label: "Accountability ledger", shortcut: "g a", go: "/accountability", group: "Page" },
  { id: "p-events", label: "Events feed", shortcut: "g e", go: "/events", group: "Page" },
  { id: "p-vintage", label: "Vintage rewinder", shortcut: "v", go: "/vintage", group: "Page" },
  // Countries
  { id: "c-usa", label: "🇺🇸 United States", go: "/countries/USA", group: "Country" },
  { id: "c-chn", label: "🇨🇳 China", go: "/countries/CHN", group: "Country" },
  { id: "c-jpn", label: "🇯🇵 Japan", go: "/countries/JPN", group: "Country" },
  { id: "c-deu", label: "🇩🇪 Germany", go: "/countries/DEU", group: "Country" },
  { id: "c-gbr", label: "🇬🇧 United Kingdom", go: "/countries/GBR", group: "Country" },
  { id: "c-fra", label: "🇫🇷 France", go: "/countries/FRA", group: "Country" },
  { id: "c-ind", label: "🇮🇳 India", go: "/countries/IND", group: "Country" },
  { id: "c-bra", label: "🇧🇷 Brazil", go: "/countries/BRA", group: "Country" },
  // Indicators
  { id: "i-gdp", label: "GDP growth (YoY)", go: "/indicators/gdp_yoy", group: "Indicator" },
  { id: "i-cpi", label: "CPI inflation (YoY)", go: "/indicators/cpi_yoy", group: "Indicator" },
  { id: "i-unemp", label: "Unemployment rate", go: "/indicators/unemployment", group: "Indicator" },
  { id: "i-rate", label: "Policy rate", go: "/indicators/policy_rate", group: "Indicator" },
  { id: "i-gpr", label: "Geopolitical risk", go: "/indicators/gpr", group: "Indicator" },
  { id: "i-gscpi", label: "Supply chain pressure (GSCPI)", go: "/indicators/gscpi", group: "Indicator" },
  // Scenarios
  { id: "s-us-rec", label: "US recession 2026 H2", go: "/scenarios/us-recession-2026h2", group: "Scenario" },
  { id: "s-eu-en", label: "EU winter energy shock", go: "/scenarios/eu-energy-shock-winter-2026", group: "Scenario" },
  { id: "s-cn-pp", label: "China property double-dip", go: "/scenarios/china-property-double-dip", group: "Scenario" },
  { id: "s-twn", label: "Taiwan Strait escalation", go: "/scenarios/taiwan-strait-escalation", group: "Scenario" },
];

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const router = useRouter();

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((o) => !o);
      } else if (e.key === "Escape") {
        setOpen(false);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  if (!open) return null;
  const filtered = COMMANDS.filter((c) =>
    c.label.toLowerCase().includes(q.toLowerCase())
  );
  const groups = filtered.reduce<Record<string, Command[]>>((acc, c) => {
    (acc[c.group] ??= []).push(c);
    return acc;
  }, {});

  return (
    <div
      className="fixed inset-0 z-[100] flex items-start justify-center bg-black/60 pt-24"
      onClick={() => setOpen(false)}
    >
      <div
        className="w-full max-w-xl rounded-sm border border-line bg-bg-elevated shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <input
          autoFocus
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search countries, indicators, scenarios, pages..."
          className="w-full border-b border-line bg-transparent px-4 py-3 font-mono text-sm text-ink outline-none placeholder:text-ink-subtle"
        />
        <div className="max-h-96 overflow-y-auto">
          {Object.entries(groups).map(([group, items]) => (
            <div key={group} className="p-1">
              <div className="px-3 py-1 text-2xs uppercase tracking-wider text-ink-subtle">{group}</div>
              {items.map((c) => (
                <button
                  key={c.id}
                  className="flex w-full items-center justify-between rounded-sm px-3 py-2 text-left text-sm text-ink hover:bg-bg-overlay"
                  onClick={() => {
                    setOpen(false);
                    router.push(c.go);
                  }}
                >
                  <span>{c.label}</span>
                  {c.shortcut && <span className="kbd">{c.shortcut}</span>}
                </button>
              ))}
            </div>
          ))}
          {filtered.length === 0 && (
            <div className="px-4 py-6 text-center text-2xs text-ink-subtle">
              No matches. Try a country code, indicator name, or page name.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
