'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useCart } from '@/lib/store';

export default function CartButton() {
  const items = useCart((state) => state.items);
  const total = useCart((state) => state.total);
  const entrega = useCart((state) => state.entrega);
  const totalFinal = useCart((state) => state.totalFinal);
  const totalItems = items.reduce((sum, i) => sum + i.quantidade, 0);
  const [showCart, setShowCart] = useState(false);
  const removeItem = useCart((state) => state.removeItem);
  const updateQuantidade = useCart((state) => state.updateQuantidade);

  if (totalItems === 0) return null;

  return (
    <>
      {/* Botão flutuante */}
      <div className="fixed bottom-0 left-0 right-0 z-40 p-4 bg-gradient-to-t from-[#0a0a0a] to-transparent">
        <button
          onClick={() => setShowCart(true)}
          className="w-full py-4 rounded-2xl bg-[#581c87] text-white font-bold text-lg shadow-lg shadow-[#581c87]/30 hover:bg-[#7e22ce] active:scale-[0.98] transition-all flex items-center justify-between px-6"
        >
          <span className="flex items-center gap-2">
            🛒 {totalItems} {totalItems === 1 ? 'item' : 'itens'}
          </span>
          <span>R$ {totalFinal.toFixed(2)}</span>
        </button>
      </div>

      {/* Modal do carrinho */}
      {showCart && (
        <div className="fixed inset-0 z-50 flex items-end justify-center">
          <div className="absolute inset-0 bg-black/70" onClick={() => setShowCart(false)} />
          <div className="relative w-full max-w-lg bg-[#1a1a1a] rounded-t-3xl animate-slide-up max-h-[85vh] overflow-y-auto">
            <div className="flex justify-center pt-3 pb-1">
              <div className="w-10 h-1 bg-[#581c87] rounded-full" />
            </div>

            <div className="px-5 pb-6">
              <div className="flex justify-between items-center mt-2 mb-4">
                <h2 className="text-xl font-bold">🛒 Seu Pedido</h2>
                <button
                  onClick={() => setShowCart(false)}
                  className="p-2 rounded-full hover:bg-[#581c87]/20 text-[#a1a1a1]"
                >
                  ✕
                </button>
              </div>

              {/* Itens */}
              <div className="space-y-3 mb-5">
                {items.map((cartItem, index) => (
                  <div
                    key={cartItem.id}
                    className="bg-[#0a0a0a] rounded-xl p-3 flex items-center gap-3"
                  >
                    <div className="flex-1">
                      <p className="font-medium text-sm">
                        {cartItem.metade
                          ? `½ ${cartItem.item.nome} / ½ ${cartItem.segundoItem?.nome || '?'}`
                          : cartItem.item.nome}
                      </p>
                      <p className="text-xs text-[#a1a1a1]">
                        {cartItem.tamanho.nome} {cartItem.tamanho.fatias ? `(${cartItem.tamanho.fatias}f)` : ''}
                      </p>
                      <p className="text-[#a855f7] font-bold text-sm mt-1">
                        R$ {(cartItem.preco * cartItem.quantidade).toFixed(2)}
                      </p>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => updateQuantidade(index, cartItem.quantidade - 1)}
                        className="w-8 h-8 rounded-full bg-[#1a1a1a] text-[#a855f7] font-bold"
                      >
                        −
                      </button>
                      <span className="w-6 text-center font-bold">{cartItem.quantidade}</span>
                      <button
                        onClick={() => updateQuantidade(index, cartItem.quantidade + 1)}
                        className="w-8 h-8 rounded-full bg-[#581c87] text-white font-bold"
                      >
                        +
                      </button>
                      <button
                        onClick={() => removeItem(index)}
                        className="w-8 h-8 rounded-full bg-red-900/30 text-red-400 font-bold ml-1"
                      >
                        🗑
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              {/* Resumo */}
              <div className="bg-[#0a0a0a] rounded-xl p-4 mb-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-[#a1a1a1]">Subtotal</span>
                  <span>R$ {total.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[#a1a1a1]">Entrega</span>
                  <span>{entrega === 0 ? <span className="text-green-400">Grátis!</span> : `R$ ${entrega.toFixed(2)}`}</span>
                </div>
                {entrega === 0 && (
                  <p className="text-xs text-green-400">🎉 Parabéns! Entrega grátis!
                  </p>
                )}
                <div className="border-t border-[#581c87]/30 pt-2 flex justify-between font-bold">
                  <span>Total</span>
                  <span className="text-[#a855f7]">R$ {totalFinal.toFixed(2)}</span>
                </div>
              </div>

              {/* Botão finalizar */}
              <Link href="/checkout">
                <button
                  onClick={() => setShowCart(false)}
                  className="w-full py-4 rounded-2xl bg-[#581c87] text-white font-bold text-lg hover:bg-[#7e22ce] active:scale-[0.98] transition-all"
                >
                  Finalizar Pedido →
                </button>
              </Link>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
