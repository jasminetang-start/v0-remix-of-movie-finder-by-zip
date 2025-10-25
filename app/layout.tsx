import type React from "react"
import type { Metadata } from "next"
import localFont from "next/font/local"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"

const myriadPro = localFont({
  src: [
    {
      path: "../public/fonts/MyriadPro-Regular.woff2",
      weight: "400",
      style: "normal",
    },
    {
      path: "../public/fonts/MyriadPro-Bold.woff2",
      weight: "700",
      style: "normal",
    },
  ],
  variable: "--font-myriad",
  display: "swap",
})

const impact = localFont({
  src: "../public/fonts/Impact.woff2",
  variable: "--font-impact",
  display: "swap",
})

const chineseTitle = localFont({
  src: "../public/fonts/ZiyuAijiaGongluTi.woff2",
  variable: "--font-chinese-title",
  display: "swap",
})

const hkSentiments = localFont({
  src: [
    {
      path: "../public/fonts/HKSentiments-Regular.woff2",
      weight: "400",
      style: "normal",
    },
    {
      path: "../public/fonts/HKSentiments-Bold.woff2",
      weight: "700",
      style: "normal",
    },
  ],
  variable: "--font-hk-sentiments",
  display: "swap",
})

export const metadata: Metadata = {
  title: "STArt Film Studio",
  description: "Discover movies in your area",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body
        className={`${hkSentiments.variable} ${impact.variable} ${myriadPro.variable} ${chineseTitle.variable} font-sans antialiased`}
      >
        {children}
        <Analytics />
      </body>
    </html>
  )
}
