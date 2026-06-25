# 🍕 Pizza Boa — Guia de Clonagem para Nova Pizzaria

Este guia explica como criar um novo app de delivery baseado no Pizza Boa para outra pizzaria.

## � Método Rápido (Script Automático)

```bash
python3 scripts/new_pizzaria.py \
  --nome "Pizza Nova" \
  --app-id "com.pizzanova.app" \
  --api-url "https://script.google.com/macros/s/SEU_GAS_ID/exec" \
  --sheet-id "SEU_SHEET_ID" \
  --whatsapp "19911112222" \
  --cor-primaria "#e11d48" \
  --cor-fundo "#1a1a1a"
```

O script automaticamente:
- Copia o template
- Atualiza config.js (nome, API, sheetId, WhatsApp, cores)
- Atualiza capacitor.config.json (appId, nome)
- Atualiza strings.xml (app name, package)
- Atualiza build.gradle (namespace, applicationId)
- Atualiza package.json (nome, descrição)
- Gera ícones com a cor da pizzaria em todas as resoluções
- Opcional: roda `npm install` + `npx cap sync android`

## 📋 Método Manual (Passo a Passo)

### 1. Pré-requisitos

- Node.js 18+ instalado
- Android SDK instalado (ANDROID_HOME configurado)
- Python 3.8+ (para geração de ícones)
- Pillow: `pip install Pillow`

### 2. Clone o template

```bash
git clone https://github.com/SEU_USER/pizza-boa.git NOME_DA_PIZZARIA
cd NOME_DA_PIZZARIA
```

### 3. Crie a infraestrutura Google

1. Crie uma nova planilha Google Sheets
2. Vá em Extensões > Apps Script
3. Cole o código do GAS (ver pasta `gas/`)
4. Substitua `sheetId` pelo ID da nova planilha
5. Faça deploy: Implantação > Nova implantação > App da Web
6. Copie a URL de acesso

### 4. Edite os arquivos de configuração

| Arquivo | O que mudar |
|---------|-------------|
| `www/config.js` | nome, slogan, apiUrl, sheetId, whatsapp, corPrimaria, corAccent, corFundo, corSurface, corTexto, pedidoMinimo, msgs |
| `capacitor.config.json` | appId, nome, backgroundColor, plugins statusBar/splash bg |
| `android/app/src/main/res/values/strings.xml` | app_name, package_name |
| `android/app/build.gradle` | namespace, applicationId |
| `package.json` | name, description |
| `android/app/src/main/res/drawable/ic_launcher_background.xml` | cor de fundo do background |

### 5. Gere os ícones

```bash
python3 scripts/generate_icons.py --cor "#e11d48" --res ./android/app/src/main/res
```

Ou substitua manualmente os PNGs em `mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/`

### 6. Build do APK

```bash
npx cap sync android
cd android
./gradlew assembleDebug
```

### 7. Instale no celular

```bash
adb install android/app/build/outputs/apk/debug/app-debug.apk
```

### 8. Deploy do site (GitHub Pages)

```bash
git add -A
git commit -m "NOME_DA_PIZZARIA - inicial"
git push
```

## � Estrutura do Projeto

```
pizza-boa/
├── www/                          # Web assets (APK source + browser)
│   ├── index.html                # APK welcome screen + JS principal
│   ├── app.html                  # Versão browser (desenvolvimento)
│   ├── config.js                 # ⭐ Configuração por pizzaria
│   ├── capacitor.js              # Runtime do Capacitor
│   └── plugins/                  # Plugins JS (local-notifications, etc)
├── android/                      # Projeto Android nativo
│   ├── app/
│   │   ├── build.gradle          # ⭐ package name (namespace, applicationId)
│   │   └── src/main/
│   │       ├── res/
│   │       │   └── values/
│   │       │       ├── strings.xml   # ⭐ App name, package name
│   │       │       └── ic_launcher_background.xml
│   │       └── AndroidManifest.xml
│   └── capacitor.config.json     # ⭐ Nome, appId, plugins
├── gas/                          # Google Apps Script (backend)
│   └── index.js
├── scripts/
│   ├── new_pizzaria.py           # ⭐ Script de clonagem automática
│   └── generate_icons.py        # ⭐ Gerador de ícones
├── package.json
└── README.md
```

## � Personalização

### Cores

No `www/config.js`, ajuste:
- `corPrimaria`: Cor principal (usada em botões, header, ícone)
- `corAccent`: Cor de destaque
- `corFundo`: Cor de fundo
- `corSurface`: Cor dos cards/modais

### Ícone

Substitua os PNGs em `mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/`:

| Pasta | Resolução | Uso |
|-------|-----------|-----|
| mipmap-mdpi | 48x48 | Launcher Android <= 5 |
| mipmap-hdpi | 72x72 | Launcher Android <= 5 |
| mipmap-xhdpi | 96x96 | Launcher Android <= 5 |
| mipmap-xxhdpi | 144x144 | Launcher Android <= 5 |
| mipmap-xxxhdpi | 192x192 | Launcher Android <= 5 |
| mipmap-anydpi-v26 | adaptive | Android 8+ (usa vectors) |

### Cardápio

Edite o objeto `CARDAPIO` em `www/index.html`:
- Categorias: salgadas, especiais, doces, bebidas
- Itens: nome, descrição, tamanhos (P/M/G) com preços

### Google Apps Script (GAS)

O backend é um script do Google Apps Script vinculado a uma planilha. Estrutura:

1. Planilha com aba "Pedidos" (colunas: id, nome, telefone, itens, status, data)
2. Planilha com aba "Config" (horário, taxas, etc.)
3. GAS com funções: `doPost` (novoPedido, pedidos, atualizarStatus, cardapio, config)

### WhatsApp

A função `enviarWhatsApp()` em `www/index.html` abre o WhatsApp com mensagem pré-preenchida. O número destino vem de `APP_CONFIG.whatsapp`.

## 🔧 Solução de Problemas

| Problema | Causa | Solução |
|----------|-------|---------|
| `Failed to resolve module specifier` | Plugin JS não carregado | Copie `node_modules/@capacitor/*/dist/esm/` para `www/plugins/` |
| Ícone não aparece | Resources cacheados | Remova `android/app/build` e rebuild |
| Notificação não chega | Permissão negada | Android 13+ precisa aceitar no welcome screen |
| `local.properties` missing | SDK path | Crie `android/local.properties` com `sdk.dir=...` |
| Sheet ID inválido | Google Sheets | Crie nova planilha e copie o ID da URL |
| APK muito grande | Build debug | Normal. Para release, configure signing |

## � Preparação para Play Store

1. Configure signing no `android/app/build.gradle`
2. Gere AAB: `./gradlew bundleRelease`
3. Crie conta developer Google Play
4. Submete o AAB via Play Console

## 📝 Notas

- `www/index.html` é a fonte do APK (web assets).
- `app.html` é para desenvolvimento no navegador.
- Mantenha ambos sincronizados quando alterar o código JS.
- O match de pedidos é feito por data/horário ±5s e ±30s (nunca por ID).
