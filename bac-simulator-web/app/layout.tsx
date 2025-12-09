import type { Metadata, Viewport } from 'next';
import './globals.css';
import { ToastProvider } from '@/components/ui/Toast';

export const metadata: Metadata = {
  title: 'BAC Simulator - Blood Alcohol Calculator',
  description: 'Scientifically accurate blood alcohol content simulator using the Widmark equation. Track drinks, food, and see your estimated BAC over time.',
  keywords: ['BAC', 'blood alcohol', 'calculator', 'drunk driving', 'alcohol metabolism', 'Widmark equation', 'BAC calculator'],
  authors: [{ name: 'BAC Simulator' }],
  creator: 'BAC Simulator',
  publisher: 'BAC Simulator',
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/favicon-16.png', sizes: '16x16', type: 'image/png' },
      { url: '/favicon-32.png', sizes: '32x32', type: 'image/png' },
      { url: '/icon-192.png', sizes: '192x192', type: 'image/png' },
      { url: '/icon-512.png', sizes: '512x512', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
  },
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'BAC Simulator',
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    siteName: 'BAC Simulator',
    title: 'BAC Simulator - Blood Alcohol Calculator',
    description: 'Track your drinks and estimate your Blood Alcohol Content using the scientifically accurate Widmark equation.',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'BAC Simulator - Blood Alcohol Calculator',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BAC Simulator - Blood Alcohol Calculator',
    description: 'Track your drinks and estimate your BAC using the Widmark equation.',
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  themeColor: '#00BFAE',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ToastProvider>
          {children}
        </ToastProvider>
      </body>
    </html>
  );
}
