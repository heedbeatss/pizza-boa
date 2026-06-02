import Header from '@/components/Header';
import CategoryNav from '@/components/CategoryNav';
import CardapioSection from '@/components/CardapioSection';
import CartButton from '@/components/CartButton';
import PWAPrompt from '@/components/PWAPrompt';
import { fetchCardapio } from '@/lib/api';
import type { Categoria } from '@/lib/store';

export default async function Home() {
  let categorias: Categoria[] = [];
  try {
    const data = await fetchCardapio();
    categorias = data.categorias || [];
  } catch (e) {
    console.error('Erro ao carregar cardápio:', e);
  }

  return (
    <main className="min-h-screen pb-24">
      <Header />
      <CategoryNav categorias={categorias} />

      <div className="px-4 pt-2">
        {categorias.map((cat) => (
          <CardapioSection key={cat.id} categoria={cat} />
        ))}
      </div>

      <CartButton />
      <PWAPrompt />
    </main>
  );
}
