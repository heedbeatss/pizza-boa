with open('app.html', 'r') as f:
    content = f.read()

# 1. Substituir as ZONAS por um sistema de calculo por km
old_zonas = """var ZONAS = [
  { nome: "Centro", valor: 5, tempo: "30-40 min", bairros: ["centro","vila nova","bela vista"], cepIni: 13000000, cepFim: 13099999 },
  { nome: "Zona Norte", valor: 8, tempo: "40-50 min", bairros: ["jardim das flores","vila industrial"], cepIni: 13100000, cepFim: 13199999 },
  { nome: "Zona Sul", valor: 10, tempo: "45-55 min", bairros: ["vila madalena","pinheiros","sumare"], cepIni: 13200000, cepFim: 13299999 },
  { nome: "Zona Leste", valor: 12, tempo: "50-60 min", bairros: ["vila projetada","jardim aurora"], cepIni: 13300000, cepFim: 13399999 },
  { nome: "Zona Oeste", valor: 15, tempo: "55-70 min", bairros: ["vila reis","jardim esperanca"], cepIni: 13400000, cepFim: 13499999 }
];
var BAIRROS_GRATIS = ["centro","vila nova"];
var MIN_GRATIS = 50;"""

new_zonas = """// ========== CONFIGURACAO DE ENTREGA ==========
// Endereco da pizzaria (altere para o endereco real)
var PIZZARIA_ENDERECO = "Rua Exemplo, 123 - Centro, Campinas - SP";
var PIZZARIA_COORDS = null; // Sera calculado automaticamente

// Taxa por km (R$ 1,00 por km)
var TAXA_POR_KM = 1.0;
var TAXA_MINIMA = 5.0; // Taxa minima de entrega
var TAXA_MAXIMA = 25.0; // Taxa maxima de entrega
var RAIO_MAXIMO_KM = 15; // Nao entrega acima de X km

// Bairros com entrega gratis (deixe vazio [] se nao tiver)
var BAIRROS_GRATIS = [];
var MIN_GRATIS = 50; // Pedido minimo para entrega gratis

// Cache de coordenadas para evitar requisicoes repetidas
var coordsCache = {};"""

if old_zonas in content:
    content = content.replace(old_zonas, new_zonas, 1)
    print("OK: ZONAS substituido por configuracao de km")
else:
    print("ERRO: nao encontrou ZONAS")

# 2. Adicionar funcoes de geocodificacao e calculo de distancia
old_buscar = "function buscarCEP() {"
new_buscar = """// ========== GEOLOCALIZACAO ==========
function geocodeAddress(address, callback) {
  // Verifica cache
  var cacheKey = address.toLowerCase().trim();
  if (coordsCache[cacheKey]) {
    callback(null, coordsCache[cacheKey]);
    return;
  }
  
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
            var coords = { lat: parseFloat(data[0].lat), lon: parseFloat(data[0].lon) };
            coordsCache[cacheKey] = coords;
            callback(null, coords);
          } else {
            callback('Endereco nao encontrado', null);
          }
        } catch(e) {
          callback('Erro ao processar resposta', null);
        }
      } else {
        callback('Erro de rede: ' + xhr.status, null);
      }
    }
  };
  xhr.send();
}

// Calcula distancia entre dois pontos (Haversine)
function calcDistance(lat1, lon1, lat2, lon2) {
  var R = 6371; // Raio da Terra em km
  var dLat = (lat2 - lat1) * Math.PI / 180;
  var dLon = (lon2 - lon1) * Math.PI / 180;
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

// Calcula taxa de entrega baseada na distancia
function calcTaxaEntrega(distKm) {
  if (distKm <= 0) return 0;
  var taxa = Math.ceil(distKm) * TAXA_POR_KM; // Arredonda km pra cima
  taxa = Math.max(taxa, TAXA_MINIMA); // Aplica taxa minima
  taxa = Math.min(taxa, TAXA_MAXIMA); // Aplica taxa maxima
  return taxa;
}

// Inicializa coordenadas da pizzaria ao carregar
function initPizzariaCoords() {
  geocodeAddress(PIZZARIA_ENDERECO, function(err, coords) {
    if (!err && coords) {
      PIZZARIA_COORDS = coords;
      console.log('[Pizzaria] Coordenadas:', coords.lat, coords.lon);
    } else {
      console.warn('[Pizzaria] Erro ao geocodificar:', err);
    }
  });
}

function buscarCEP() {"""

