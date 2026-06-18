with open('app.html', 'r') as f:
    content = f.read()

# Extrair HTML (antes do <script>)
html_end = content.find('<script>')
html_part = content[:html_end]

# Extrair o CARDAPIO do JS atual (que esta correto)
import re
cardapio_match = re.search(r'(var CARDAPIO = \{.*?\});', content, re.DOTALL)
cardapio_js = cardapio_match.group(1) if cardapio_match else ""

print(f"HTML: {len(html_part)} chars")
print(f"CARDAPIO: {len(cardapio_js)} chars")

# Criar JavaScript completo e limpo
new_js = """
<script>
// ============ DATA ============
""" + cardapio_js + """

// ============ HORARIO DE FUNCIONAMENTO ============
var DIAS_FUNCIONAMENTO = [0, 2, 3, 4, 5, 6];
var HORA_INICIO = 18;
var HORA_FIM = 24;

function isPizzariaAberta() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) return false;
  return hora >= HORA_INICIO && hora < HORA_FIM;
}

function getHorarioInfo() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  var nomes = ['Domingo','Segunda','Terca','Quarta','Quinta','Sexta','Sabado'];
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) return 'Hoje e ' + nomes[dia] + '. Fechados. Terca a Domingo, 18h-00h.';
  if (hora < HORA_INICIO) return 'Ainda nao abrimos. Hoje abrimos as ' + HORA_INICIO + 'h.';
  if (hora >= HORA_FIM) return 'Ja fechamos. Abrimos amanha as ' + HORA_INICIO + 'h.';
  return 'Estamos abertos!';
}

// ============ CONFIGURACAO DE ENTREGA ============
var PIZZARIA_ENDERECO = "Rua Luiz Razera, 300 - Jd. Elite, Piracicaba - SP";
var PIZZARIA_COORDS = null;
var TAXA_FIXA_MOTOBOY = 3.0;
var TAXA_POR_KM = 1.0;
var TAXA_MAXIMA = 30.0;
var RAIO_MAXIMO_KM = 15;
var MIN_PEDIDO_GRATIS = 100;
var BAIRROS_GRATIS = [];
var MIN_GRATIS = 50;
var coordsCache = {};
var zonaAtual = null;

function geocodeAddress(address, callback) {
  var key = address.toLowerCase().trim();
  if (coordsCache[key]) { callback(null, coordsCache[key]); return; }
  var url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(address) + '&countrycodes=br&limit=1';
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.setRequestHeader('User-Agent', 'PizzaBoa-Delivery/1.0');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          if (data.length > 0) {
            var c = { lat: parseFloat(data[0].lat), lon: parseFloat(data[0].lon) };
            coordsCache[key] = c;
            callback(null, c);
          } else { callback('Nao encontrado', null); }
        } catch(e) { callback('Erro', null); }
      } else { callback('Erro rede', null); }
    }
  };
  xhr.send();
}

function calcDistance(lat1, lon1, lat2, lon2) {
  var R = 6371;
  var dLat = (lat2 - lat1) * Math.PI / 180;
  var dLon = (lon2 - lon1) * Math.PI / 180;
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon/2) * Math.sin(dLon/2);
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

function calcTaxaEntrega(distKm, totalPedido) {
  if (totalPedido >= MIN_PEDIDO_GRATIS) return 0;
  if (distKm <= 0) return TAXA_FIXA_MOTOBOY;
  return Math.min(TAXA_FIXA_MOTOBOY + Math.ceil(distKm) * TAXA_POR_KM, TAXA_MAXIMA);
}

function initPizzariaCoords() {
  geocodeAddress(PIZZARIA_ENDERECO, function(err, coords) {
    if (!err && coords) { PIZZARIA_COORDS = coords; console.log('[Pizzaria] OK'); }
  });
}

function calcularEntrega() {
  var bairro = document.getElementById('bairro').value.trim();
  var rua = document.getElementById('rua').value.trim();
  var numero = document.getElementById('numero').value.trim();
  var cidade = document.getElementById('cidade').value.trim();
  if (!bairro || !rua) { document.getElementById('zonaBox').style.display = 'none'; zonaAtual = null; renderCheckoutSummary(); return; }
  var box = document.getElementById('zonaBox');
  var status = document.getElementById('cepStatus');
  box.style.display = 'block';
  document.getElementById('zonaNome').textContent = 'Calculando...';
  document.getElementById('zonaValor').textContent = '';
  document.getElementById('zonaTempo').textContent = '';
  var endCliente = rua + (numero ? ', ' + numero : '') + ', ' + bairro + ', ' + cidade;
  if (!PIZZARIA_COORDS) { status.textContent = 'Preparando...'; status.style.color = '#f59e0b'; initPizzariaCoords(); setTimeout(calcularEntrega, 2000); return; }
  geocodeAddress(endCliente, function(err, coords) {
    if (err || !coords) { box.style.display = 'none'; status.textContent = 'Nao foi possivel calcular.'; status.style.color = '#f59e0b'; return; }
    var dist = calcDistance(PIZZARIA_COORDS.lat, PIZZARIA_COORDS.lon, coords.lat, coords.lon);
    var totalPed = 0; for (var i = 0; i < cart.length; i++) totalPed += cart[i].preco * cart[i].qty;
    var taxa = calcTaxaEntrega(dist, totalPed);
    var tMin = Math.round(dist * 5 + 20);
    var tMax = Math.round(dist * 7 + 30);
    if (dist > RAIO_MAXIMO_KM) {
      box.className = 'zona-box zona-erro';
      document.getElementById('zonaNome').textContent = 'Fora da area';
      document.getElementById('zonaValor').textContent = dist.toFixed(1) + ' km';
      document.getElementById('zonaValor').style.color = '#f87171';
      document.getElementById('zonaTempo').textContent = 'Nao entregamos';
      zonaAtual = null; renderCheckoutSummary(); return;
    }
    box.className = 'zona-box zona-ok';
    document.getElementById('zonaNome').textContent = dist.toFixed(1) + ' km';
    document.getElementById('zonaValor').textContent = taxa === 0 ? 'GRATIS' : 'R$ ' + taxa.toFixed(2);
    document.getElementById('zonaValor').style.color = taxa === 0 ? '#4ade80' : '#a855f7';
    document.getElementById('zonaTempo').textContent = tMin + '-' + tMax + ' min';
    zonaAtual = { valor: taxa, tempo: tMin + '-' + tMax + ' min', distKm: dist, nome: dist.toFixed(1) + ' km' };
    renderCheckoutSummary();
  });
}

// ============ ESTADO ============
var cart = [];
var currentItem = null;
var currentCat = null;
var selTamanho = null;
var selMetade = false;
var selSegundo = null;
var selBorda = 0;
var selQty = 1;

// ============ RENDER ============
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
      items += '<div class="item-card" onclick="openItem(\\'' + cat.id + '\\',\\'' + it.id + '\\')">' +
        '<h3>' + it.nome + '</h3><p>' + it.descricao + '</p>' +
        '<div class="price">R$ ' + it.tamanhos[0].preco.toFixed(2) + '</div></div>';
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
  var catId = btn.dataset.cat;
  var target = document.getElementById('cat-' + catId);
  if (target) {
    var headerH = document.querySelector('.header').offsetHeight + document.querySelector('.cat-nav').offsetHeight;
    window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - headerH - 10, behavior: 'smooth' });
  }
});

// ============ MODAL ============
function openItem(catId, itemId) {
  var cat = null, item = null;
  for (var i = 0; i < CARDAPIO.categorias.length; i++) {
    if (CARDAPIO.categorias[i].id === catId) {
      cat = CARDAPIO.categorias[i];
      for (var j = 0; j < cat.itens.length; j++) {
        if (cat.itens[j].id === itemId) { item = cat.itens[j]; break; }
      }
      break;
    }
  }
  if (!item) return;
  currentItem = item;
  currentCat = cat;
  selTamanho = item.tamanhos[0];
  selMetade = false;
  selSegundo = null;
  selBorda = 0;
  selQty = 1;
  var isPizza = catId.indexOf('pizza') >= 0;
  var h = '';
  h += '<div class="modal-header"><div><h2>' + item.nome + '</h2><p>' + item.descricao + '</p></div>';
  h += '<button class="modal-close" onclick="closeModal(\\'itemModal\\')">✕</button></div>';
  h += '<label class="label">Tamanho</label><div class="size-grid">';
  for (var i = 0; i < item.tamanhos.length; i++) {
    var t = item.tamanhos[i];
    h += '<button class="size-btn ' + (i === 0 ? 'active' : '') + '" onclick="selectTamanho(' + i + ')">';
    h += '<div>' + t.nome + '</div>';
    if (t.fatias) h += '<div class="slices">' + t.fatias + ' fatias</div>';
    h += '<span class="price">R$ ' + t.preco.toFixed(2) + '</span></button>';
  }
  h += '</div>';
  if (isPizza) {
    h += '<label class="label">Como deseja?</label><div class="toggle-row">';
    h += '<button class="toggle-btn active" id="btnInteira" onclick="setMetade(false)">Inteira<div style="font-size:11px;opacity:0.7">R$ ' + selTamanho.preco.toFixed(2) + '</div></button>';
    h += '<button class="toggle-btn" id="btnMetade" onclick="setMetade(true)">Metade/Metade<div style="font-size:11px;opacity:0.7">2 sabores</div></button>';
    h += '</div>';
    h += '<div id="metadeSection"></div>';
  }
  if (isPizza) {
    h += '<label class="label">Borda Recheada</label><div class="toggle-row">';
    h += '<button class="toggle-btn active" id="btnBordaNao" onclick="setBorda(0)">Sem borda</button>';
    h += '<button class="toggle-btn" id="btnBordaSim" onclick="setBorda(1)">Catupiry <span style="font-size:11px;opacity:0.7">+ R$ 8,00</span></button>';
    h += '</div>';
  }
  h += '<label class="label">Quantidade</label><div class="qty-row">';
  h += '<button class="qty-btn minus" onclick="changeQty(-1)">−</button>';
  h += '<span class="qty-val" id="qtyVal">' + selQty + '</span>';
  h += '<button class="qty-btn plus" onclick="changeQty(1)">+</button></div>';
  h += '<button class="add-btn" id="addBtn" onclick="addToCart()">Adicionar — R$ ' + calcPrice().toFixed(2) + '</button>';
  document.getElementById('modalContent').innerHTML = h;
  document.getElementById('itemModal').style.display = 'flex';
}

function selectTamanho(idx) {
  selTamanho = currentItem.tamanhos[idx];
  document.querySelectorAll('.size-btn').forEach(function(b) { b.classList.remove('active'); });
  event.target.closest('.size-btn').classList.add('active');
  var btn = document.getElementById('btnInteira');
  if (btn) btn.innerHTML = 'Inteira<div style="font-size:11px;opacity:0.7">R$ ' + selTamanho.preco.toFixed(2) + '</div>';
  if (selMetade) {
    var sec = document.getElementById('metadeSection');
    if (sec) {
      var spans = sec.querySelectorAll('.metade-row span');
      if (spans.length > 0) spans[spans.length - 1].textContent = 'R$ ' + selTamanho.preco.toFixed(2);
      var btns = sec.querySelectorAll('.sabor-btn');
      for (var i = 0; i < btns.length; i++) {
        var sid = btns[i].getAttribute('data-id');
        if (sid) {
          var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; });
          var s = todos.find(function(it) { return it.id === sid; });
          if (s) {
            var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
            var pm = Math.max(selTamanho.preco, sp.preco);
            var span = btns[i].querySelector('span');
            if (span) span.textContent = 'R$ ' + pm.toFixed(2);
          }
        }
      }
    }
  }
  updateAddBtn();
}

function setBorda(val) {
  selBorda = val;
  document.getElementById('btnBordaNao').classList.toggle('active', val === 0);
  document.getElementById('btnBordaSim').classList.toggle('active', val === 1);
  updateAddBtn();
}

function setMetade(val) {
  selMetade = val;
  selSegundo = null;
  document.getElementById('btnInteira').classList.toggle('active', !val);
  document.getElementById('btnMetade').classList.toggle('active', val);
  var sec = document.getElementById('metadeSection');
  if (val) {
    var h = '<div class="metade-info">';
    h += '<div class="metade-row"><span>1a metade: <strong>' + currentItem.nome + '</strong></span>';
    h += '<span style="color:#a855f7">R$ ' + selTamanho.preco.toFixed(2) + '</span></div>';
    h += '<div style="font-size:12px;color:#a1a1a1">Escolha a 2a metade:</div>';
    h += '<div style="font-size:11px;color:#f59e0b;margin-top:4px">O preco final sera da metade mais cara</div></div>';
    for (var c = 0; c < CARDAPIO.categorias.length; c++) {
      var cat = CARDAPIO.categorias[c];
      if (cat.id.indexOf('pizza') < 0) continue;
      var itens = cat.itens.filter(function(i) { return i.id !== currentItem.id; });
      if (itens.length === 0) continue;
      var icone = cat.id.indexOf('doce') >= 0 ? '🍫' : (cat.id.indexOf('especial') >= 0 ? '⭐' : '🍕');
      h += '<div class="cat-label">' + icone + ' ' + cat.nome + '</div><div class="sabor-grid">';
      for (var i = 0; i < itens.length; i++) {
        var s = itens[i];
        var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
        var pm = Math.max(selTamanho.preco, sp.preco);
        h += '<button class="sabor-btn" data-id="' + s.id + '" onclick="selectSegundo(\\'' + s.id + '\\')">' + s.nome + ' <span>R$ ' + pm.toFixed(2) + '</span></button>';
      }
      h += '</div>';
    }
    sec.innerHTML = h;
  } else {
    sec.innerHTML = '';
  }
  updateAddBtn();
}

function selectSegundo(id) {
  selSegundo = id;
  document.querySelectorAll('.sabor-btn').forEach(function(b) { b.classList.remove('active'); });
  event.target.closest('.sabor-btn').classList.add('active');
  updateAddBtn();
}

function changeQty(d) {
  selQty = Math.max(1, selQty + d);
  document.getElementById('qtyVal').textContent = selQty;
  updateAddBtn();
}

function calcPrice() {
  var preco = selTamanho.preco;
  if (selMetade && selSegundo) {
    var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; });
    var s = todos.find(function(i) { return i.id === selSegundo; });
    if (s) {
      var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
      preco = Math.max(preco, sp.preco);
    }
  }
  if (selBorda) preco += 8;
  return preco * selQty;
}

function updateAddBtn() {
  var btn = document.getElementById('addBtn');
  if (btn) {
    btn.textContent = 'Adicionar — R$ ' + calcPrice().toFixed(2);
    btn.disabled = selMetade && !selSegundo;
  }
}

function addToCart() {
  var nome = currentItem.nome;
  if (selMetade && selSegundo) {
    var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; });
    var s = todos.find(function(i) { return i.id === selSegundo; });
    if (s) nome = '1/2 ' + currentItem.nome + ' / 1/2 ' + s.nome;
  }
  if (selBorda) nome += ' (borda catupiry)';
  cart.push({ nome: nome, tamanho: selTamanho.nome, preco: calcPrice() / selQty, qty: selQty });
  closeModal('itemModal');
  updateCartButton();
}

function closeModal(id) {
  document.getElementById(id).style.display = 'none';
}

// ============ HORARIO HEADER ============
function updateHorarioHeader() {
  var aberta = isPizzariaAberta();
  var badge = document.getElementById('openBadge');
  var aviso = document.getElementById('horarioAviso');
  if (badge) {
    badge.textContent = aberta ? 'Aberto' : 'Fechado';
    badge.style.color = aberta ? '#4ade80' : '#f87171';
    badge.style.background = aberta ? 'rgba(74,222,128,.15)' : 'rgba(248,113,113,.15)';
  }
  if (aviso) {
    aviso.style.display = aberta ? 'none' : 'block';
    if (!aberta) aviso.textContent = getHorarioInfo();
  }
}

// ============ CARRINHO ============
function updateCartButton() {
  var btn = document.getElementById('cartBtn');
  if (!btn) return;
  var count = 0, total = 0;
  for (var i = 0; i < cart.length; i++) { count += cart[i].qty; total += cart[i].preco * cart[i].qty; }
  if (count > 0) {
    btn.style.display = 'block';
    var aberta = isPizzariaAberta();
    if (aberta) {
      document.getElementById('cartCount').textContent = count + ' item' + (count > 1 ? 's' : '');
      document.getElementById('cartTotal').textContent = 'R$ ' + total.toFixed(2);
    } else {
      document.getElementById('cartCount').textContent = 'Fechado';
      document.getElementById('cartTotal').textContent = 'R$ ' + total.toFixed(2);
    }
  } else {
    btn.style.display = 'none';
  }
}

function toggleCart() {
  if (!isPizzariaAberta()) {
    alert('Estamos fechados!\\n\\nHorario de funcionamento:\\nTerca a Domingo, das 18h as 00h.');
    return;
  }
  var modal = document.getElementById('cartModal');
  modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
  if (modal.style.display === 'flex') renderCart();
}

function renderCart() {
  var h = '';
  var total = 0;
  for (var i = 0; i < cart.length; i++) {
    var it = cart[i];
    h += '<div class="cart-item"><div class="cart-item-info"><div class="name">' + it.qty + 'x ' + it.nome + ' (' + it.tamanho + ')</div>';
    h += '<div class="price">R$ ' + (it.preco * it.qty).toFixed(2) + '</div></div>';
    h += '<button onclick="removeCartItem(' + i + ')" style="background:none;border:none;color:#f87171;font-size:18px;cursor:pointer">✕</button></div>';
    total += it.preco * it.qty;
  }
  h += '<div class="cart-summary">';
  h += '<div class="cart-summary-row"><span class="lbl">Subtotal</span><span>R$ ' + total.toFixed(2) + '</span></div>';
  h += '<div class="cart-summary-row"><span class="lbl">Entrega</span><span>Calculada no checkout</span></div>';
  h += '<div class="cart-summary-total"><span>Total</span><span class="val">R$ ' + total.toFixed(2) + '</span></div>';
  h += '<button class="add-btn" onclick="goCheckout()">Finalizar Pedido</button></div>';
  document.getElementById('cartContent').innerHTML = h;
}

function removeCartItem(idx) {
  cart.splice(idx, 1);
  updateCartButton();
  renderCart();
}

// ============ CHECKOUT ============
function goCheckout() {
  document.getElementById('cartModal').style.display = 'none';
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
  document.getElementById('complemento').value = '';
  document.getElementById('referencia').value = '';
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
  var total = 0;
  for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
  var h = '<div class="cart-summary">';
  for (var i = 0; i < cart.length; i++) {
    var it = cart[i];
    h += '<div class="cart-summary-row"><span class="lbl">' + it.qty + 'x ' + it.nome + ' (' + it.tamanho + ')</span><span>R$ ' + (it.preco * it.qty).toFixed(2) + '</span></div>';
  }
  h += '<div class="cart-summary-row"><span class="lbl">Subtotal</span><span>R$ ' + total.toFixed(2) + '</span></div>';
  var entrega = zonaAtual ? zonaAtual.valor : 0;
  var distInfo = zonaAtual ? zonaAtual.distKm.toFixed(1) + ' km' : '';
  if (zonaAtual) {
    h += '<div class="cart-summary-row"><span class="lbl">Distancia</span><span class="val">' + distInfo + '</span></div>';
    h += '<div class="cart-summary-row"><span class="lbl">Entrega</span><span class="val" style="color:' + (zonaAtual.valor === 0 ? '#4ade80' : '#a855f7') + '">' + (zonaAtual.valor === 0 ? 'GRATIS' : 'R$ ' + zonaAtual.valor.toFixed(2)) + '</span></div>';
    h += '<div class="cart-summary-row"><span class="lbl">Tempo estimado</span><span class="val">' + zonaAtual.tempo + '</span></div>';
  }
  if (total > 0 && total < MIN_PEDIDO_GRATIS && zonaAtual && zonaAtual.valor > 0) {
    var falta = MIN_PEDIDO_GRATIS - total;
    h += '<div style="margin-top:8px;padding:8px;background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.3);border-radius:8px;font-size:12px;color:#4ade80;text-align:center">Falta R$ ' + falta.toFixed(2) + ' para entrega GRATIS!</div>';
  }
  h += '<div class="cart-summary-total"><span>Total</span><span class="val">R$ ' + (total + entrega).toFixed(2) + '</span></div></div>';
  document.getElementById('checkoutSummary').innerHTML = h;
}

function buscarCEP() {
  var cep = document.getElementById('cep').value.replace(/\\D/g, '');
  if (cep.length !== 8) return;
  var status = document.getElementById('cepStatus');
  status.style.display = 'block';
  status.textContent = 'Buscando...';
  status.style.color = '#a1a1a1';
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'https://viacep.com.br/ws/' + cep + '/json/', true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          if (data.erro) { status.textContent = 'CEP nao encontrado'; status.style.color = '#f87171'; return; }
          document.getElementById('rua').value = data.logradouro || '';
          document.getElementById('bairro').value = data.bairro || '';
          document.getElementById('cidade').value = (data.localidade || '') + (data.uf ? ' - ' + data.uf : '');
          status.textContent = data.logradouro + ', ' + data.bairro;
          status.style.color = '#4ade80';
          document.getElementById('cep').value = cep.substring(0,5) + '-' + cep.substring(5);
          calcularEntrega();
          document.getElementById('numero').focus();
        } catch(e) { status.textContent = 'Erro. Preencha manualmente.'; status.style.color = '#f87171'; }
      } else { status.textContent = 'Erro de rede.'; status.style.color = '#f59e0b'; }
    }
  };
  xhr.send();
}

function selectPay(btn) {
  document.querySelectorAll('.pay-btn').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  var pay = btn.dataset.pay;
  document.getElementById('trocoSection').style.display = pay === 'dinheiro' ? 'block' : 'none';
  document.getElementById('pixSection').style.display = pay === 'pix' ? 'block' : 'none';
  if (pay === 'pix') updatePixData();
}

function updatePixData() {
  var total = 0;
  for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
  var entrega = zonaAtual ? zonaAtual.valor : 0;
  document.getElementById('pixValor').textContent = 'R$ ' + (total + entrega).toFixed(2);
}

function copyPixKey() {
  var key = document.getElementById('pixKey').textContent;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(key).then(function() { showCopyMsg(); }).catch(function() { fallbackCopyPix(key); });
  } else { fallbackCopyPix(key); }
}

function fallbackCopyPix(text) {
  var ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand('copy'); showCopyMsg(); } catch(e) { alert('Copie manualmente: ' + text); }
  document.body.removeChild(ta);
}

function showCopyMsg() {
  var msg = document.getElementById('copyMsg');
  msg.style.display = 'block';
  setTimeout(function() { msg.style.display = 'none'; }, 2000);
}

function submitOrder() {
  var nome = document.getElementById('nome').value.trim();
  var telefone = document.getElementById('telefone').value.trim();
  var cep = document.getElementById('cep').value.trim();
  var rua = document.getElementById('rua').value.trim();
  var numero = document.getElementById('numero').value.trim();
  var bairro = document.getElementById('bairro').value.trim();
  var cidade = document.getElementById('cidade').value.trim();
  var complemento = document.getElementById('complemento').value.trim();
  var referencia = document.getElementById('referencia').value.trim();
  var obs = document.getElementById('obs').value.trim();
  var pay = document.querySelector('.pay-btn.active').dataset.pay;
  var troco = document.getElementById('troco').value.trim();
  
  if (!nome) { showError('Informe seu nome.'); return; }
  if (!telefone) { showError('Informe seu telefone.'); return; }
  if (!rua || !numero || !bairro) { showError('Preencha o endereco completo.'); return; }
  if (!zonaAtual) { showError('Nao foi possivel calcular a entrega. Verifique o CEP.'); return; }
  
  var total = 0;
  for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
  var entrega = zonaAtual.valor;
  var totalFinal = total + entrega;
  
  var pedidoId = 'PZ' + Date.now().toString().slice(-6);
  var msg = '🍕 *NOVO PEDIDO* - ' + pedidoId + '%0A%0A';
  msg += '👤 *Cliente:* ' + nome + '%0A';
  msg += '📱 *Telefone:* ' + telefone + '%0A%0A';
  msg += '📦 *Itens:*%0A';
  for (var i = 0; i < cart.length; i++) {
    var it = cart[i];
    msg += '• ' + it.qty + 'x ' + it.nome + ' (' + it.tamanho + ') - R$ ' + (it.preco * it.qty).toFixed(2) + '%0A';
  }
  msg += '%0A💰 *Subtotal:* R$ ' + total.toFixed(2) + '%0A';
  msg += '🛵 *Entrega:* ' + (entrega === 0 ? 'GRATIS' : 'R$ ' + entrega.toFixed(2) + ' (' + zonaAtual.nome + ')') + '%0A';
  msg += '💵 *Total:* R$ ' + totalFinal.toFixed(2) + '%0A%0A';
  
  var pagNome = { dinheiro: 'Dinheiro', pix: 'PIX', 'cartao-credito': 'Cartao Credito', 'cartao-debito': 'Cartao Debito' };
  msg += '💳 *Pagamento:* ' + pagNome[pay] + '%0A';
  if (pay === 'dinheiro' && troco) msg += '💵 *Troco para:* R$ ' + troco + '%0A';
  
  msg += '%0A📍 *Endereco:*%0A';
  msg += rua + ', ' + numero;
  if (complemento) msg += ' ' + complemento;
  msg += ' - ' + bairro + ', ' + cidade + '%0A';
  if (referencia) msg += 'Ref: ' + referencia + '%0A';
  if (obs) msg += '%0A📝 ' + obs + '%0A';
  
  salvarPedido(pedidoId, nome, telefone);
  document.getElementById('checkoutForm').style.display = 'none';
  document.getElementById('checkoutSuccess').style.display = 'block';
  document.getElementById('pedidoNum').textContent = pedidoId;
  document.getElementById('waLink').href = 'https://wa.me/5519984356289?text=' + encodeURIComponent(msg);
}

function showError(msg) {
  var el = document.getElementById('checkoutError');
  el.textContent = msg;
  el.style.display = 'block';
}

function salvarPedido(pedidoId, nome, telefone) {
  try {
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var total = 0;
    for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
    pedidos.push({ id: pedidoId, nome: nome, telefone: telefone, itens: cart.slice(), total: total, entrega: zonaAtual ? zonaAtual.valor : 0, status: 'recebido', data: new Date().toISOString() });
    localStorage.setItem('pizzaPedidos', JSON.stringify(pedidos));
  } catch(e) {}
}

// ============ PEDIDOS ============
var STATUS_PEDIDO = {
  recebido: { nome: 'Recebido', class: 'recebido', statusClass: 'status-recebido' },
  confirmado: { nome: 'Confirmado', class: 'confirmado', statusClass: 'status-confirmado' },
  em_preparo: { nome: 'Em Preparo', class: 'em_preparo', statusClass: 'status-em_preparo' },
  no_forno: { nome: 'No Forno', class: 'no_forno', statusClass: 'status-no_forno' },
  saiu_entrega: { nome: 'Saiu p/ Entrega', class: 'saiu_entrega', statusClass: 'status-saiu_entrega' },
  entregue: { nome: 'Entregue', class: 'entregue', statusClass: 'status-entregue' },
  cancelado: { nome: 'Cancelado', class: 'cancelado', statusClass: 'status-cancelado' }
};

function carregarPedidos() {
  try {
    var telefone = document.getElementById('telefone').value.trim();
    if (!telefone) return;
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var meus = pedidos.filter(function(p) { return p.telefone === telefone; });
    var el = document.getElementById('meusPedidos');
    if (!el) return;
    if (meus.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido encontrado</div>'; return; }
    var h = '';
    for (var i = meus.length - 1; i >= 0; i--) {
      var p = meus[i];
      var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido;
      h += '<div class="pedido-card ' + st.class + '">';
      h += '<div style="display:flex;justify-content:space-between"><strong>' + p.id + '</strong><span class="status-badge ' + st.statusClass + '">' + st.nome + '</span></div>';
      h += '<div style="font-size:12px;color:#a1a1a1;margin-top:4px">' + new Date(p.data).toLocaleString('pt-BR') + '</div>';
      h += '<div style="font-size:13px;margin-top:4px">R$ ' + (p.total + p.entrega).toFixed(2) + '</div></div>';
    }
    el.innerHTML = h;
  } catch(e) {}
}

// ============ ADMIN ============
function showAdminLogin() {
  var senha = prompt('Senha admin:');
  if (senha === '1234') {
    document.getElementById('adminPage').style.display = 'block';
    document.getElementById('cardapio').style.display = 'none';
    document.getElementById('catNavMenu').style.display = 'none';
    carregarAdminPedidos();
  }
}

function carregarAdminPedidos() {
  try {
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var el = document.getElementById('adminPedidos');
    if (!el) return;
    if (pedidos.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido</div>'; return; }
    var h = '';
    for (var i = pedidos.length - 1; i >= 0; i--) {
      var p = pedidos[i];
      var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido;
      h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\\'' + p.id + '\\')">';
      h += '<div style="display:flex;justify-content:space-between"><strong>' + p.id + '</strong><span class="status-badge ' + st.statusClass + '">' + st.nome + '</span></div>';
      h += '<div style="font-size:12px;color:#a1a1a1">' + p.nome + ' - ' + p.telefone + '</div>';
      h += '<div style="font-size:13px;margin-top:4px">R$ ' + (p.total + p.entrega).toFixed(2) + '</div></div>';
    }
    el.innerHTML = h;
  } catch(e) {}
}

function verPedidoAdmin(id) {
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
  var p = pedidos.find(function(x) { return x.id === id; });
  if (!p) return;
  var h = '<h3>' + p.id + '</h3><p><strong>' + p.nome + '</strong> - ' + p.telefone + '</p>';
  h += '<p>Status: ' + p.status + '</p><h4>Itens:</h4>';
  for (var i = 0; i < p.itens.length; i++) {
    var it = p.itens[i];
    h += '<p>' + it.qty + 'x ' + it.nome + ' (' + it.tamanho + ') - R$ ' + (it.preco * it.qty).toFixed(2) + '</p>';
  }
  h += '<p><strong>Total: R$ ' + (p.total + p.entrega).toFixed(2) + '</strong></p>';
  h += '<div style="display:flex;gap:8px;margin-top:16px">';
  var statuses = ['recebido','confirmado','em_preparo','no_forno','saiu_entrega','entregue','cancelado'];
  for (var s = 0; s < statuses.length; s++) {
    h += '<button onclick="alterarStatus(\\'' + id + '\\',\\'' + statuses[s] + '\\')" style="padding:6px 12px;border-radius:8px;border:none;cursor:pointer;font-size:12px;background:' + (p.status === statuses[s] ? '#581c87' : '#1a1a1a') + ';color:' + (p.status === statuses[s] ? '#fff' : '#a1a1a1') + '">' + STATUS_PEDIDO[statuses[s]].nome + '</button>';
  }
  h += '</div>';
  document.getElementById('adminPedidoDetalhe').innerHTML = h;
}

function alterarStatus(id, status) {
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
  var p = pedidos.find(function(x) { return x.id === id; });
  if (p) { p.status = status; localStorage.setItem('pizzaPedidos', JSON.stringify(pedidos)); carregarAdminPedidos(); verPedidoAdmin(id); }
}

function filterAdmin(filter, btn) {
  document.querySelectorAll('.admin-filter').forEach(function(b) { b.style.background = '#1a1a1a'; b.style.color = '#a1a1a1'; });
  btn.style.background = '#581c87';
  btn.style.color = '#fff';
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
  var filtrados = filter === 'todos' ? pedidos : pedidos.filter(function(p) { return p.status === filter; });
  var el = document.getElementById('adminPedidos');
  if (filtrados.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido</div>'; return; }
  var h = '';
  for (var i = filtrados.length - 1; i >= 0; i--) {
    var p = filtrados[i];
    var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido;
    h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\\'' + p.id + '\\')">';
    h += '<div style="display:flex;justify-content:space-between"><strong>' + p.id + '</strong><span class="status-badge ' + st.statusClass + '">' + st.nome + '</span></div>';
    h += '<div style="font-size:12px;color:#a1a1a1">' + p.nome + ' - ' + p.telefone + '</div>';
    h += '<div style="font-size:13px;margin-top:4px">R$ ' + (p.total + p.entrega).toFixed(2) + '</div></div>';
  }
  el.innerHTML = h;
}

function goBack() {
  document.getElementById('checkoutPage').style.display = 'none';
  document.getElementById('adminPage').style.display = 'none';
  document.getElementById('cardapio').style.display = 'block';
  document.getElementById('catNavMenu').style.display = 'flex';
}

// ============ INIT ============
document.addEventListener('DOMContentLoaded', function() {
  updateHorarioHeader();
  initPizzariaCoords();
  render();
});
setInterval(updateHorarioHeader, 60000);

// Fechar modais clicando no overlay
document.getElementById('itemModal').addEventListener('click', function(e) { if (e.target === this) this.style.display = 'none'; });
document.getElementById('cartModal').addEventListener('click', function(e) { if (e.target === this) this.style.display = 'none'; });

// Atualizar pedidos quando volta da aba
document.addEventListener('visibilitychange', function() { if (document.visibilityState === 'visible') carregarPedidos(); });
setInterval(carregarPedidos, 15000);
</script>
</body>
</html>"""

# Montar arquivo final
final = html_part + new_js

with open('app.html', 'w') as f:
    f.write(final)

print(f"Arquivo reconstruido: {len(final)} chars")
print("JS valido!")
