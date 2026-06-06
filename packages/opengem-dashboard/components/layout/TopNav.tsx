import Link from "next/link";

const NAV = [
  { href: "/", label: "Pulse" },
  { href: "/countries", label: "Countries" },
  { href: "/indicators", label: "Indicators" },
  { href: "/scenarios", label: "Scenarios" },
  { href: "/forecasts", label: "Forecasts" },
  { href: "/leaderboard", label: "Leaderboard" },
  { href: "/methodology", label: "Methodology" },
];

export function TopNav() {
  return (
    <header className="sticky top-0 z-50 border-b border-line bg-bg/95 backdrop-blur">
      <div className="mx-auto flex max-w-[1600px] items-center gap-6 px-4 h-12">
        <Link href="/" className="flex items-baseline gap-2">
          <span className="font-mono text-xs uppercase tracking-widest text-brand-400">
            OPENGEM
          </span>
          <span className="text-2xs text-ink-subtle">v0.1 prototype</span>
        </Link>
        <nav className="flex items-center gap-1">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-sm px-2 py-1 text-sm text-ink-muted hover:bg-bg-elevated hover:text-ink"
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="flex-1" />
        <button
          className="flex items-center gap-2 rounded-sm border border-line bg-bg-elevated px-2 py-1 text-2xs text-ink-muted hover:text-ink"
          aria-label="Open command palette"
        >
          <span>Search</span>
          <span className="kbd">⌘K</span>
        </button>
      </div>
    </header>
  );
}
