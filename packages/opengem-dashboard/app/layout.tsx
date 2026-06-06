import type { Metadata } from "next";
import "./globals.css";
import { TopNav } from "@/components/layout/TopNav";
import { Footer } from "@/components/layout/Footer";
import { CommandPalette } from "@/components/CommandPalette";

export const metadata: Metadata = {
  title: "OPENGEM — The World Dashboard",
  description:
    "Open-source macro + geopolitics dashboard. Every forecast vintaged, every miss named.",
  openGraph: {
    title: "OPENGEM — The World Dashboard",
    description:
      "An open-source Bloomberg + Stratfor. Every number dated. Every miss named.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-bg text-ink antialiased">
        <TopNav />
        <main className="mx-auto max-w-[1600px] px-4 py-4">{children}</main>
        <Footer />
        <CommandPalette />
      </body>
    </html>
  );
}
