import Link from "next/link";

const SNIPPETS: Array<{ title: string; subtitle: string; lang: string; code: string }> = [
  {
    title: "Claude Desktop / Claude.ai",
    subtitle: "Add to ~/.config/Claude/claude_desktop_config.json",
    lang: "json",
    code: `{
  "mcpServers": {
    "opengem": {
      "command": "npx",
      "args": ["-y", "@opengem/mcp-server"],
      "env": { "OPENGEM_API_KEY": "<your-key-or-leave-empty>" }
    }
  }
}`,
  },
  {
    title: "Cursor",
    subtitle: "Settings → MCP → Add server",
    lang: "json",
    code: `{
  "name": "opengem",
  "command": "npx",
  "args": ["-y", "@opengem/mcp-server"]
}`,
  },
  {
    title: "ChatGPT (via OpenAI Connectors)",
    subtitle: "Settings → Connectors → Custom MCP URL",
    lang: "text",
    code: `https://opengem.org/mcp/sse`,
  },
  {
    title: "VS Code (with Continue.dev)",
    subtitle: "~/.continue/config.json mcpServers",
    lang: "json",
    code: `"mcpServers": [
  {
    "name": "opengem",
    "transport": { "type": "stdio", "command": "npx", "args": ["-y", "@opengem/mcp-server"] }
  }
]`,
  },
];

const TOOLS = [
  { name: "get_forecast", desc: "Fetch a single forecast object — country × indicator × horizon." },
  { name: "compare_forecasts", desc: "Compare OPENGEM forecasts against WEO, OECD EO, FRB SEP, ECB SPF." },
  { name: "list_scenarios", desc: "List currently-triggered scenarios with probabilities and affected countries." },
  { name: "get_recession_probability", desc: "Bauer-Mertens 12-month recession probability per Tier-V country." },
  { name: "get_gpr_nowcast", desc: "Caldara-Iacoviello geopolitical-risk nowcast — global or per-country." },
  { name: "rewind_vintage", desc: "Replay any historical forecast at any vintage date." },
  { name: "get_leaderboard", desc: "Forecast leaderboard per indicator × horizon (CRPS-ranked)." },
  { name: "list_misses", desc: "Recent forecast misses with post-mortem URLs." },
];

export default function MCPPage() {
  return (
    <div className="space-y-6 max-w-4xl">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          MCP server — install
        </h1>
        <p className="mt-2 text-base text-ink">
          Plug OPENGEM into Claude, ChatGPT, Cursor, VS Code, or any MCP-compatible
          client. Eight tools, fully open, vintage-stamped responses, optional API key
          for elevated rate limits.
        </p>
      </header>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {SNIPPETS.map((s) => (
          <div key={s.title} className="tile">
            <div className="tile-h">{s.title}</div>
            <div className="mt-1 text-2xs text-ink-subtle">{s.subtitle}</div>
            <pre className="mt-2 overflow-x-auto rounded-sm border border-line bg-bg-overlay p-2 font-mono text-2xs">
              {s.code}
            </pre>
          </div>
        ))}
      </section>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Tools exposed
        </h2>
        <div className="rounded-sm border border-line bg-bg-elevated divide-y divide-line">
          {TOOLS.map((t) => (
            <div key={t.name} className="grid grid-cols-1 gap-1 p-3 md:grid-cols-4">
              <code className="md:col-span-1 font-mono text-sm text-brand-400">{t.name}</code>
              <p className="md:col-span-3 text-sm text-ink-muted">{t.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-sm border border-line bg-bg-elevated p-4 text-sm text-ink-muted">
        <h2 className="font-mono text-sm uppercase tracking-widest text-brand-400">
          The MCP guarantee
        </h2>
        <ul className="mt-2 list-inside list-disc space-y-1">
          <li>
            Every tool response includes a <code className="text-brand-400">vintage_id</code> and a
            <code className="text-brand-400"> provenance</code> object.
          </li>
          <li>
            The LLM you wrap us with cannot "hallucinate" a forecast — it always gets a
            numbered, dated, model-cited object.
          </li>
          <li>
            Misses are surfaced in the same response stream as fresh forecasts. The model
            sees both.
          </li>
          <li>
            Free tier: 100 tool calls / day / IP. Pro tier: 100k / day / key.
          </li>
        </ul>
        <div className="mt-3">
          <Link href="/pricing" className="text-info underline">
            Pricing →
          </Link>
        </div>
      </section>
    </div>
  );
}
