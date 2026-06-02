'use client';

import { useState } from 'react';
import type { CardapioItem, Tamanho, CarrinhoItem, Categoria } from '@/lib/store';
import { useCart } from '@/lib/store';
import { fetchCardapio } from '@/lib/api';

interface Props {
  item: CardapioItem;
  onClose: () => void;
  onAdd: (item: CarrinhoItem) => void;
}

export default function ItemModal({ item, onClose, onAdd }: Props) {
  const [selectedTamanho, setSelectedTamanho] = useState<Tamanho>(item.tamanhos[0]);
  const [metade, setMetade] = useState(false);
  const [segundoItemId, setSegundoItemId] = useState<string | null>(null);
  const [quantidade, setQuantidade] = useState(1);
  const [categorias, setCategorias] = useState<Categoria[]>([]);

  // Carrega categorias para opção metade/metade
  useState(() => {
    fetchCardapio().then(d => setCategorias(d.categorias || [])).catch(() => {});
  });

  const isPizza = item.categoria === 'Pizzas Salgadas' || item.categoria === 'Pizzas Doces';

  const pizzasDisponiveis = categorias
    .flatMap(c => c.itens)
    .filter(i => i.id !== item.id);

  const segundoItem = pizzasDisponiveis.find(i => i.id === segundoItemId);
  const segundoPreco = segundoItem?.tamanhos.find(t => t.nome === selectedTamanho.nome)?.preco || segundoItem?.tamanhos[0]?.preco || 0;
  const precoMetade = metade ? Math.max(selectedTamanho.preco, segundoPreco) : selectedTamanho.preco;
  const precoFinal = precoMetade * quantidade;

  const handleAdd = () => {
    const carrinhoItem: CarrinhoItem = {
      id: `${item.id}-${Date.now()}`,
      item,
      tamanho: selectedTamanho,
      metade,
      segundoItem: segundoItem,
      quantidade,
      preco: metade ? precoMetade : selectedTamanho.preco,
    };
    onAdd(carrinhoItem);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center">
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/70" onClick={onClose} />

      {/* Modal */}
      <div className="relative w-full max-w-lg bg-[#1a1a1a] rounded-t-3xl animate-slide-up max-h-[90vh] overflow-y-auto">
        {/* Handle */}
        <div className="flex justify-center pt-3 pb-1">
          <div className="w-10 h-1 bg-[#581c87] rounded-full" />
        </div>

        <div className="px-5 pb-6">
          {/* Header */}
          <div className="flex justify-between items-start mt-2 mb-4">
            <div>
              <h2 className="text-xl font-bold">{item.nome}</h2>
              <p className="text-sm text-[#a1a1a1] mt-1">{item.descricao}</p>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-full hover:bg-[#581c87]/20 text-[#a1a1a1]"
            >
              ✕
            </button>
          </div>

          {/* Tamanho */}
          <div className="mb-5">
            <h3 className="text-sm font-semibold text-[#a855f7] mb-2">Tamanho</h3>
            <div className="grid grid-cols-3 gap-2">
              {item.tamanhos.map((t) => (
                <button
                  key={t.nome}
                  onClick={() => setSelectedTamanho(t)}
                  className={`p-3 rounded-xl text-center transition-all ${
                    selectedTamanho.nome === t.nome
                      ? 'bg-[#581c87] text-white'
                      : 'bg-[#0a0a0a] text-[#a1a1a1] hover:bg-[#581c87]/20'
                  }`}
                >
                  <div className="font-medium text-sm">{t.nome}</div>
                  {t.fatias && <div className="text-xs opacity-70">{t.fatias} fatias</div>}
                  <div className="font-bold text-[#a855f7] mt-1">R$ {t.preco.toFixed(2)}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Metade/Metade (só pizzas) */}
          {isPizza && (
            <div className="mb-5">
              <h3 className="text-sm font-semibold text-[#a855f7] mb-2">Inteira ou Metade?</h3>
              <div className="flex gap-2">
                <button
                  onClick={() => setMetade(false)}
                  className={`flex-1 p-3 rounded-xl text-center transition-all ${
                    !metade ? 'bg-[#581c87] text-white' : 'bg-[#0a0a0a] text-[#a1a1a1]'
                  }`}
                >
                  Inteira
                </button>
                <button
                  onClick={() => setMetade(true)}
                  className={`flex-1 p-3 rounded-xl text-center transition-all ${
                    metade ? 'bg-[#581c87] text-white' : 'bg-[#0a0a0a] text-[#a1a1a1]'
                  }`}
                >
                  Metade/Metade
                </button>
              </div>

              {metade && (
                <div className="mt-3">
                  <p className="text-xs text-[#a1a1a1] mb-2">Escolha o segundo sabor:</p>
                  <div className="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto">
                    {pizzasDisponiveis.map((p) => (
                      <button
                        key={p.id}
                        onClick={() => setSegundoItemId(p.id)}
                        className={`p-2 rounded-lg text-left text-sm transition-all ${
                          segundoItemId === p.id
                            ? 'bg-[#581c87] text-white'
                            : 'bg-[#0a0a0a] text-[#a1a1a1] hover:bg-[#581c87]/20'
                        }`}
                      >
                        {p.nome}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Quantidade */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-[#a855f7] mb-2">Quantidade</h3>
            <div className="flex items-center gap-4 justify-center">
              <button
                onClick={() => setQuantidade(Math.max(1, quantidade - 1))}
                className="w-10 h-10 rounded-full bg-[#0a0a0a] text-[#a855f7] text-xl font-bold hover:bg-[#581c87]/20"
              >
                −
              </button>
              <span className="text-2xl font-bold w-12 text-center">{quantidade}</span>
              <button
                onClick={() => setQuantidade(quantidade + 1)}
                className="w-10 h-10 rounded-full bg-[#581c87] text-white text-xl font-bold hover:bg-[#7e22ce]"
              >
                +
              </button>
            </div>
          </div>

          {/* Botão adicionar */}
          <button
            onClick={handleAdd}
            disabled={metade && !segundoItemId}
            className="w-full py-4 rounded-2xl bg-[#581c87] text-white font-bold text-lg hover:bg-[#7e22ce] active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Adicionar — R$ {precoFinal.toFixed(2)}
          </button>
        </div>
      </div>
    </div>
  );
}
