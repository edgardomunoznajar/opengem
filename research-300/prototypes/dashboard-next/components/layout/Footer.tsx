export function Footer() {
  return (
    <footer className="mt-12 border-t border-line">
      <div className="mx-auto max-w-[1600px] px-4 py-6 text-2xs text-ink-subtle">
        <div className="grid grid-cols-1 gap-6 md:grid-cols-4">
          <div>
            <div className="mb-2 font-mono uppercase tracking-widest text-brand-400">
              OPENGEM
            </div>
            <p className="leading-relaxed">
              Open-source world dashboard. Every forecast vintaged. Every miss named.
              <br />
              Apache-2.0 code · CC-BY-4.0 data.
            </p>
          </div>
          <div>
            <div className="mb-2 uppercase tracking-wide">Product</div>
            <ul className="space-y-1">
              <li><a href="/pricing" className="hover:text-ink">Pricing</a></li>
              <li><a href="/api" className="hover:text-ink">API</a></li>
              <li><a href="/mcp" className="hover:text-ink">MCP server</a></li>
              <li><a href="/embed" className="hover:text-ink">Embeds</a></li>
            </ul>
          </div>
          <div>
            <div className="mb-2 uppercase tracking-wide">Open</div>
            <ul className="space-y-1">
              <li><a href="/accountability" className="hover:text-ink">Accountability ledger</a></li>
              <li><a href="/methodology" className="hover:text-ink">Methodology</a></li>
              <li><a href="/changelog" className="hover:text-ink">Changelog</a></li>
              <li><a href="https://github.com/opengem/opengem" className="hover:text-ink">GitHub</a></li>
            </ul>
          </div>
          <div>
            <div className="mb-2 uppercase tracking-wide">Legal</div>
            <ul className="space-y-1">
              <li><a href="/terms" className="hover:text-ink">Terms</a></li>
              <li><a href="/privacy" className="hover:text-ink">Privacy</a></li>
              <li><a href="/governance" className="hover:text-ink">Governance</a></li>
            </ul>
          </div>
        </div>
        <div className="mt-6 border-t border-line pt-4">
          Not investment advice. Not affiliated with any sovereign entity. All forecasts
          are open-vintaged and scored — see the{" "}
          <a className="underline hover:text-ink" href="/accountability">accountability ledger</a>.
        </div>
      </div>
    </footer>
  );
}