if old_buscar in content:
    content = content.replace(old_buscar, new_buscar, 1)
    print("OK: funcoes de geolocalizacao adicionadas")
else:
    print("ERRO: nao encontrou buscarCEP")

# 3. Adicionar initPizzariaCoords no DOMContentLoaded
old_dom = "document.addEventListener('DOMContentLoaded', updateHorarioHeader);"
new_dom = "document.addEventListener('DOMContentLoaded', function() { updateHorarioHeader(); initPizzariaCoords(); });"
if old_dom in content:
    content = content.replace(old_dom, new_dom, 1)
    print("OK: initPizzariaCoords adicionado ao DOMContentLoaded")
else:
    print("ERRO: nao encontrou DOMContentLoaded")

# 4. Substituir calcularEntrega para usar km
old_calc = """function calcularEntrega() {
  var bairro = document.getElementById('bairro').value.trim();
  var cep = document.getElementById('cep').value.trim();
  
  if (!bairro) {
    document.getElementById('zonaBox').style.display = 'none';
    zonaAtual = null;
    renderCheckoutSummary();
    return;
  }
  
  var bn = norm(bairro);
  var cepNum = parseInt(cep.replace(/\\D/g, '')) || 0;"""

new_calc = """function calcularEntrega() {
  var bairro = document.getElementById('bairro').value.trim();
  var cep = document.getElementById('cep').value.trim();
  var rua = document.getElementById('rua').value.trim();
  var numero = document.getElementById('numero').value.trim();
  var cidade = document.getElementById('cidade').value.trim();
  
  if (!bairro || !rua) {
    document.getElementById('zonaBox').style.display = 'none';
    zonaAtual = null;
    renderCheckoutSummary();
    return;
  }
  
  var zonaBox = document.getElementById('zonaBox');
  var status = document.getElementById('cepStatus');
  zonaBox.style.display = 'block';
  document.getElementById('zonaNome').textContent = 'Calculando...';
  document.getElementById('zonaValor').textContent = '';
  document.getElementById('zonaTempo').textContent = '';
  
  // Monta endereco completo do cliente
  var enderecoCliente = rua + (numero ? ', ' + numero : '') + ', ' + bairro + ', ' + cidade;
  
  // Se pizzaria ainda nao tem coords, tenta inicializar
  if (!PIZZARIA_COORDS) {
    status.textContent = '⏳ Preparando sistema de entrega...';
    status.style.color = '#f59e0b';
    initPizzariaCoords();
    setTimeout(calcularEntrega, 2000); // Tenta de novo em 2s
    return;
  }
  
  // Geocodifica endereco do cliente
  geocodeAddress(enderecoCliente, function(err, coords) {
    if (err || !coords) {
      zonaBox.style.display = 'none';
      status.textContent = '⚠️ Nao foi possivel calcular a entrega. Tente novamente.';
      status.style.color = '#f59e0b';
      return;
    }
    
    // Calcula distancia
    var distKm = calcDistance(PIZZARIA_COORDS.lat, PIZZARIA_COORDS.lon, coords.lat, coords.lon);
    var taxa = calcTaxaEntrega(distKm);
    var tempoMin = Math.round(distKm * 5 + 20); // Estima 5min por km + 20min preparo
    var tempoMax = Math.round(distKm * 7 + 30);
    
    // Verifica raio maximo
    if (distKm > RAIO_MAXIMO_KM) {
      zonaBox.className = 'zona-box zona-erro';
      document.getElementById('zonaNome').textContent = 'Fora da area de entrega';
      document.getElementById('zonaValor').textContent = distKm.toFixed(1) + ' km';
      document.getElementById('zonaValor').style.color = '#f87171';
      document.getElementById('zonaTempo').textContent = 'Nao entregamos nessa regiao';
      zonaAtual = null;
      renderCheckoutSummary();
      return;
    }
    
    // Verifica se bairro e gratuito
    var bn = norm(bairro);
    var isGratis = BAIRROS_GRATIS.indexOf(bn) >= 0;
    var totalPedido = 0;
    for (var i = 0; i < cart.length; i++) totalPedido += cart[i].preco * cart[i].qty;
    if (isGratis && totalPedido >= MIN_GRATIS) taxa = 0;
    
    // Atualiza UI
    zonaBox.className = 'zona-box zona-ok';
    document.getElementById('zonaNome').textContent = distKm.toFixed(1) + ' km';
    document.getElementById('zonaValor').textContent = taxa === 0 ? 'GRATIS' : 'R$ ' + taxa.toFixed(2);
    document.getElementById('zonaValor').style.color = taxa === 0 ? '#4ade80' : '#a855f7';
    document.getElementById('zonaTempo').textContent = tempoMin + '-' + tempoMax + ' min';
    
    zonaAtual = { valor: taxa, tempo: tempoMin + '-' + tempoMax + ' min', distKm: distKm };
    renderCheckoutSummary();
  });
  
  var cepNum = parseInt(cep.replace(/\\D/g, '')) || 0;"""

