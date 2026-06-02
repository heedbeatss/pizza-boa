/**
 * Servidor Principal - Pizza Delivery
 * 
 * Combina:
 * - API REST pro frontend (cardápio, pedidos, checkout)
 * - Webhook WhatsApp (bot de mensagens)
 */
import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import dotenv from 'dotenv';
import { readdirSync, readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

dotenv.config({ path: join(dirname(fileURLToPath(import.meta.url)), '..', '.env') });

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, '..', '..', 'data');

// ============ DATABASE (JSON) ============
function loadJSON(filename) {
  const path = join(DATA_DIR, filename);
  if (!existsSync(path)) return null;
  return JSON.parse(readFileSync(path, 'utf-8'));
}

function saveJSON(filename, data) {
  writeFileSync(join(DATA_DIR, filename), JSON.stringify(data, null, 2));
}

// Carrega cardápio
const cardapio = loadJSON('cardapio.json');

// Pedidos em memória (persistidos em JSON)
let pedidos = loadJSON('pedidos.json') || [];
let nextId = pedidos.length > 0 ? Math.max(...pedidos.map(p => p.id)) + 1 : 1;

function savePedidos() {
  saveJSON('pedidos.json', pedidos);
}

// Sessões do bot WhatsApp
const sessions = new Map();

// ============ APP ============
const app = express();
app.use(cors());
app.use(bodyParser.json());

const PORT = process.env.PORT || 3000;

// ============ API - CARDÁPIO ============

// Listar cardápio completo
app.get('/api/cardapio', (req, res) => {
  res.json(cardapio);
});

// Buscar item específico
app.get('/api/cardapio/:id', (req, res) => {
  const id = req.params.id;
  for (const cat of cardapio.categorias) {
    const item = cat.itens.find(i => i.id === id);
    if (item) return res.json({ ...item, categoria: cat.nome, categoriaId: cat.id });
  }
  res.status(404).json({ error: 'Item não encontrado' });
});

// ============ API - PEDIDOS ============

// Criar pedido
app.post('/api/pedidos', (req, res) => {
  const { itens, endereco, pagamento, observacao, nomeCliente } = req.body;

  if (!itens || itens.length === 0) {
    return res.status(400).json({ error: 'Pedido vazio' });
  }
  if (!endereco) {
    return res.status(400).json({ error: 'Endereço obrigatório' });
  }

  const total = itens.reduce((sum, i) => sum + i.preco, 0);
  const entrega = parseFloat(process.env.DELIVERY_FEE || '5.00');

  const pedido = {
    id: nextId++,
    itens,
    endereco,
    pagamento: pagamento || 'dinheiro',
    observacao: observacao || '',
    nomeCliente: nomeCliente || 'Cliente',
    total,
    entrega,
    totalFinal: total + entrega,
    status: 'recebido',
    criadoEm: new Date().toISOString(),
    historico: [{ status: 'recebido', data: new Date().toISOString(), obs: 'Pedido criado pelo app' }]
  };

  pedidos.push(pedido);
  savePedidos();

  // Notifica via WhatsApp
  notifyWhatsApp(pedido);

  res.status(201).json(pedido);
});

// Listar pedidos
app.get('/api/pedidos', (req, res) => {
  const { status, telefone } = req.query;
  let result = [...pedidos].sort((a, b) => b.id - a.id);
  if (status) result = result.filter(p => p.status === status);
  if (telefone) result = result.filter(p => p.telefone === telefone);
  res.json({ total: result.length, pedidos: result });
});

// Buscar pedido por ID
app.get('/api/pedidos/:id', (req, res) => {
  const pedido = pedidos.find(p => p.id === parseInt(req.params.id));
  if (!pedido) return res.status(404).json({ error: 'Pedido não encontrado' });
  res.json(pedido);
});

