import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CandiLift',
  description: 'AI-powered resume analysis and optimization tool',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
        {children}
      </body>
    </html>
  )
}
