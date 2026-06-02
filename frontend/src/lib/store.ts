import { create } from 'zustand';

export interface Tamanho {
  nome: string;
  fatias: number | null;
  preco: number;
}

export interface CardapioItem {
  id: string;
  nome: string;
  descricao: string;
  tamanhos: Tamanho[];
}

export interface Categoria {
  id: string;
  nome: string;
  icone: string;
  itens: CardapioItem[];
}

export interface CarrinhoItem {
  id: string;
  item: CardapioItem;
  tamanho: Tamanho;
  metade: boolean;
  segundoItem?: CardapioItem;
  segundoTamanho?: Tamanho;
  quantidade: number;
  preco: number;
}

export interface Endereco {
  rua: string;
  numero: string;
  bairro: string;
  complemento: string;
  referencia: string;
}

interface CartStore {
  items: CarrinhoItem[];
  endereco: Endereco;
  pagamento: string;
  observacao: string;
  addItem: (item: CarrinhoItem) => void;
  removeItem: (index: number) => void;
  updateQuantidade: (index: number, qtd: number) => void;
  setEndereco: (endereco: Endereco) => void;
  setPagamento: (pagamento: string) => void;
  setObservacao: (obs: string) => void;
  clearCart: () => void;
  total: number;
  entrega: number;
  totalFinal: number;
}

const DELIVERY_FEE = 5.00;

export const useCart = create<CartStore>((set, get) => ({
  items: [],
  endereco: { rua: '', numero: '', bairro: '', complemento: '', referencia: '' },
  pagamento: 'dinheiro',
  observacao: '',

  addItem: (item) => set((state) => ({ items: [...state.items, item] })),

  removeItem: (index) => set((state) => ({
    items: state.items.filter((_, i) => i !== index)
  })),

  updateQuantidade: (index, qtd) => set((state) => ({
    items: state.items.map((item, i) =>
      i === index ? { ...item, quantidade: Math.max(1, qtd) } : item
    )
  })),

  setEndereco: (endereco) => set({ endereco }),
  setPagamento: (pagamento) => set({ pagamento }),
  setObservacao: (observacao) => set({ observacao }),
  clearCart: () => set({ items: [], observacao: '' }),

  get total() {
    return get().items.reduce((sum, i) => sum + i.preco * i.quantidade, 0);
  },

  get entrega() {
    const total = get().items.reduce((sum, i) => sum + i.preco * i.quantidade, 0);
    return total >= 50 ? 0 : DELIVERY_FEE;
  },

  get totalFinal() {
    const total = get().items.reduce((sum, i) => sum + i.preco * i.quantidade, 0);
    const entrega = total >= 50 ? 0 : DELIVERY_FEE;
    return total + entrega;
  }
}));