// Atualizar status do pedido
app.put('/api/pedidos/:id/status', (req, res) => {
  const pedido = pedidos.find(p => p.id === parseInt(req.params.id));
  if (!pedido) return res.status(404).json({ error: 'Pedido não encontrado' });

  const { status, obs } = req.body;
  const validos = ['recebido', 'confirmado', 'em_preparo', 'no_forno', 'saiu_entrega', 'entregue', 'cancelado'];
  if (!validos.includes(status)) {
    return res.status(400).json({ error: `Status inválido. Válidos: ${validos.join(', ')}` });
  }

  pedido.status = status;
  pedido.historico.push({ status, data: new Date().toISOString(), obs: obs || '' });
  savePedidos();

  res.json(pedido);
});

// ============ API - TEMA/CONFIG ============
app.get('/api/config', (req, res) => {
  res.json({
    name: process.env.BUSINESS_NAME || 'Pizza Boa',
    deliveryFee: parseFloat(process.env.DELIVERY_FEE || '5.00'),
    deliveryTime: parseInt(process.env.DELIVERY_TIME_MIN || '45'),
    orderMinimum: parseFloat(process.env.ORDER_MINIMUM || '20.00'),
  });
});

// ============ WEBHOOK WHATSAPP ============

// Verificação (GET)
app.get('/webhook', (req, res) => {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === process.env.WEBHOOK_VERIFY_TOKEN) {
    console.log('[WEBHOOK] Verificado com sucesso!');
    return res.status(200).send(challenge);
  }
  res.sendStatus(403);
});

// Recebimento de mensagens (POST)
app.post('/webhook', async (req, res) => {
  const body = req.body;
  if (!body.object) return res.sendStatus(404);

  const entry = body.entry?.[0];
  const changes = entry?.changes?.[0];
  const value = changes?.value;

  if (value?.messages) {
    const message = value.messages[0];
    const from = message.from;

    let text = '';
    if (message.type === 'text') {
      text = message.text.body;
    } else if (message.type === 'interactive') {
      const i = message.interactive;
      if (i.type === 'button_reply') text = i.button_reply.title;
      else if (i.type === 'list_reply') text = i.list_reply.title;
    }

    console.log(`[WA] Mensagem de ${from}: "${text}"`);
    await handleBotMessage(from, text);
  }

  res.sendStatus(200);
});

// ============ BOT WHATSAPP ============

import axios from 'axios';

const PHONE_ID = process.env.WHATSAPP_PHONE_ID;
const TOKEN = process.env.WHATSAPP_TOKEN;
const API_URL = `https://graph.facebook.com/v21.0/${PHONE_ID}/messages`;
const BUSINESS_NAME = process.env.BUSINESS_NAME || 'Pizza Boa';

async function waSend(to, text) {
  try {
    await axios.post(API_URL, {
      messaging_product: 'whatsapp',
      recipient_type: 'individual',
      to, type: 'text',
      text: { preview_url: false, body: text }
    }, { headers: { 'Authorization': `Bearer ${TOKEN}`, 'Content-Type': 'application/json' } });
  } catch (err) {
    console.error('[WA] Erro:', err.response?.data || err.message);
  }
}

async function waSendButtons(to, text, buttons) {
  try {
    const waButtons = buttons.slice(0, 3).map((btn, i) => ({
      type: 'reply',
      reply: { id: btn.id || `btn_${i}`, title: btn.title.slice(0, 20) }
    }));
    await axios.post(API_URL, {
      messaging_product: 'whatsapp', recipient_type: 'individual', to,
      type: 'interactive',
      interactive: {
        type: 'button',
        body: { text: text.slice(0, 1024) },
        action: { buttons: waButtons }
      }
    }, { headers: { 'Authorization': `Bearer ${TOKEN}`, 'Content-Type': 'application/json' } });
  } catch (err) {
    console.error('[WA] Erro botões:', err.response?.data || err.message);
  }
}

