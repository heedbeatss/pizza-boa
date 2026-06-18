# Script para reconstruir o app.html de forma limpa
import re

# Ler arquivo atual
with open('app.html', 'r') as f:
    content = f.read()

# Extrair HTML puro (antes do <script>)
html_end = content.find('<script>')
html_part = content[:html_end]

# Extrair CARDAPIO
match = re.search(r'var CARDAPIO = \{.*?\n\};', content, re.DOTALL)
cardapio = match.group() if match else ""

print(f"HTML: {len(html_part)} chars")
print(f"CARDAPIO: {len(cardapio)} chars")

# Criar JS limpo - usando template string com aspas duplas escapadas
js = r"""
<script>
""" + cardapio + """

var DIAS_FUNCIONAMENTO = [0, 2, 3, 4, 5, 6];
var HORA_INICIO = 18;
var HORA_FIM = 1;

function isPizzariaAberta() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) return false;
  if (hora >= 18) return true;
  if (hora < 1) return true;
  return false;
}

function getHorarioInfo() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  var nomes = ['Domingo','Segunda','Terca','Quarta','Quinta','Sexta','Sabado'];
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) return 'Hoje e ' + nomes[dia] + '. Fechados. Terca a Domingo, 18h-01h.';
  if (hora >= 1 && hora < 18) return 'Ainda nao abrimos. Hoje abrimos as 18h.';
  return 'Estamos abertos!';
}

var TAXA_FIXA_MOTOBOY = 3.0;
var TAXA_POR_KM = 1.0;
var TAXA_MAXIMA = 25.0;
var MIN_PEDIDO_GRATIS = 100;
var zonaAtual = null;
var cart = [];
var currentItem = null;
var selTamanho = null;
var selMetade = false;
var selSegundo = null;
var selBorda = 0;
var selQty = 1;
var ultimoPedidoId = null;
var contadorPedidos = parseInt(localStorage.getItem('contadorPedidos') || '0');

var ZONAS_ENTREGA = [
  { nome: "Jardim Elite", bairros: ["jardim elite","jd. elite","elite"], dist: 1, taxa: 4 },
  { nome: "Centro", bairros: ["centro","alto","nova piracicaba","vila cristina"], dist: 2, taxa: 5 },
  { nome: "Nova America", bairros: ["nova america","nova américa","america"], dist: 4, taxa: 7 },
  { nome: "Vila Reis", bairros: ["vila reis","reis"], dist: 3, taxa: 6 },
  { nome: "Sao Judas", bairros: ["sao judas","judas"], dist: 3.5, taxa: 6.5 },
  { nome: "Morumbi", bairros: ["morumbi"], dist: 4, taxa: 7 },
  { nome: "Pacaembu", bairros: ["pacaembu"], dist: 4.5, taxa: 7.5 },
  { nome: "Corrego", bairros: ["corrego","córrego"], dist: 3.5, taxa: 6.5 },
  { nome: "Santa Olimpia", bairros: ["santa olimpia","santa olímpia"], dist: 4, taxa: 7 },
  { nome: "Verde", bairros: ["verde","vila verde"], dist: 5, taxa: 8 },
  { nome: "Campestre", bairros: ["campestre","monsenhor martinho","martinho"], dist: 5, taxa: 8 },
  { nome: "Tupi", bairros: ["tupi","tupy","campestre"], dist: 6, taxa: 9 },
  { nome: "Aguas Claras", bairros: ["aguas claras","águas claras"], dist: 7, taxa: 10 },
  { nome: "Irmaos Camargo", bairros: ["irmaos camargo","irmãos camargo"], dist: 7.5, taxa: 10.5 },
  { nome: "Alfredo Guedes", bairros: ["alfredo guedes","jardim gloria","jd. gloria"], dist: 8, taxa: 11 },
  { nome: "Esplanada", bairros: ["esplanada","ceu azul","céu azul"], dist: 9, taxa: 12 },
  { nome: "Vila Monteiro", bairros: ["vila monteiro","monteiro","geraldao","geraldão"], dist: 8, taxa: 11 },
  { nome: "Potumirim", bairros: ["potumirim","santa teresa","sta. teresa"], dist: 10, taxa: 13 },
  { nome: "Anhumas", bairros: ["anhumas"], dist: 12, taxa: 15 }
];

function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }

function calcularEntrega() {
  var bairro = document.getElementById('bairro').value.trim();
  var rua = document.getElementById('rua').value.trim();
  if (!bairro || !rua) { document.getElementById('zonaBox').style.display = 'none'; zonaAtual = null; renderCheckoutSummary(); return; }
  var box = document.getElementById('zonaBox');
  var status = document.getElementById('cepStatus');
  box.style.display = 'block'; status.style.display = 'block';
  document.getElementById('zonaNome').textContent = 'Calculando...';
  document.getElementById('zonaValor').textContent = '';
  document.getElementById('zonaTempo').textContent = '';
  var bn = norm(bairro);
  var encontrada = null;
  for (var i = 0; i < ZONAS_ENTREGA.length; i++) {
    for (var j = 0; j < ZONAS_ENTREGA[i].bairros.length; j++) {
      if (bn.indexOf(ZONAS_ENTREGA[i].bairros[j]) >= 0 || ZONAS_ENTREGA[i].bairros[j].indexOf(bn) >= 0) { encontrada = ZONAS_ENTREGA[i]; break; }
    }
    if (encontrada) break;
  }
  if (!encontrada) encontrada = { nome: "Zona Piracicaba", dist: 8, taxa: 11 };
  var taxa = encontrada.taxa;
  var totalPed = 0; for (var i = 0; i < cart.length; i++) totalPed += cart[i].preco * cart[i].qty;
  if (totalPed >= MIN_PEDIDO_GRATIS) taxa = 0;
  var tMin = Math.round(encontrada.dist * 5 + 20);
  var tMax = Math.round(encontrada.dist * 7 + 30);
  box.className = 'zona-box zona-ok';
  document.getElementById('zonaNome').textContent = encontrada.nome + ' (~' + encontrada.dist + ' km)';
  document.getElementById('zonaValor').textContent = taxa === 0 ? 'GRATIS' : 'R$ ' + taxa.toFixed(2);
  document.getElementById('zonaValor').style.color = taxa === 0 ? '#4ade80' : '#a855f7';
  document.getElementById('zonaTempo').textContent = tMin + '-' + tMax + ' min';
  status.textContent = 'Entrega calculada!'; status.style.color = '#4ade80';
  zonaAtual = { valor: taxa, tempo: tMin + '-' + tMax + ' min', distKm: encontrada.dist, nome: encontrada.nome };
  renderCheckoutSummary();
}

function render() {
  var nav = document.getElementById('catNavMenu');
  var cardapio = document.getElementById('cardapio');
  var h = '', c = '';
  for (var i = 0; i < CARDAPIO.categorias.length; i++) {
    var cat = CARDAPIO.categorias[i];
    h += '<button class="cat-btn ' + (i === 0 ? 'active' : '') + '" data-cat="' + cat.id + '">' + cat.icone + ' ' + cat.nome + '</button>';
    var items = '';
    for (var j = 0; j < cat.itens.length; j++) {
      var it = cat.itens[j];
      items += '<div class="item-card" onclick="openItem(\\'' + cat.id + '\\', \\'' + it.id + '\\')"><h3>' + it.nome + '</h3><p>' + it.descricao + '</p><div class="price">R$ ' + it.tamanhos[0].preco.toFixed(2) + '</div></div>';
    }
    c += '<div class="section" id="cat-' + cat.id + '"><h2 class="section-title">' + cat.icone + ' ' + cat.nome + '</h2>' + items + '</div>';
  }
  nav.innerHTML = h;
  cardapio.innerHTML = c;
}

document.querySelector('.cat-nav').addEventListener('click', function(e) {
  var btn = e.target.closest('.cat-btn');
  if (!btn) return;
  this.querySelectorAll('.cat-btn').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  var target = document.getElementById('cat-' + btn.dataset.cat);
  if (target) window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 120, behavior: 'smooth' });
});

function openItem(catId, itemId) {
  var cat = null, item = null;
  for (var i = 0; i < CARDAPIO.categorias.length; i++) {
    if (CARDAPIO.categorias[i].id === catId) {
      cat = CARDAPIO.categorias[i];
      for (var j = 0; j < cat.itens.length; j++) { if (cat.itens[j].id === itemId) { item = cat.itens[j]; break; } }
      break;
    }
  }
  if (!item) return;
  currentItem = item; selTamanho = item.tamanhos[0]; selMetade = false; selSegundo = null; selBorda = 0; selQty = 1;
  var isPizza = catId.indexOf('pizza') >= 0;
  var h = '';
  h += '<div class="modal-header"><div><h2>' + item.nome + '</h2><p>' + item.descricao + '</p></div>';
  h += '<button class="modal-close" onclick="closeModal(\\'itemModal\\')">✕</button></div>';
  h += '<label class="label">Tamanho</label><div class="size-grid">';
  for (var i = 0; i < item.tamanhos.length; i++) {
    var t = item.tamanhos[i];
    h += '<button class="size-btn ' + (i === 0 ? 'active' : '') + '" onclick="selectTamanho(' + i + ')"><div>' + t.nome + '</div>' + (t.fatias ? '<div class="slices">' + t.fatias + ' fatias</div>' : '') + '<span class="price">R$ ' + t.preco.toFixed(2) + '</span></button>';
  }
  h += '</div>';
  if (isPizza) {
    h += '<label class="label">Como deseja?</label><div class="toggle-row">';
    h += '<button class="toggle-btn active" id="btnInteira" onclick="setMetade(false)">Inteira<div style="font-size:11px;opacity:0.7">R$ ' + selTamanho.preco.toFixed(2) + '</div></button>';
    h += '<button class="toggle-btn" id="btnMetade" onclick="setMetade(true)">Metade/Metade<div style="font-size:11px;opacity:0.7">2 sabores</div></button>';
    h += '</div><div id="metadeSection"></div>';
  }
  if (isPizza) {
    h += '<label class="label">Borda Recheada</label><div class="toggle-row">';
    h += '<button class="toggle-btn active" id="btnBordaNao" onclick="setBorda(0)">Sem borda</button>';
    h += '<button class="toggle-btn" id="btnBordaSim" onclick="setBorda(1)">Catupiry <span style="font-size:11px;opacity:0.7">+ R$ 8,00</span></button>';
    h += '</div>';
  }
  h += '<label class="label">Quantidade</label><div class="qty-row"><button class="qty-btn minus" onclick="changeQty(-1)">−</button><span class="qty-val" id="qtyVal">' + selQty + '</span><button class="qty-btn plus" onclick="changeQty(1)">+</button></div>';
  h += '<button class="add-btn" id="addBtn" onclick="addToCart()">Adicionar — R$ ' + calcPrice().toFixed(2) + '</button>';
  document.getElementById('modalContent').innerHTML = h;
  document.getElementById('itemModal').style.display = 'flex';
}

function selectTamanho(idx) { selTamanho = currentItem.tamanhos[idx]; document.querySelectorAll('.size-btn').forEach(function(b) { b.classList.remove('active'); }); event.target.closest('.size-btn').classList.add('active'); var btn = document.getElementById('btnInteira'); if (btn) btn.innerHTML = 'Inteira<div style="font-size:11px;opacity:0.7">R$ ' + selTamanho.preco.toFixed(2) + '</div>'; updateAddBtn(); }
function setBorda(val) { selBorda = val; document.getElementById('btnBordaNao').classList.toggle('active', val === 0); document.getElementById('btnBordaSim').classList.toggle('active', val === 1); updateAddBtn(); }
function setMetade(val) { selMetade = val; selSegundo = null; document.getElementById('btnInteira').classList.toggle('active', !val); document.getElementById('btnMetade').classList.toggle('active', val); var sec = document.getElementById('metadeSection'); if (val) { var h = '<div class="metade-info"><div class="metade-row"><span>1a metade: <strong>' + currentItem.nome + '</strong></span><span style="color:#a855f7">R$ ' + selTamanho.preco.toFixed(2) + '</span></div><div style="font-size:12px;color:#a1a1a1">Escolha a 2a metade:</div><div style="font-size:11px;color:#f59e0b;margin-top:4px">O preco final sera da metade mais cara</div></div>'; for (var c = 0; c < CARDAPIO.categorias.length; c++) { var cat = CARDAPIO.categorias[c]; if (cat.id.indexOf('pizza') < 0) continue; var itens = cat.itens.filter(function(i) { return i.id !== currentItem.id; }); if (itens.length === 0) continue; var icone = cat.id.indexOf('doce') >= 0 ? '🍫' : (cat.id.indexOf('especial') >= 0 ? '⭐' : '🍕'); h += '<div class="cat-label">' + icone + ' ' + cat.nome + '</div><div class="sabor-grid">'; for (var i = 0; i < itens.length; i++) { var s = itens[i]; var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0]; var pm = Math.max(selTamanho.preco, sp.preco); h += '<button class="sabor-btn" data-id="' + s.id + '" onclick="selectSegundo(\\'' + s.id + '\\')">' + s.nome + ' <span>R$ ' + pm.toFixed(2) + '</span></button>'; } h += '</div>'; } sec.innerHTML = h; } else { sec.innerHTML = ''; } updateAddBtn(); }
function selectSegundo(id) { selSegundo = id; document.querySelectorAll('.sabor-btn').forEach(function(b) { b.classList.remove('active'); }); event.target.closest('.sabor-btn').classList.add('active'); updateAddBtn(); }
function changeQty(d) { selQty = Math.max(1, selQty + d); document.getElementById('qtyVal').textContent = selQty; updateAddBtn(); }

function calcPrice() {
  var preco = selTamanho.preco;
  if (selMetade && selSegundo) { var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; }); var s = todos.find(function(i) { return i.id === selSegundo; }); if (s) { var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0]; preco = Math.max(preco, sp.preco); } }
  if (selBorda) preco += 8;
  return preco * selQty;
}

function updateAddBtn() { var btn = document.getElementById('addBtn'); if (btn) { btn.textContent = 'Adicionar — R$ ' + calcPrice().toFixed(2); btn.disabled = selMetade && !selSegundo; } }

function addToCart() {
  var nome = currentItem.nome;
  if (selMetade && selSegundo) { var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; }); var s = todos.find(function(i) { return i.id === selSegundo; }); if (s) nome = '1/2 ' + currentItem.nome + ' / 1/2 ' + s.nome; }
  if (selBorda) nome += ' (borda catupiry)';
  cart.push({ nome: nome, tamanho: selTamanho.nome, preco: calcPrice() / selQty, qty: selQty });
  closeModal('itemModal'); updateCartButton();
}

function closeModal(id) { document.getElementById(id).style.display = 'none'; }

function updateHorarioHeader() {
  var aberta = isPizzariaAberta();
  var badge = document.getElementById('openBadge');
  var aviso = document.getElementById('horarioAviso');
  if (badge) { badge.textContent = aberta ? 'Aberto' : 'Fechado'; badge.style.color = aberta ? '#4ade80' : '#f87171'; badge.style.background = aberta ? 'rgba(74,222,128,.15)' : 'rgba(248,113,113,.15)'; }
  if (aviso) { aviso.style.display = aberta ? 'none' : 'block'; if (!aberta) aviso.textContent = getHorarioInfo(); }
}

function updateCartButton() { var btn = document.getElementById('cartBtn'); if (!btn) return; var count = 0, total = 0; for (var i = 0; i < cart.length; i++) { count += cart[i].qty; total += cart[i].preco * cart[i].qty; } if (count > 0) { btn.style.display = 'block'; document.getElementById('cartCount').textContent = count + ' item' + (count > 1 ? 's' : ''); document.getElementById('cartTotal').textContent = 'R$ ' + total.toFixed(2); } else { btn.style.display = 'none'; } }

function toggleCart() { if (!isPizzariaAberta()) { alert('Estamos fechados!\\n\\nHorario: Terca a Domingo, 18h-01h.'); return; } var modal = document.getElementById('cartModal'); modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex'; if (modal.style.display === 'flex') renderCart(); }

function renderCart() {
  var h = ''; var total = 0;
  for (var i = 0; i < cart.length; i++) { var it = cart[i]; h += '<div class="cart-item"><div class="cart-item-info"><div class="name">' + it.qty + 'x ' + it.nome + ' (' + it.tamanho + ')</div><div class="price">R$ ' + (it.preco * it.qty).toFixed(2) + '</div></div><button onclick="removeCartItem(' + i + ')" style="background:none;border:none;color:#f87171;font-size:18px;cursor:pointer">✕</button></div>'; total += it.preco * it.qty;
  }
  h += '<div class="cart-summary"><div class="cart-summary-row"><span class="lbl">Subtotal</span><span>R$ ' + total.toFixed(2) + '</span></div><div class="cart-summary-row"><span class="lbl">Entrega</span><span>Calculada no checkout</span></div><div class="cart-summary-total"><span>Total</span><span class="val">R$ ' + total.toFixed(2) + '</span></div><button class="add-btn" onclick="goCheckout()">Finalizar Pedido</button></div>';
  document.getElementById('cartContent').innerHTML = h;
}

function removeCartItem(idx) { cart.splice(idx, 1); updateCartButton(); renderCart(); }

function goCheckout() {
  document.getElementById('cartModal').style.display = 'none';
  document.getElementById('cartBtn').style.display = 'none';
  document.getElementById('checkoutPage').style.display = 'block';
  document.getElementById('cardapio').style.display = 'none';
  document.getElementById('catNavMenu').style.display = 'none';
  document.getElementById('checkoutForm').style.display = 'block';
  document.getElementById('checkoutSuccess').style.display = 'none';
  document.getElementById('cep').value = '';
  document.getElementById('rua').value = '';
  document.getElementById('bairro').value = '';
  document.getElementById('cidade').value = '';
  document.getElementById('numero').value = '';
  document.getElementById('nome').value = '';
  document.getElementById('telefone').value = '';
  document.getElementById('troco').value = '';
  document.getElementById('obs').value = '';
  document.getElementById('cepStatus').style.display = 'none';
  document.getElementById('zonaBox').style.display = 'none';
  zonaAtual = null;
  renderCheckoutSummary();
  window.scrollTo(0, 0);
}

function renderCheckoutSummary() {
  var total = 0; for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
  var h = '<div class="cart-summary">';
  for (var i = 0; i < cart.length; i++) { var it = cart[i]; h += '<div class="cart-summary-row"><span class="lbl">' + it.qty + 'x ' + it.nome + ' (' + it.tamanho + ')</span><span>R$ ' + (it.preco * it.qty).toFixed(2) + '</span></div>'; }
  h += '<div class="cart-summary-row"><span class="lbl">Subtotal</span><span>R$ ' + total.toFixed(2) + '</span></div>';
  var entrega = zonaAtual ? zonaAtual.valor : 0;
  if (zonaAtual) { h += '<div class="cart-summary-row"><span class="lbl">Entrega (' + zonaAtual.nome + ')</span><span style="color:' + (zonaAtual.valor === 0 ? '#4ade80' : '#a855f7') + '">' + (zonaAtual.valor === 0 ? 'GRATIS' : 'R$ ' + zonaAtual.valor.toFixed(2)) + '</span></div>'; }
  if (total > 0 && total < MIN_PEDIDO_GRATIS && zonaAtual && zonaAtual.valor > 0) { h += '<div style="margin-top:8px;padding:8px;background:rgba(74,222,128,.1);border-radius:8px;font-size:12px;color:#4ade80;text-align:center">Falta R$ ' + (MIN_PEDIDO_GRATIS - total).toFixed(2) + ' para entrega GRATIS!</div>'; }
  h += '<div class="cart-summary-total"><span>Total</span><span class="val">R$ ' + (total + entrega).toFixed(2) + '</span></div></div>';
  document.getElementById('checkoutSummary').innerHTML = h;
}

function buscarCEP() {
  var cep = document.getElementById('cep').value.replace(/\D/g, '');
  if (cep.length !== 8) return;
  var status = document.getElementById('cepStatus'); status.style.display = 'block'; status.textContent = 'Buscando...'; status.style.color = '#a1a1a1';
  var xhr = new XMLHttpRequest(); xhr.open('GET', 'https://viacep.com.br/ws/' + cep + '/json/', true);
  xhr.onreadystatechange = function() { if (xhr.readyState === 4 && xhr.status === 200) { try { var data = JSON.parse(xhr.responseText); if (data.erro) { status.textContent = 'CEP nao encontrado'; status.style.color = '#f87171'; return; } document.getElementById('rua').value = data.logradouro || ''; document.getElementById('bairro').value = data.bairro || ''; document.getElementById('cidade').value = (data.localidade || '') + (data.uf ? ' - ' + data.uf : ''); status.textContent = data.logradouro + ', ' + data.bairro; status.style.color = '#4ade80'; document.getElementById('cep').value = cep.substring(0,5) + '-' + cep.substring(5); calcularEntrega(); document.getElementById('numero').focus(); } catch(e) { status.textContent = 'Erro'; status.style.color = '#f87171'; } } };
  xhr.send();
}

function selectPay(btn) { document.querySelectorAll('.pay-btn').forEach(function(b) { b.classList.remove('active'); }); btn.classList.add('active'); document.getElementById('trocoSection').style.display = btn.dataset.pay === 'dinheiro' ? 'block' : 'none'; document.getElementById('pixSection').style.display = btn.dataset.pay === 'pix' ? 'block' : 'none'; }
function copyPixKey() { var key = document.getElementById('pixKey').textContent; if (navigator.clipboard) { navigator.clipboard.writeText(key).then(function() { showCopyMsg(); }).catch(function() { fallbackCopy(key); }); } else { fallbackCopy(key); } }
function fallbackCopy(text) { var ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); showCopyMsg(); } catch(e) { alert('Copie: ' + text); } document.body.removeChild(ta); }
function showCopyMsg() { var msg = document.getElementById('copyMsg'); msg.style.display = 'block'; setTimeout(function() { msg.style.display = 'none'; }, 2000); }

var STATUS_PEDIDO = {
  recebido: { nome: 'Recebido', class: 'recebido', icon: '📥' },
  confirmado: { nome: 'Confirmado', class: 'confirmado', icon: '✅' },
  em_preparo: { nome: 'Em Preparo', class: 'em_preparo', icon: '👨‍🍳' },
  no_forno: { nome: 'No Forno', class: 'no_forno', icon: '🔥' },
  saiu_entrega: { nome: 'Saiu p/ Entrega', class: 'saiu_entrega', icon: '🛵' },
  entregue: { nome: 'Entregue', class: 'entregue', icon: '🎉' },
  cancelado: { nome: 'Cancelado', class: 'cancelado', icon: '❌' }
};

function submitOrder() {
  var nome = document.getElementById('nome').value.trim();
  var telefone = document.getElementById('telefone').value.trim();
  var rua = document.getElementById('rua').value.trim();
  var numero = document.getElementById('numero').value.trim();
  var bairro = document.getElementById('bairro').value.trim();
  var cidade = document.getElementById('cidade').value.trim();
  var cep = document.getElementById('cep').value.trim();
  var complemento = document.getElementById('complemento').value.trim();
  var referencia = document.getElementById('referencia').value.trim();
  var obs = document.getElementById('obs').value.trim();
  var pay = document.querySelector('.pay-btn.active') ? document.querySelector('.pay-btn.active').dataset.pay : 'dinheiro';
  var troco = document.getElementById('troco').value.trim();
  if (!nome) { showError('Informe seu nome.'); return; }
  if (!telefone) { showError('Informe seu telefone.'); return; }
  if (!rua || !numero || !bairro) { showError('Preencha o endereco completo.'); return; }
  if (!zonaAtual) { showError('Nao foi possivel calcular a entrega.'); return; }
  contadorPedidos++; localStorage.setItem('contadorPedidos', contadorPedidos);
  var pedidoId = '#' + String(contadorPedidos).padStart(4, '0');
  var total = 0; for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
  var entrega = zonaAtual.valor; var totalFinal = total + entrega;
  var pedido = { id: pedidoId, nome: nome, telefone: telefone, endereco: { cep: cep, rua: rua, numero: numero, bairro: bairro, cidade: cidade, complemento: complemento, referencia: referencia }, itens: cart.slice(), pagamento: pay, troco: troco, total: total, entrega: entrega, totalFinal: totalFinal, obs: obs, status: 'recebido', data: new Date().toISOString() };
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]'); pedidos.push(pedido); localStorage.setItem('pizzaPedidos', JSON.stringify(pedidos)); localStorage.setItem('ultimoTelefone', telefone); ultimoPedidoId = pedidoId;
  var msg = '🍕 *NOVO PEDIDO* - ' + pedidoId + '%0A%0A👤 *Cliente:* ' + nome + '%0A📱 *Telefone:* ' + telefone + '%0A%0A📦 *Itens:*%0A';
  for (var i = 0; i < cart.length; i++) { var it = cart[i]; msg += '• ' + it.qty + 'x ' + it.nome + ' (' + it.tamanho + ') - R$ ' + (it.preco * it.qty).toFixed(2) + '%0A'; }
  msg += '%0A💰 *Subtotal:* R$ ' + total.toFixed(2) + '%0A🛵 *Entrega:* ' + (entrega === 0 ? 'GRATIS' : 'R$ ' + entrega.toFixed(2)) + '%0A';
  if (pay === 'dinheiro' && troco) msg += '💵 *Troco para:* R$ ' + troco + '%0A';
  msg += '💵 *TOTAL:* R$ ' + totalFinal.toFixed(2) + '%0A%0A';
  var pagNome = { dinheiro: 'Dinheiro', pix: 'PIX', 'cartao-credito': 'Cartao Credito', 'cartao-debito': 'Cartao Debito' };
  msg += '💳 *Pagamento:* ' + (pagNome[pay] || pay) + '%0A%0A📍 *Endereco:*%0A' + rua + ', ' + numero;
  if (complemento) msg += ' ' + complemento;
  msg += ' - ' + bairro + ', ' + cidade + '%0A';
  if (referencia) msg += 'Ref: ' + referencia + '%0A';
  if (obs) msg += '%0A📝 ' + obs + '%0A';
  cart = []; updateCartButton();
  document.getElementById('checkoutForm').style.display = 'none';
  document.getElementById('checkoutSuccess').style.display = 'block';
  document.getElementById('pedidoNum').textContent = pedidoId;
  document.getElementById('waLink').href = 'https://wa.me/551984356289?text=' + encodeURIComponent(msg);
}

function showError(msg) { var el = document.getElementById('checkoutError'); el.textContent = msg; el.style.display = 'block'; }

function carregarPedidos() {
  var telefone = ''; var elTel = document.getElementById('telefonePedidos'); if (elTel) telefone = elTel.value.trim(); if (!telefone) telefone = localStorage.getItem('ultimoTelefone') || ''; if (!telefone) { var el = document.getElementById('meusPedidos'); if (el) el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Digite seu telefone acima</div>'; return; }
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]'); var meus = pedidos.filter(function(p) { return p.telefone === telefone; }); var el = document.getElementById('meusPedidos'); if (!el) return; if (meus.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido encontrado</div>'; return; }
  var h = ''; for (var i = meus.length - 1; i >= 0; i--) { var p = meus[i]; var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido; h += '<div class="pedido-card ' + st.class + '" style="margin-bottom:12px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><strong style="font-size:16px">' + p.id + '</strong><span class="status-badge ' + st.class + '">' + st.icon + ' ' + st.nome + '</span></div><div style="font-size:12px;color:#a1a1a1;margin-bottom:8px">' + new Date(p.data).toLocaleString('pt-BR') + '</div><div style="font-size:13px;margin-bottom:4px">'; for (var j = 0; j < p.itens.length; j++) { h += '• ' + p.itens[j].qty + 'x ' + p.itens[j].nome + ' (' + p.itens[j].tamanho + ')<br>'; } h += '</div><div style="display:flex;justify-content:space-between;border-top:1px solid rgba(88,28,135,.2);padding-top:8px"><span style="color:#a1a1a1;font-size:12px">Entrega: ' + (p.entrega === 0 ? 'GRATIS' : 'R$ ' + p.entrega.toFixed(2)) + '</span><strong style="color:#a855f7">R$ ' + p.totalFinal.toFixed(2) + '</strong></div></div>'; }
  el.innerHTML = h;
}

function showAdminLogin() { var senha = prompt('Senha admin:'); if (senha === '1234') { document.getElementById('adminPage').style.display = 'block'; document.getElementById('cardapio').style.display = 'none'; document.getElementById('catNavMenu').style.display = 'none'; document.getElementById('checkoutPage').style.display = 'none'; carregarAdminPedidos(); } }

function carregarAdminPedidos() {
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]'); var el = document.getElementById('adminPedidosList'); if (!el) return; if (pedidos.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido recebido</div>'; return; }
  var h = ''; for (var i = pedidos.length - 1; i >= 0; i--) { var p = pedidos[i]; var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido; h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\\'' + p.id + '\\')"><div style="display:flex;justify-content:space-between"><strong>' + p.id + '</strong><span class="status-badge ' + st.class + '">' + st.icon + ' ' + st.nome + '</span></div><div style="font-size:12px;color:#a1a1a1">' + p.nome + ' - ' + p.telefone + '</div><div style="font-size:12px;color:#a1a1a1">' + p.endereco.rua + ', ' + p.endereco.numero + ' - ' + p.endereco.bairro + '</div><div style="font-size:13px;margin-top:4px;color:#a855f7">R$ ' + p.totalFinal.toFixed(2) + '</div></div>'; }
  el.innerHTML = h;
}

function verPedidoAdmin(id) {
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]'); var p = pedidos.find(function(x) { return x.id === id; }); if (!p) return;
  var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido;
  var h = '<h3 style="margin-bottom:16px">' + p.id + ' - ' + st.icon + ' ' + st.nome + '</h3>';
  h += '<div style="background:#0a0a0a;border-radius:12px;padding:16px;margin-bottom:16px"><h4 style="color:#a855f7;margin-bottom:8px">👤 Cliente</h4><p><strong>Nome:</strong> ' + p.nome + '</p><p><strong>Telefone:</strong> ' + p.telefone + '</p></div>';
  h += '<div style="background:#0a0a0a;border-radius:12px;padding:16px;margin-bottom:16px"><h4 style="color:#a855f7;margin-bottom:8px">📍 Endereço</h4><p>' + p.endereco.rua + ', ' + p.endereco.numero + '</p>'; if (p.endereco.complemento) h += '<p>Complemento: ' + p.endereco.complemento + '</p>'; h += '<p>' + p.endereco.bairro + ', ' + p.endereco.cidade + '</p>'; if (p.endereco.referencia) h += '<p>Ref: ' + p.endereco.referencia + '</p></div>';
  h += '<div style="background:#0a0a0a;border-radius:12px;padding:16px;margin-bottom:16px"><h4 style="color:#a855f7;margin-bottom:8px">📦 Itens</h4>'; for (var i = 0; i < p.itens.length; i++) { var it = p.itens[i]; h += '<p>' + it.qty + 'x ' + it.nome + ' (' + it.tamanho + ') - R$ ' + (it.preco * it.qty).toFixed(2) + '</p>'; } h += '</div>';
  h += '<div style="background:#0a0a0a;border-radius:12px;padding:16px;margin-bottom:16px"><h4 style="color:#a855f7;margin-bottom:8px">💰 Pagamento</h4>'; var pagNome = { dinheiro: 'Dinheiro', pix: 'PIX', 'cartao-credito': 'Cartao Credito', 'cartao-debito': 'Cartao Debito' }; h += '<p><strong>Forma:</strong> ' + (pagNome[p.pagamento] || p.pagamento) + '</p>'; if (p.troco) h += '<p><strong>Troco para:</strong> R$ ' + p.troco + '</p>'; h += '<p><strong>Subtotal:</strong> R$ ' + p.total.toFixed(2) + '</p><p><strong>Entrega:</strong> ' + (p.entrega === 0 ? 'GRATIS' : 'R$ ' + p.entrega.toFixed(2)) + '</p><p style="font-size:18px;color:#a855f7"><strong>TOTAL: R$ ' + p.totalFinal.toFixed(2) + '</strong></p></div>';
  if (p.obs) { h += '<div style="background:#0a0a0a;border-radius:12px;padding:16px;margin-bottom:16px"><h4 style="color:#a855f7;margin-bottom:8px">📝 Observação</h4><p>' + p.obs + '</p></div>'; }
  h += '<h4 style="color:#a855f7;margin-bottom:12px">🔄 Alterar Status</h4><div style="display:flex;flex-wrap:wrap;gap:8px">';
  var statuses = ['recebido','confirmado','em_preparo','no_forno','saiu_entrega','entregue','cancelado'];
  for (var s = 0; s < statuses.length; s++) { var ss = STATUS_PEDIDO[statuses[s]]; var bg = p.status === statuses[s] ? '#581c87' : '#1a1a1a'; var color = p.status === statuses[s] ? '#fff' : '#a1a1a1'; h += '<button onclick="alterarStatus(\\'' + id + '\\', \\'' + statuses[s] + '\\')" style="padding:8px 16px;border-radius:8px;border:none;cursor:pointer;font-size:13px;background:' + bg + ';color:' + color + '">' + ss.icon + ' ' + ss.nome + '</button>'; }
  h += '</div>';
  document.getElementById('adminPedidoDetalhe').innerHTML = h;
}

function alterarStatus(id, status) { var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]'); var p = pedidos.find(function(x) { return x.id === id; }); if (p) { p.status = status; localStorage.setItem('pizzaPedidos', JSON.stringify(pedidos)); carregarAdminPedidos(); verPedidoAdmin(id); } }

function filterAdmin(filter, btn) { document.querySelectorAll('.admin-filter').forEach(function(b) { b.style.background = '#1a1a1a'; b.style.color = '#a1a1a1'; }); btn.style.background = '#581c87'; btn.style.color = '#fff'; var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]'); var filtrados = filter === 'todos' ? pedidos : pedidos.filter(function(p) { return p.status === filter; }); var el = document.getElementById('adminPedidosList'); if (filtrados.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido</div>'; return; } var h = ''; for (var i = filtrados.length - 1; i >= 0; i--) { var p = filtrados[i]; var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido; h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\\'' + p.id + '\\')"><div style="display:flex;justify-content:space-between"><strong>' + p.id + '</strong><span class="status-badge ' + st.class + '">' + st.icon + ' ' + st.nome + '</span></div><div style="font-size:12px;color:#a1a1a1">' + p.nome + ' - ' + p.telefone + '</div><div style="font-size:13px;margin-top:4px;color:#a855f7">R$ ' + p.totalFinal.toFixed(2) + '</div></div>'; } el.innerHTML = h; }

function showHome() { document.getElementById('checkoutPage').style.display = 'none'; document.getElementById('adminPage').style.display = 'none'; document.getElementById('checkoutSuccess').style.display = 'none'; document.getElementById('checkoutForm').style.display = 'block'; document.getElementById('cardapio').style.display = 'block'; document.getElementById('catNavMenu').style.display = 'flex'; document.getElementById('cartBtn').style.display = 'none'; zonaAtual = null; window.scrollTo({ top: 0, behavior: 'smooth' }); setTimeout(function() { carregarPedidos(); }, 500); }
function goBack() { showHome(); }

document.addEventListener('DOMContentLoaded', function() { updateHorarioHeader(); render(); });
setInterval(updateHorarioHeader, 60000);
document.getElementById('itemModal').addEventListener('click', function(e) { if (e.target === this) this.style.display = 'none'; });
document.getElementById('cartModal').addEventListener('click', function(e) { if (e.target === this) this.style.display = 'none'; });
document.addEventListener('visibilitychange', function() { if (document.visibilityState === 'visible') carregarPedidos(); });
setInterval(carregarPedidos, 10000);
</script>
</body>
</html>"""

final = html_part + js

with open('app.html', 'w') as f:
    f.write(final)

# Validar
import subprocess
with open('/tmp/test.js', 'w') as f:
    f.write(js)
result = subprocess.run(['node', '-c', '/tmp/test.js'], capture_output=True, text=True)
if result.returncode == 0:
    print("JS VALIDO! Arquivo reconstruido com sucesso.")
else:
    print("ERRO no JS:")
    print(result.stderr[:300])
