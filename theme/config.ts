/**
 * 🎨 TEMA - Configuração customizável por pizzaria
 * 
 * Para criar um app para outra pizzaria, copie a pasta
 * theme/ e modifique APENAS este arquivo.
 */

export const theme = {
  // ============ IDENTIDADE ============
  business: {
    name: "Pizza Boa",
    slogan: "A melhor pizza da cidade!",
    logo: "/logo.png",           // Coloque a logo em public/
    favicon: "/favicon.ico",
  },

  // ============ CORES ============
  // Paleta roxa escura (padrão HeeD)
  colors: {
    primary: "#581c87",          // Roxo escuro
    primaryLight: "#7e22ce",     // Roxo médio
    primaryDark: "#3b0764",      // Roxo muito escuro
    accent: "#a855f7",           // Roxo claro
    background: "#0a0a0a",       // Fundo escuro
    surface: "#1a1a1a",          // Cards
    text: "#ffffff",             // Texto principal
    textSecondary: "#a1a1a1",    // Texto secundário
  },

  // ============ ENTREGA ============
  delivery: {
    fee: 5.00,                   // Taxa de entrega
    timeMinutes: 45,             // Tempo estimado
    minimumOrder: 20.00,         // Pedido mínimo
    freeDeliveryAbove: 50.00,    // Entrega grátis acima de
  },

  // ============ CONTATO ============
  contact: {
    phone: "+55 19 99999-9999",
    whatsapp: "5519999999999",
    address: "Rua Exemplo, 123 - Centro",
    city: "Sua Cidade - UF",
    instagram: "@pizzaboa",
  },

  // ============ HORÁRIOS ============
  hours: {
    Seg: { open: "18:00", close: "23:00" },
    Ter: { open: "18:00", close: "23:00" },
    Qua: { open: "18:00", close: "23:00" },
    Qui: { open: "18:00", close: "23:00" },
    Sex: { open: "18:00", close: "00:00" },
    Sáb: { open: "18:00", close: "00:00" },
    Dom: { open: "18:00", close: "23:00" },
  },

  // ============ PAGAMENTO ============
  payment: {
    pixKey: "sua-chave-pix-aqui",
    pixName: "Pizza Boa",
  },

  // ============ TEXTO DO BOT ============
  bot: {
    welcomeMessage: "Olá! Bem-vindo(a) à {name}! 🍕\n\nSou o assistente virtual. O que deseja?",
    menuTitle: "Escolha uma opção:",
    orderStarted: "Vamos montar seu pedido! 🍕\nNúmero do pedido: *#{id}*",
    orderConfirm: "Confirme seu pedido 👇",
    orderSent: "Pedido enviado com sucesso! ✅\n\nTempo estimado: {time} minutos.\nEntraremos em contato para confirmar.",
  },
};

export default theme;
