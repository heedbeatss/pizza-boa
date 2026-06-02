'use client';

import { useState, useRef, useEffect } from 'react';
import type { Categoria } from '@/lib/store';

interface Props {
  categorias: Categoria[];
}

export default function CategoryNav({ categorias }: Props) {
  const [active, setActive] = useState(categorias[0]?.id || '');
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollTo = (id: string) => {
    setActive(id);
    const el = document.getElementById(`cat-${id}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <div
      ref={scrollRef}
      className="sticky top-[57px] z-40 bg-[#0a0a0a]/95 backdrop-blur-sm border-b border-[#581c87]/20 overflow-x-auto"
    >
      <div className="flex gap-2 px-4 py-3 min-w-max">
        {categorias.map((cat) => (
          <button
            key={cat.id}
            onClick={() => scrollTo(cat.id)}
            className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
              active === cat.id
                ? 'bg-[#581c87] text-white shadow-lg shadow-[#581c87]/30'
                : 'bg-[#1a1a1a] text-[#a1a1a1] hover:bg-[#581c87]/20'
            }`}
          >
            {cat.icone} {cat.nome}
          </button>
        ))}
      </div>
    </div>
  );
}
