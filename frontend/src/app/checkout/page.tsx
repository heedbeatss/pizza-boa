'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useCart } from '@/lib/store';
import { createPedido } from '@/lib/api';

const PAGAMENTOS = [
  { id: 'dinheiro', nome: 'Dinheiro', icone: '💵' },
  { id: 'pix', nome: 'PIX', icone: '📱' },
  { id: 'cartao-credito', nome: 'Crédito', icone: '💳' },
  { id: 'cartao-debito', nome: 'Débito', icone: '💳' },
];

export default function CheckoutPage() {
  const router = useRouter();
  const items = useCart((state) => state.items);
  const total = useCart((state) => state.total);
  const entrega = useCart((state) => state.entrega);
  const totalFinal = useCart((state) => state.totalFinal);
  const endereco = useCart((state) => state.endereco);
  const setEndereco = useCart((state) => state.setEndereco);
  const pagamento = useCart((state) => state.pagamento);
  const setPagamento = useCart((state) => state.setPagamento);
  const observacao = useCart((state) => state.observacao);
  const setObservacao = useCart((state) => state.setObservacao);
  const clearCart = useCart((state) => state.clearCart);

  const [nome, setNome] = useState('');
  const [loading, setLoading] = useState(false);
  const [sucesso, setSucesso] = useState(false);
  const [pedidoId, setPedidoId] = useState<number | null>(null);
  const [erro, setErro] = useState('');

  if (items.length === 0 && !sucesso) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center">
          <p className="text-6xl mb-4">🛒</p>
          <h1 className="text-xl font-bold mb-2">Carrinho vazio</h1>
          <p className="text-[#a1a1a1] mb-6">Adicione itens do cardápio para continuar</p>
          <button
            onClick={() => router.push('/')}
            className="px-6 py-3 rounded-xl bg-[#581c87] text-white font-bold"
          >
            Ver Cardápio
          </button>
        </div>
      </div>
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nome.trim()) { setErro('Informe seu nome'); return; }
    if (!endereco.rua || !endereco.numero || !endereco.bairro) {
      setErro('Preencha o endereço completo'); return;
    }

    setLoading(true);
    setErro('');

    try {
      const pedido = await createPedido({
        itens: items.map(i => ({
          nome: i.metade ? `½ ${i.item.nome} / ½ ${i.segundoItem?.nome}` : i.item.nome,
          tamanho: i.tamanho.nome,
          preco: i.preco,
          quantidade: i.quantidade,
        })),
        endereco: `${endereco.rua}, ${endereco.numero}${endereco.complemento ? ` - ${endereco.complemento}` : ''} - ${endereco.bairro}${endereco.referencia ? ` (${endereco.referencia})` : ''}`,
        pagamento,
        observacao,
        nomeCliente: nome,
      });

      setPedidoId(pedido.id);
      setSucesso(true);
      clearCart();
    } catch (err: any) {
      setErro(err.message || 'Erro ao enviar pedido');
    } finally {
      setLoading(false);
    }
  };

  // Tela de sucesso
  if (sucesso) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center animate-fade-in">
          <p className="text-6xl mb-4">🎉</p>
          <h1 className="text-2xl font-bold text-green-400 mb-2">Pedido Confirmado!</h1>
          <p className="text-[#a1a1a1] mb-2">Pedido <span className="text-[#a855f7] font-bold">#{pedidoId}</span></p>
          <p className="text-sm text-[#a1a1a1] mb-6">
            Tempo estimado: <span className="text-white font-bold">45-60 minutos</span>
          </p>

          {/* Botão WhatsApp */}
          <a
            href={`https://wa.me/5519999999999?text=Olá! Fiz o pedido #${pedidoId} pelo app. Podem confirmar?`}
            target="_blank"
            rel="noopener"
            className="inline-block px-6 py-3 rounded-xl bg-green-600 text-white font-bold mb-4 hover:bg-green-700 transition-all"
          >
            📱 Confirmar pelo WhatsApp
          </a>

          <br />
          <button
            onClick={() => router.push('/')}
            className="px-6 py-3 rounded-xl bg-[#581c87] text-white font-bold hover:bg-[#7e22ce] transition-all"
          >
            Voltar ao Cardápio
          </button>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="min-h-screen pb-8">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-[#0a0a0a]/95 backdrop-blur-sm border-b border-[#581c87]/20 px-4 py-3">
        <button
          type="button"
          onClick={() => router.back()}
          className="text-[#a855f7] font-medium text-sm mb-1"
        >
          ← Voltar
        </button>
        <h1 className="text-lg font-bold">Finalizar Pedido</h1>
      </header>

      <div className="px-4 pt-4 space-y-5">
        {/* Dados pessoais */}
        <section>
          <h2 className="text-sm font-semibold text-[#a855f7] mb-3">👤 Seus Dados</h2>
          <input
            type="text"
            placeholder="Seu nome"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            className="w-full p-4 rounded-xl bg-[#1a1a1a] text-white placeholder-[#a1a1a1] border border-[#581c87]/20 focus:border-[#581c87] outline-none transition-all"
          />
        </section>

        {/* Endereço */}
        <section>
          <h2 className="text-sm font-semibold text-[#a855f7] mb-3">📍 Endereço de Entrega</h2>
          <div className="space-y-3">
            <div className="grid grid-cols-3 gap-3">
              <input
                type="text"
                placeholder="Rua"
                value={endereco.rua}
                onChange={(e) => setEndereco({ ...endereco, rua: e.target.value })}
                className="col-span-2 p-3 rounded-xl bg-[#1a1a1a] text-white placeholder-[#a1a1a1] border border-[#581c87]/20 focus:border-[#581c87] outline-none text-sm"
              />
              <input
                type="text"
                placeholder="Nº"
                value={endereco.numero}
                onChange={(e) => setEndereco({ ...endereco, numero: e.target.value })}
                className="p-3 rounded-xl bg-[#1a1a1a] text-white placeholder-[#a1a1a1] border border-[#581c87]/20 focus:border-[#581c87] outline-none text-sm"
              />
            </div>
            <input
              type="text"
              placeholder="Bairro"
              value={endereco.bairro}
              onChange={(e) => setEndereco({ ...endereco, bairro: e.target.value })}
              className="w-full p-3 rounded-xl bg-[#1a1a1a] text-white placeholder-[#a1a1a1] border border-[#581c87]/20 focus:border-[#581c87] outline-none text-sm"
            />
            <input
              type="text"
              placeholder="Complemento (opcional)"
              value={endereco.complemento}
              onChange={(e) => setEndereco({ ...endereco, complemento: e.target.value })}
              className="w-full p-3 rounded-xl bg-[#1a1a1a] text-white placeholder-[#a1a1a1] border border-[#581c87]/20 focus:border-[#581c87] outline-none text-sm"
            />
            <input
              type="text"
              placeholder="Ponto de referência (opcional)"
              value={endereco.referencia}
              onChange={(e) => setEndereco({ ...endereco, referencia: e.target.value })}
              className="w-full p-3 rounded-xl bg-[#1a1a1a] text-white placeholder-[#a1a1a1] border border-[#581c87]/20 focus:border-[#581c87] outline-none text-sm"
            />
          </div>
        </section>

        {/* Pagamento */}
        <section>
          <h2 className="text-sm font-semibold text-[#a855f7] mb-3">💳 Forma de Pagamento</h2>
          <div className="grid grid-cols-2 gap-2">
            {PAGAMENTOS.map((p) => (
              <button
                key={p.id}
                type="button"
                onClick={() => setPagamento(p.id)}
                className={`p-3 rounded-xl text-center transition-all ${
                  pagamento === p.id
                    ? 'bg-[#581c87] text-white'
                    : 'bg-[#1a1a1a] text-[#a1a1a1] hover:bg-[#581c87]/20'
                }`}
              >
                <span className="text-lg">{p.icone}</span>
                <p className="text-sm font-medium mt-1">{p.nome}</p>
              </button>
            ))}
          </div>
        </section>

        {/* Observação */}
        <section>
          <h2 className="text-sm font-semibold text-[#a855f7] mb-3">📝 Observação</h2>
          <textarea
            placeholder="Alguma observação? (ex: sem cebola, troco para...)"
            value={observacao}
            onChange={(e) => setObservacao(e.target.value)}
            rows={3}
            className="w-full p-3 rounded-xl bg-[#1a1a1a] text-white placeholder-[#a1a1a1] border border-[#581c87]/20 focus:border-[#581c87] outline-none text-sm resize-none"
          />
        </section>

        {/* Resumo */}
        <section className="bg-[#1a1a1a] rounded-2xl p-4">
          <h3 className="font-bold mb-3">Resumo do Pedido</h3>
          <div className="space-y-2 mb-3">
            {items.map((item) => (
              <div key={item.id} className="flex justify-between text-sm">
                <span className="text-[#a1a1a1]">
                  {item.quantidade}x {item.metade ? `½${item.item.nome}/½${item.segundoItem?.nome}` : item.item.nome}
                  <span className="text-xs"> ({item.tamanho.nome})</span>
                </span>
                <span>R$ {(item.preco * item.quantidade).toFixed(2)}</span>
              </div>
            ))}
          </div>
          <div className="border-t border-[#581c87]/30 pt-3 space-y-1">
            <div className="flex justify-between text-sm">
              <span className="text-[#a1a1a1]">Entrega</span>
              <span>{entrega === 0 ? <span className="text-green-400">Grátis</span> : `R$ ${entrega.toFixed(2)}`}</span>
            </div>
            <div className="flex justify-between font-bold text-lg">
              <span>Total</span>
              <span className="text-[#a855f7]">R$ {totalFinal.toFixed(2)}</span>
            </div>
          </div>
        </section>

        {/* Erro */}
        {erro && (
          <p className="text-red-400 text-sm text-center bg-red-900/20 p-3 rounded-xl">
            {erro}
          </p>
        )}

        {/* Botão */}
        <button
          type="submit"
          disabled={loading}
          className="w-full py-4 rounded-2xl bg-[#581c87] text-white font-bold text-lg shadow-lg shadow-[#581c87]/30 hover:bg-[#7e22ce] active:scale-[0.98] transition-all disabled:opacity-50"
        >
          {loading ? 'Enviando...' : `Confirmar Pedido — R$ ${totalFinal.toFixed(2)}`}
        </button>
      </div>
    </form>
  );
}
