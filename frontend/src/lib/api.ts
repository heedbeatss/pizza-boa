export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000';

export async function fetchCardapio() {
  const res = await fetch(`${API_URL}/api/cardapio`);
  if (!res.ok) throw new Error('Erro ao carregar cardápio');
  return res.json();
}

export async function fetchConfig() {
  const res = await fetch(`${API_URL}/api/config`);
  if (!res.ok) throw new Error('Erro ao carregar config');
  return res.json();
}

export async function createPedido(data: {
  itens: any[];
  endereco: string;
  pagamento: string;
  observacao: string;
  nomeCliente: string;
}) {
  const res = await fetch(`${API_URL}/api/pedidos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Erro ao criar pedido');
  return res.json();
}

export async function fetchPedido(id: number) {
  const res = await fetch(`${API_URL}/api/pedidos/${id}`);
  if (!res.ok) throw new Error('Pedido não encontrado');
  return res.json();
}
