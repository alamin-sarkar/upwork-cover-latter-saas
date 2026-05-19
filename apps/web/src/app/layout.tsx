import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PitchCraft — AI Cover Letters for Upwork",
  description: "Paste an Upwork job post, get a personalized cover letter backed by your profile.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
