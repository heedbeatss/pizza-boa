'use client';

import { useState } from 'react';
import type { Categoria, CardapioItem, Tamanho, CarrinhoItem } from '@/lib/store';
import { useCart } from '@/lib/store';
import ItemModal from './ItemModal';

interface Props {
  categoria: Categoria;
}

export default function CardapioSection({ categoria }: Props) {
  const [selectedItem, setSelectedItem] = useState<CardapioItem | null>(null);
  const addItem = useCart((state) => state.addItem);

  const handleAdd = (carrinhoItem: CarrinhoItem) => {
    addItem(carrinhoItem);
    setSelectedItem(null);
  };

  return (
    <>
      <section id={`cat-${categoria.id}`} className="pt-6 pb-4">
        <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
          <span>{categoria.icone}</span>
          {categoria.nome}
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {categoria.itens.map((item) => (
            <button
              key={item.id}
              onClick={() => setSelectedItem(item)}
              className="bg-[#1a1a1a] rounded-2xl p-4 text-left hover:bg-[#581c87]/20 transition-all active:scale-[0.98] border border-[#581c87]/10 hover:border-[#581c87]/40"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="font-semibold text-[#e2e8f0]">{item.nome}</h3>
                  <p className="text-sm text-[#a1a1a1] mt-1 line-clamp-2">{item.descricao}</p>
                </div>
              </div>
              <div className="mt-3 flex items-center gap-2">
                <span className="text-[#a855f7] font-bold text-lg">
                  R$ {item.tamanhos[0].preco.toFixed(2)}
                </span>
                {item.tamanhos.length > 1 && (
                  <span className="text-xs text-[#a1a1a1]">
                    — R$ {item.tamanhos[item.tamanhos.length - 1].preco.toFixed(2)}
                  </span>
                )}
              </div>
            </button>
          ))}
        </div>
      </section>

      {selectedItem && (
        <ItemModal
          item={selectedItem}
          categoriaNome={categoria.nome}
          onClose={() => setSelectedItem(null)}
          onAdd={handleAdd}
        />
      )}
    </>
  );
}
