import type { Metadata, Viewport } from 'next';
import './globals.css';
import { ToastProvider } from '@/components/ui/Toast';

export const metadata: Metadata = {
  title: 'BAC Simulator - Blood Alcohol Calculator',
  description: 'Scientifically accurate blood alcohol content simulator using the Widmark equation',
  keywords: ['BAC', 'blood alcohol', 'calculator', 'drunk driving', 'alcohol metabolism'],
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