async function handleBotMessage(from, text) {
  const sessao = sessions.get(from) || { estado: 'inicio', pedido: null };
  const t = text?.toLowerCase() || '';

  // Comando global
  if (t === 'menu') {
    sessao.estado = 'inicio';
    sessions.set(from, sessao);
  }

  switch (sessao.estado) {
    case 'inicio':
      sessions.set(from, { estado: 'menu', pedido: null });
      await waSend(from, `Olá! Bem-vindo(a) à ${BUSINESS_NAME}! 🍕\n\nSou o assistente virtual. O que deseja?`);
      await waSendButtons(from, 'Escolha uma opção:', [
        { id: 'ver_cardapio', title: 'Ver Cardápio' },
        { id: 'fazer_pedido', title: 'Fazer Pedido' },
        { id: 'rastrear', title: 'Rastrear Pedido' }
      ]);
      break;

    case 'menu':
      if (t.includes('cardapio') || t.includes('ver')) {
        let msg = '📋 *Nosso Cardápio*\n\n';
        for (const cat of cardapio.categorias) {
          msg += `${cat.icone} *${cat.nome}*\n`;
          for (const item of cat.itens) {
            const menor = item.tamanhos[0];
            msg += `  • ${item.nome} — a partir de R$ ${menor.preco.toFixed(2)}\n`;
          }
          msg += '\n';
        }
        msg += 'Para fazer um pedido, digite "pedido".';
        await waSend(from, msg);
      } else if (t.includes('pedido') || t.includes('fazer')) {
        sessions.set(from, { estado: 'pedido_categoria', pedido: { itens: [], total: 0 } });
        let cats = cardapio.categorias.map((c, i) => ({
          id: `cat_${c.id}`,
          title: `${c.icone} ${c.nome}`
        }));
        await waSendButtons(from, '🍕 Vamos montar seu pedido!\n\nSelecione uma categoria:', cats);
      } else if (t.includes('rastrear')) {
        await waSend(from, 'Digite o número do seu pedido (ex: #123):');
        sessions.set(from, { estado: 'rastrear', pedido: null });
      } else {
        await waSendButtons(from, 'Não entendi. Escolha uma opção:', [
          { id: 'ver_cardapio', title: 'Ver Cardápio' },
          { id: 'fazer_pedido', title: 'Fazer Pedido' },
          { id: 'rastrear', title: 'Rastrear Pedido' }
        ]);
      }
      break;

    case 'rastrear': {
      const num = parseInt(text.replace(/\D/g, ''));
      const pedido = pedidos.find(p => p.id === num);
      if (pedido) {
        const statusEmoji = {
          recebido: '📥', confirmado: '✅', em_preparo: '👨‍🍳',
          no_forno: '🔥', saiu_entrega: '🛵', entregue: '🎉', cancelado: '❌'
        };
        await waSend(from,
          `📦 *Pedido #${pedido.id}*\n\n` +
          `Status: ${statusEmoji[pedido.status] || '📋'} ${pedido.status}\n` +
          `Total: R$ ${pedido.totalFinal.toFixed(2)}\n` +
          `Endereço: ${pedido.endereco}\n\n` +
          pedido.itens.map(i => `• ${i.nome} (${i.tamanho}) — R$ ${i.preco.toFixed(2)}`).join('\n')
        );
      } else {
        await waSend(from, 'Pedido não encontrado. Verifique o número e tente novamente.');
      }
      sessions.set(from, { estado: 'menu', pedido: null });
      break;
    }

    default:
      sessions.set(from, { estado: 'inicio', pedido: null });
      await handleBotMessage(from, '');
  }
}

// Notifica novo pedido via WhatsApp
async function notifyWhatsApp(pedido) {
  // Aqui você pode notificar o dono da pizzaria
  console.log(`[PEDIDO #${pedido.id}] Novo pedido! Total: R$ ${pedido.totalFinal.toFixed(2)}`);
}

// ============ HEALTH CHECK ============
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ============ SERVIDOR ============
app.listen(PORT, () => {
  console.log('=================================');
  console.log(`  🍕 ${BUSINESS_NAME} - Servidor rodando`);
  console.log(`  📡 API:     http://localhost:${PORT}/api`);
  console.log(`  📋 Cardápio: http://localhost:${PORT}/api/cardapio`);
  console.log(`  📦 Pedidos:  http://localhost:${PORT}/api/pedidos`);
  console.log(`  ❤️  Health:  http://localhost:${PORT}/health`);
  console.log('=================================');
});
