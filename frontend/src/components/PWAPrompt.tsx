'use client';

import { useEffect, useState } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export default function PWAPrompt() {
  const [showBanner, setShowBanner] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);

  useEffect(() => {
    // Verifica se já está instalado
    if (window.matchMedia('(display-mode: standalone)').matches) return;

    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      setShowBanner(true);
    };

    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;
    await deferredPrompt.prompt();
    const result = await deferredPrompt.userChoice;
    if (result.outcome === 'accepted') setShowBanner(false);
    setDeferredPrompt(null);
  };

  if (!showBanner) return null;

  return (
    <div className="fixed bottom-20 left-4 right-4 z-50 animate-slide-up">
      <div className="bg-[#581c87] rounded-2xl p-4 flex items-center gap-3 shadow-lg shadow-[#581c87]/40">
        <div className="text-3xl">🍕</div>
        <div className="flex-1">
          <p className="font-bold text-sm">Instalar App</p>
          <p className="text-xs opacity-80">Adicione à tela inicial para acesso rápido</p>
        </div>
        <button
          onClick={handleInstall}
          className="px-4 py-2 bg-white text-[#581c87] rounded-xl font-bold text-sm hover:bg-gray-100 active:scale-95 transition-all"
        >
          Instalar
        </button>
        <button
          onClick={() => setShowBanner(false)}
          className="p-2 text-white/60 hover:text-white"
        >
          ✕
        </button>
      </div>
    </div>
  );
}
