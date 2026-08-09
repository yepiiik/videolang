import type { Metadata } from "next";
import "./globals.css";

import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

export const metadata: Metadata = {
  title: "uSearch - Intelligent YouTube Caption Search",
  description: "Find specific information in videos with intelligent search.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased scroll-smooth">
      <body className="min-h-full flex flex-col bg-background text-foreground animate-in fade-in duration-500">
        <Navbar />
        <main className="flex-1 flex flex-col min-w-0">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
