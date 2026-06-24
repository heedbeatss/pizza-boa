/**
 * 🍕 CONFIG - Variáveis customizáveis por pizzaria
 * 
 * Para criar um app para outra pizzaria, copie este arquivo
 * e modifique APENAS os valores abaixo.
 */

var APP_CONFIG = {
  // ============ IDENTIDADE ============
  nome: "Pizza Boa",
  slogan: "Delivery",
  
  // ============ API ============
  apiUrl: "https://script.google.com/macros/s/AKfycbxnxQ9Hj6hEbmveEPNySjkLYXRMwXIwdhV4TGeiLIJn6uf0evIUPne1X6XFJPimhi5qAQ/exec",
  
  // ============ CONTATO ============
  whatsapp: "19984356289",
  nomeAdmin: "Admin",
  senhaAdmin: "1234",
  
  // ============ CORES ============
  corPrimaria: "#581c87",
  corAccent: "#a855f7",
  corFundo: "#0a0a0a",
  corSurface: "#1a1a1a",
  corTexto: "#ffffff",
  
  // ============ ENTREGA ============
  pedidoMinimo: 30.00,
  
  // ============ TEXTOS NOTIFICAÇÃO ============
  msgs: {
    recebido: { title: "🍕 Pedido Recebido!", body: "Seu pedido foi recebido!" },
    confirmado: { title: "✅ Pedido Confirmado!", body: "Seu pedido foi confirmado!" },
    em_preparo: { title: "👨‍🍳 Em Preparo!", body: "Seu pedido está sendo preparado!" },
    no_forno: { title: "🔥 No Forno!", body: "Seu pedido foi para o forno!" },
    saiu_entrega: { title: "🛵 Saiu para Entrega!", body: "Seu pedido saiu para entrega!" },
    retirou: { title: "🏪 Retirado!", body: "Seu pedido foi retirado!" },
    entregue: { title: "🎉 Entregue!", body: "Seu pedido foi entregue!" },
    cancelado: { title: "❌ Cancelado!", body: "Seu pedido foi cancelado." }
  }
};
