import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PitchCraft — AI Cover Letters for Upwork",
  description:
    "Paste an Upwork job post, get a personalized cover letter backed by your profile, samples, and writing rules.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-bg-base text-ink-primary antialiased">
        {children}
      </body>
    </html>
  );
}
