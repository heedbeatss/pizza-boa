'use client';

import Link from 'next/link';
import { useCart } from '@/lib/store';

export default function Header() {
  const totalItems = useCart((state) => state.items.reduce((sum, i) => sum + i.quantidade, 0));

  return (
    <header className="sticky top-0 z-50 bg-[#0a0a0a]/95 backdrop-blur-sm border-b border-[#581c87]/30">
      <div className="flex items-center justify-between px-4 py-3">
        <div>
          <h1 className="text-xl font-bold text-[#a855f7]">🍕 Pizza Boa</h1>
          <p className="text-xs text-[#a1a1a1]">Delivery</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs text-[#a1a1a1] bg-[#1a1a1a] px-3 py-1 rounded-full">
            🕐 45-60 min
          </span>
        </div>
      </div>
    </header>
  );
}
