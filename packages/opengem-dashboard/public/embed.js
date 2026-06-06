/**
 * OPENGEM Embed SDK — drop-in tile/chart embed.
 *
 * Usage:
 *   <div data-opengem
 *        data-kind="tile"
 *        data-country="USA"
 *        data-indicator="recession_prob"
 *        data-size="square"></div>
 *   <script src="https://opengem.org/embed.js" defer></script>
 *
 * Sizes: "square" (200x200), "banner" (600x120), "tall" (300x420)
 *
 * Every embed includes a tiny attribution link back to OPENGEM and a
 * mandatory "data-vintage" badge — that is the price of using the data.
 *
 * License: Apache-2.0
 */

(function () {
  const API = "https://opengem.org/v1";
  const SIZES = {
    square: { w: 200, h: 200 },
    banner: { w: 600, h: 120 },
    tall:   { w: 300, h: 420 },
  };

  function el(tag, attrs, ...children) {
    const e = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => {
      if (k === "style") Object.assign(e.style, v);
      else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v);
    });
    children.forEach((c) => {
      if (c == null) return;
      e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return e;
  }

  function sparkline(values, w, h, color) {
    if (!values || values.length < 2) return "";
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;
    const step = w / (values.length - 1);
    const pts = values
      .map((v, i) => `${(i * step).toFixed(2)},${(h - ((v - min) / range) * h).toFixed(2)}`)
      .join(" ");
    return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><polyline fill="none" stroke="${color}" stroke-width="1.4" points="${pts}" /></svg>`;
  }

  async function fetchData(kind, country, indicator) {
    const path =
      kind === "recession_prob"
        ? `${API}/recession-probability?country=${encodeURIComponent(country)}`
        : kind === "gpr_nowcast"
        ? `${API}/gpr-nowcast${country ? `?country=${encodeURIComponent(country)}` : ""}`
        : `${API}/forecasts?country=${encodeURIComponent(country)}&indicator=${encodeURIComponent(indicator)}`;
    try {
      const res = await fetch(path);
      if (!res.ok) return null;
      return await res.json();
    } catch {
      return null;
    }
  }

  function renderTile(node, data, size, label, vintage) {
    const dims = SIZES[size] ?? SIZES.square;
    const value = data?.value ?? (Array.isArray(data) ? data[0]?.point : undefined);
    const delta = data?.delta;
    const spark = data?.spark;
    const color = delta == null ? "#a1a1aa" : delta > 0 ? "#10b981" : "#ef4444";
    node.innerHTML = `
      <div style="
        width:${dims.w}px;height:${dims.h}px;
        background:#0a0a0b;color:#fafafa;
        font-family:Inter,system-ui,sans-serif;
        border:1px solid #27272a;border-radius:2px;
        padding:12px;box-sizing:border-box;display:flex;flex-direction:column;gap:6px;
      ">
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.06em;color:#a1a1aa">
          ${label}
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:28px;font-variant-numeric:tabular-nums">
          ${value != null ? value.toFixed(2) : "—"}
          ${delta != null ? `<span style="color:${color};font-size:14px;margin-left:6px">${delta > 0 ? "▲" : "▼"} ${Math.abs(delta).toFixed(2)}</span>` : ""}
        </div>
        ${spark ? `<div style="color:${color}">${sparkline(spark, dims.w - 24, 24, color)}</div>` : ""}
        <div style="flex:1"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;font-size:10px;color:#71717a">
          <span>vintage ${vintage ?? "—"}</span>
          <a href="https://opengem.org" target="_blank" style="color:#f59e0b;text-decoration:none">OPENGEM</a>
        </div>
      </div>
    `;
  }

  function mount(node) {
    const kind = node.dataset.kind || "forecast";
    const country = node.dataset.country || "USA";
    const indicator = node.dataset.indicator || "gdp_yoy";
    const size = node.dataset.size || "square";

    const label =
      kind === "recession_prob" ? `${country} recession 12m` :
      kind === "gpr_nowcast" ? "Geopolitical risk" :
      `${country} ${indicator}`;

    fetchData(kind, country, indicator).then((data) => {
      const vintage = data?.as_of || (Array.isArray(data) ? data[0]?.vintage_id : undefined);
      renderTile(node, data, size, label, vintage);
    });
  }

  function init() {
    document.querySelectorAll("[data-opengem]").forEach(mount);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.OPENGEM = { mount, init };
})();
