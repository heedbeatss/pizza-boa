#!/bin/bash
# Script para gerar o app iOS
# Execute no Mac com Xcode instalado

cd /Users/seu-usuario/pizza-delivery/mobile

echo "Sincronizando Capacitor..."
npx cap sync ios

echo "Abrindo Xcode..."
npx cap open ios

echo ""
echo "No Xcode:"
echo "  1. Selecione 'Any iOS Device' como target"
echo "  2. Va em Product -> Archive"
echo "  3. Clique em 'Distribute App'"
echo "  4. Escolha 'App Store Connect' ou 'Ad Hoc'"
