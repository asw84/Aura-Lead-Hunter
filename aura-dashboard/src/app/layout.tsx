import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Aura AI Hub | 204+ Hot Leads Found 🚀",
  description: "Autonomous AI engine for real-time Affiliate Marketing & Web3 Intelligence. 200+ verified leads identified.",
  keywords: ["affiliate marketing", "leads", "telegram scraper", "crypto", "arbitrage"],
  authors: [{ name: "Aura AI" }],
  openGraph: {
    title: "Aura AI Hub 💘 Matchmaking 2.0",
    description: "Real-time AI matching for top-tier traffic buyers and employers. Discover the best opportunities in arbitrage.",
    url: "https://aura-dashboard-nine.vercel.app",
    siteName: "Aura Lead Hunter",
    images: [
      {
        url: "/aura.png",
        width: 1200,
        height: 630,
        alt: "Aura AI Hub Preview",
      },
    ],
    locale: "ru_RU",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Aura AI Hub | Leads & Matchmaking",
    description: "Autonomous AI engine for real-time Affiliate Marketing intelligence.",
    images: ["/aura.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        suppressHydrationWarning
      >
        {children}
      </body>
    </html>
  );
}
