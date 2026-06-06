import type { Config } from "tailwindcss";

/**
 * OPENGEM Dashboard — terminal palette.
 * Inspired by Bloomberg amber, but with editorial restraint.
 * Default theme = dark. Light theme available.
 */
const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Semantic
        good: { DEFAULT: "#10b981", muted: "#047857" }, // green-500/700
        bad: { DEFAULT: "#ef4444", muted: "#991b1b" }, // red-500/800
        warn: { DEFAULT: "#f59e0b", muted: "#92400e" }, // amber-500/800
        info: { DEFAULT: "#3b82f6", muted: "#1e40af" }, // blue-500/800
        // Brand (terminal amber, editorial pink alt)
        brand: {
          50: "#fffbeb",
          100: "#fef3c7",
          200: "#fde68a",
          300: "#fcd34d",
          400: "#fbbf24",
          500: "#f59e0b",
          600: "#d97706",
          700: "#b45309",
          800: "#92400e",
          900: "#78350f",
        },
        // Surfaces
        bg: { DEFAULT: "#0a0a0b", elevated: "#16161a", overlay: "#1f1f25" },
        ink: { DEFAULT: "#fafafa", muted: "#a1a1aa", subtle: "#71717a" },
        // Grid / borders
        line: { DEFAULT: "#27272a", strong: "#3f3f46" },
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
        serif: ["Source Serif 4", "ui-serif", "Georgia", "serif"],
      },
      fontSize: {
        // Terminal information density: a step finer than default
        "2xs": ["0.6875rem", { lineHeight: "1rem" }], // 11px
        xs: ["0.75rem", { lineHeight: "1.125rem" }],   // 12px
        sm: ["0.8125rem", { lineHeight: "1.25rem" }],  // 13px
        base: ["0.875rem", { lineHeight: "1.375rem" }],// 14px
        lg: ["1rem", { lineHeight: "1.5rem" }],
        xl: ["1.125rem", { lineHeight: "1.625rem" }],
        "2xl": ["1.375rem", { lineHeight: "1.875rem" }],
        "3xl": ["1.75rem", { lineHeight: "2.25rem" }],
      },
      borderRadius: {
        sm: "0.125rem", // 2px — terminal-square
        DEFAULT: "0.25rem",
        md: "0.375rem",
        lg: "0.5rem",
      },
      animation: {
        "pulse-fast": "pulse 0.8s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
    },
  },
  plugins: [],
};

export default config;
