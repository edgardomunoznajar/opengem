import { getScenarios } from "@/lib/api";
import Link from "next/link";
import { cn } from "@/lib/utils";

export default async function ScenariosIndex() {
  const scenarios = await getScenarios();
  const sorted = [...scenarios].sort((a, b) => b.probability - a.probability);

  return (
    <div className="space-y-4">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          Scenarios
        </h1>
        <p className="mt-2 text-sm text-ink-muted">
          Pre-coded scenarios fire when their trigger conditions hit. Probability
          rolls up Bayesian conditional on observed indicators. Every trigger is
          machine-checkable and every methodology is open.
        </p>
      </header>
      <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
        <table className="min-w-full text-sm">
          <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
            <tr>
              <th className="px-3 py-2 text-left">Scenario</th>
              <th className="px-3 py-2 text-right">P</th>
              <th className="px-3 py-2 text-left">Trigger</th>
              <th className="px-3 py-2 text-left">Countries</th>
              <th className="px-3 py-2 text-left">Triggered</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {sorted.map((s) => (
              <tr key={s.slug} className="hover:bg-bg-overlay">
                <td className="px-3 py-2">
                  <Link href={`/scenarios/${s.slug}`} className="text-ink hover:underline">
                    {s.name}
                  </Link>
                </td>
                <td className="px-3 py-2 text-right">
                  <span
                    className={cn(
                      "pill num",
                      s.probability > 0.5 && "pill-bad",
                      s.probability > 0.25 && s.probability <= 0.5 && "pill-warn",
                      s.probability <= 0.25 && "pill-good"
                    )}
                  >
                    {(s.probability * 100).toFixed(0)}%
                  </span>
                </td>
                <td className="px-3 py-2 text-2xs text-ink-muted">
                  {s.trigger_summary.slice(0, 80)}…
                </td>
                <td className="px-3 py-2 font-mono text-2xs text-ink-muted">
                  {s.affected_countries.join(" ")}
                </td>
                <td className="px-3 py-2 text-2xs text-ink-subtle">
                  {new Date(s.triggered_at).toISOString().slice(0, 16).replace("T", " ")}Z
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
