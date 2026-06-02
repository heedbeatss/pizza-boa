import type { Metadata, Viewport } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Pizza Boa - Delivery',
  description: 'Peça sua pizza pelo app!',
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: '#581c87',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="bg-[#0a0a0a] text-white min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
