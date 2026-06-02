# 🍕 Pizza Delivery - Multi-Pizzaria

App de cardápio e delivery para pizzarias.

## Estrutura

```
pizza-delivery/
├── frontend/          # Next.js - Interface do app
├── mobile/           # Capacitor - Wrapper para Android/iOS
├── backend/          # Express - API + Webhook WhatsApp
├── theme/            # Config customizável por pizzaria
└── data/             # Banco de dados JSON
```

## 🚀 Como usar

### 1. Instalar dependências

```bash
# Backend
cd backend && npm install

# Frontend
cd frontend && npm install
```

### 2. Configurar variáveis de ambiente

```bash
# Backend
cp backend/.env.example backend/.env
# Edite .env com seus dados
```

### 3. Rodar em desenvolvimento

```bash
# Terminal 1 - Backend
cd backend && npm run dev

# Terminal 2 - Frontend
cd frontend && npm run dev
```

Frontend: http://localhost:3001
API: http://localhost:3000

## 🎨 Customizar para outra pizzaria

Para criar um app para outra pizzaria, edite esses arquivos:

### 1. `theme/config.ts`
```typescript
business: {
  name: "Nova Pizzaria",
  slogan: "Seu slogan aqui",
  colors: {
    primary: "#sua-cor",
    // ...
  }
}
```

### 2. `data/cardapio.json`
```json
{
  "categorias": [
    {
      "id": "pizzas",
      "nome": "Pizzas",
      "itens": [...]
    }
  ]
}
```

### 3. `backend/.env`
```
BUSINESS_NAME=Nova Pizzaria
WHATSAPP_TOKEN=seu_token
WHATSAPP_PHONE_ID=seu_phone_id
```

### 4. Substituir logo
Coloque a nova logo em `frontend/public/logo.png`

## 📱 Build para mobile (Capacitor)

```bash
cd frontend
npm run build

cd ../mobile
npx cap init "Pizza Boa" "com.pizzaboa.app"
npx cap add android   # ou ios
npx cap sync
npx cap open android  # abre no Android Studio
```

## 📦 Deploy

### Backend (VPS/Railway/Render)
```bash
cd backend
npm install
npm start
```

### Frontend (Vercel)
```bash
cd frontend
npx vercel
```

## 📋 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/cardapio | Lista cardápio completo |
| GET | /api/cardapio/:id | Busca item específico |
| GET | /api/config | Config da pizzaria |
| POST | /api/pedidos | Cria novo pedido |
| GET | /api/pedidos | Lista pedidos |
| GET | /api/pedidos/:id | Busca pedido por ID |
| PUT | /api/pedidos/:id/status | Atualiza status |
| GET | /health | Health check |

## 🔗 Webhook WhatsApp

Configure no Meta Developer Console:
- Callback URL: `https://sua-url.com/webhook`
- Verify Token: o valor de WEBHOOK_VERIFY_TOKEN no .env

## 📝 Licença

Uso livre para pizzarias.