if old_calc in content:
    content = content.replace(old_calc, new_calc, 1)
    print("OK: calcularEntrega substituido por versao com km")
else:
    print("ERRO: nao encontrou calcularEntrega")

# 5. Atualizar renderCheckoutSummary para mostrar distancia
old_summary = """  var entrega = zonaAtual ? zonaAtual.valor : 0;
  var totalFinal = total + entrega;"""

new_summary = """  var entrega = zonaAtual ? zonaAtual.valor : 0;
  var distInfo = zonaAtual ? zonaAtual.distKm.toFixed(1) + ' km' : '';
  var totalFinal = total + entrega;"""

if old_summary in content:
    content = content.replace(old_summary, new_summary, 1)
    print("OK: renderCheckoutSummary atualizado")
else:
    print("ERRO: nao encontrou renderCheckoutSummary")

# 6. Atualizar resumo do checkout para mostrar distancia
old_resumo = """  if (zonaAtual) {
    h += '<div class="cart-summary-row"><span class="lbl">Entrega</span><span class="val" style="color:' + (zonaAtual.valor === 0 ? '#4ade80' : '#a855f7') + '">' + (zonaAtual.valor === 0 ? 'GRATIS' : 'R$ ' + zonaAtual.valor.toFixed(2)) + '</span></div>';
    h += '<div class="cart-summary-row"><span class="lbl">Tempo estimado</span><span class="val">' + zonaAtual.tempo + '</span></div>';
  }"""

new_resumo = """  if (zonaAtual) {
    h += '<div class="cart-summary-row"><span class="lbl">Distancia</span><span class="val">' + distInfo + '</span></div>';
    h += '<div class="cart-summary-row"><span class="lbl">Entrega</span><span class="val" style="color:' + (zonaAtual.valor === 0 ? '#4ade80' : '#a855f7') + '">' + (zonaAtual.valor === 0 ? 'GRATIS' : 'R$ ' + zonaAtual.valor.toFixed(2)) + '</span></div>';
    h += '<div class="cart-summary-row"><span class="lbl">Tempo estimado</span><span class="val">' + zonaAtual.tempo + '</span></div>';
  }"""

if old_resumo in content:
    content = content.replace(old_resumo, new_resumo, 1)
    print("OK: resumo do checkout atualizado com distancia")
else:
    print("ERRO: nao encontrou resumo do checkout")

with open('app.html', 'w') as f:
    f.write(content)

print("\nTudo pronto!")
