with open('app.html', 'r') as f:
    content = f.read()

# Encontrar onde inserir o codigo de geolocalizacao (antes de buscarCEP)
insert_before = "function buscarCEP() {"
idx = content.find(insert_before)

if idx < 0:
    print("ERRO: nao encontrou buscarCEP")
    exit(1)

geo_code = """// ========== CONFIGURACAO DE ENTREGA ==========
// Endereco da pizzaria
var PIZZARIA_ENDERECO = "Rua Luiz Razera, 300 - Jd. Elite, Piracicaba - SP";
var PIZZARIA_COORDS = null;

// Taxa: R$ 3,00 fixo + R$ 1,00 por km
var TAXA_FIXA_MOTOBOY = 3.0;
var TAXA_POR_KM = 1.0;
var TAXA_MINIMA = 3.0;
var TAXA_MAXIMA = 30.0;
var RAIO_MAXIMO_KM = 15;
var MIN_PEDIDO_GRATIS = 100;

// Cache de coordenadas
var coordsCache = {};

function geocodeAddress(address, callback) {
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
          callback('Erro ao processar', null);
        }
      } else {
        callback('Erro de rede', null);
      }
    }
  };
  xhr.send();
}

function calcDistance(lat1, lon1, lat2, lon2) {
  var R = 6371;
  var dLat = (lat2 - lat1) * Math.PI / 180;
  var dLon = (lon2 - lon1) * Math.PI / 180;
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

function calcTaxaEntrega(distKm, totalPedido) {
  if (totalPedido >= MIN_PEDIDO_GRATIS) return 0;
  if (distKm <= 0) return TAXA_FIXA_MOTOBOY;
  var kmArredondado = Math.ceil(distKm);
  var taxa = TAXA_FIXA_MOTOBOY + (kmArredondado * TAXA_POR_KM);
  return Math.min(taxa, TAXA_MAXIMA);
}

function initPizzariaCoords() {
  geocodeAddress(PIZZARIA_ENDERECO, function(err, coords) {
    if (!err && coords) {
      PIZZARIA_COORDS = coords;
      console.log('[Pizzaria] OK:', coords.lat, coords.lon);
    } else {
      console.warn('[Pizzaria] Erro:', err);
    }
  });
}

function calcularEntrega() {
  var bairro = document.getElementById('bairro').value.trim();
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
  
  var enderecoCliente = rua + (numero ? ', ' + numero : '') + ', ' + bairro + ', ' + cidade;
  
  if (!PIZZARIA_COORDS) {
    status.textContent = 'Preparando sistema de entrega...';
    status.style.color = '#f59e0b';
    initPizzariaCoords();
    setTimeout(calcularEntrega, 2000);
    return;
  }
  
  geocodeAddress(enderecoCliente, function(err, coords) {
    if (err || !coords) {
      zonaBox.style.display = 'none';
      status.textContent = 'Nao foi possivel calcular a entrega.';
      status.style.color = '#f59e0b';
      return;
    }
    
    var distKm = calcDistance(PIZZARIA_COORDS.lat, PIZZARIA_COORDS.lon, coords.lat, coords.lon);
    var totalPedido = 0;
    for (var i = 0; i < cart.length; i++) totalPedido += cart[i].preco * cart[i].qty;
    var taxa = calcTaxaEntrega(distKm, totalPedido);
    var tempoMin = Math.round(distKm * 5 + 20);
    var tempoMax = Math.round(distKm * 7 + 30);
    
    if (distKm > RAIO_MAXIMO_KM) {
      zonaBox.className = 'zona-box zona-erro';
      document.getElementById('zonaNome').textContent = 'Fora da area';
      document.getElementById('zonaValor').textContent = distKm.toFixed(1) + ' km';
      document.getElementById('zonaValor').style.color = '#f87171';
      document.getElementById('zonaTempo').textContent = 'Nao entregamos';
      zonaAtual = null;
      renderCheckoutSummary();
      return;
    }
    
    zonaBox.className = 'zona-box zona-ok';
    document.getElementById('zonaNome').textContent = distKm.toFixed(1) + ' km';
    document.getElementById('zonaValor').textContent = taxa === 0 ? 'GRATIS' : 'R$ ' + taxa.toFixed(2);
    document.getElementById('zonaValor').style.color = taxa === 0 ? '#4ade80' : '#a855f7';
    document.getElementById('zonaTempo').textContent = tempoMin + '-' + tempoMax + ' min';
    
    zonaAtual = { valor: taxa, tempo: tempoMin + '-' + tempoMax + ' min', distKm: distKm, nome: distKm.toFixed(1) + ' km' };
    renderCheckoutSummary();
  });
}

"""

content = content[:idx] + geo_code + content[idx:]

# Adicionar initPizzariaCoords no DOMContentLoaded
content = content.replace(
    "document.addEventListener('DOMContentLoaded', function() { updateHorarioHeader(); });",
    "document.addEventListener('DOMContentLoaded', function() { updateHorarioHeader(); initPizzariaCoords(); });"
)

with open('app.html', 'w') as f:
    f.write(content)

print("OK: Codigo de entrega por km adicionado!")
