import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "F1 Strategy Room",
  description: "Turn F1 telemetry into race-winning strategy insights",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
