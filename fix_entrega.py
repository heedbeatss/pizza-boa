with open('app.html', 'r') as f:
    content = f.read()

# Substituir a funcao calcularEntrega inteira
old_func_start = "function calcularEntrega() {"
old_func_end = "  });\n}"

# Encontrar a funcao
start_idx = content.find(old_func_start)
if start_idx < 0:
    print("ERRO: nao encontrou calcularEntrega")
    exit(1)

# Encontrar o fim da funcao (balanceamento de chaves)
depth = 0
end_idx = start_idx
for i in range(start_idx, len(content)):
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end_idx = i + 1
            break

old_func = content[start_idx:end_idx]
print(f"Funcao encontrada: {start_idx} a {end_idx} ({len(old_func)} chars)")

new_func = """function calcularEntrega() {
  var bairro = document.getElementById('bairro').value.trim();
  var cep = document.getElementById('cep').value.replace(/\\D/g, '');
  
  if (!bairro || cep.length < 8) {
    document.getElementById('zonaBox').style.display = 'none';
    zonaAtual = null;
    renderCheckoutSummary();
    return;
  }
  
  var box = document.getElementById('zonaBox');
  var status = document.getElementById('cepStatus');
  box.style.display = 'block';
  status.style.display = 'block';
  status.textContent = 'Calculando entrega...';
  status.style.color = '#a1a1a1';
  
  // Tenta usar a API de geocodificacao
  var rua = document.getElementById('rua').value.trim();
  var numero = document.getElementById('numero').value.trim();
  var cidade = document.getElementById('cidade').value.trim();
  
  if (!rua) {
    // Se nao tem rua ainda, so mostra aguardando
    document.getElementById('zonaNome').textContent = 'Preencha o endereco';
    document.getElementById('zonaValor').textContent = '';
    document.getElementById('zonaTempo').textContent = '';
    zonaAtual = null;
    renderCheckoutSummary();
    return;
  }
  
  var endCliente = rua + (numero ? ', ' + numero : '') + ', ' + bairro + ', ' + cidade;
  
  // Se pizzaria ainda nao tem coords, inicializa
  if (!PIZZARIA_COORDS) {
    document.getElementById('zonaNome').textContent = 'Preparando...';
    document.getElementById('zonaValor').textContent = '';
    status.textContent = 'Preparando sistema de entrega...';
    status.style.color = '#f59e0b';
    initPizzariaCoords();
    setTimeout(calcularEntrega, 2000);
    return;
  }
  
  // Tenta geocodificar
  geocodeAddress(endCliente, function(err, coords) {
    if (err || !coords) {
      // Se falhar, usa estimativa baseada no bairro
      calcularPorBairro(bairro, cep);
      return;
    }
    
    var dist = calcDistance(PIZZARIA_COORDS.lat, PIZZARIA_COORDS.lon, coords.lat, coords.lon);
    var totalPed = 0; 
    for (var i = 0; i < cart.length; i++) totalPed += cart[i].preco * cart[i].qty;
    var taxa = calcTaxaEntrega(dist, totalPed);
    var tMin = Math.round(dist * 5 + 20);
    var tMax = Math.round(dist * 7 + 30);
    
    if (dist > RAIO_MAXIMO_KM) {
      box.className = 'zona-box zona-erro';
      document.getElementById('zonaNome').textContent = 'Fora da area';
      document.getElementById('zonaValor').textContent = dist.toFixed(1) + ' km';
      document.getElementById('zonaValor').style.color = '#f87171';
      document.getElementById('zonaTempo').textContent = 'Nao entregamos';
      status.textContent = 'Nao entregamos nessa regiao';
      status.style.color = '#f87171';
      zonaAtual = null;
      renderCheckoutSummary();
      return;
    }
    
    box.className = 'zona-box zona-ok';
    document.getElementById('zonaNome').textContent = dist.toFixed(1) + ' km';
    document.getElementById('zonaValor').textContent = taxa === 0 ? 'GRATIS' : 'R$ ' + taxa.toFixed(2);
    document.getElementById('zonaValor').style.color = taxa === 0 ? '#4ade80' : '#a855f7';
    document.getElementById('zonaTempo').textContent = tMin + '-' + tMax + ' min';
    status.textContent = 'Entrega calculada com sucesso!';
    status.style.color = '#4ade80';
    
    zonaAtual = { valor: taxa, tempo: tMin + '-' + tMax + ' min', distKm: dist, nome: dist.toFixed(1) + ' km' };
    renderCheckoutSummary();
  });
}

// Calcula baseado no bairro (fallback quando API falha)
function calcularPorBairro(bairro, cep) {
  var bn = norm(bairro);
  var cepNum = parseInt(cep) || 0;
  var box = document.getElementById('zonaBox');
  var status = document.getElementById('cepStatus');
  
  // Tabela de distancias por bairro de Piracicaba (km aproximada da pizzaria)
  var DISTANCIAS = [
    // Centro e proximos (1-3 km)
    { bairros: ['centro', 'centro histórico', 'represa'], dist: 1.5 },
    { bairros: ['alto', 'alto de piracicaba'], dist: 2.0 },
    { bairros: ['nova piracicaba', 'nova'], dist: 2.5 },
    { bairros: ['vila cristina', 'cristina'], dist: 2.0 },
    { bairros: ['jose de queiroz', 'jd. jose de queiroz'], dist: 2.5 },
    
    // Zona intermediaria (3-6 km)
    { bairros: ['vila reis', 'reis'], dist: 3.0 },
    { bairros: ['são judas', 'sao judas', 'judas'], dist: 3.5 },
    { bairros: ['morumbi'], dist: 4.0 },
    { bairros: ['paris', 'vl. paris'], dist: 4.0 },
    { bairros: ['pacaembu'], dist: 4.5 },
    { bairros: ['corrego corrego', 'corrego'], dist: 3.5 },
    { bairros: ['verde', 'vl. verde'], dist: 5.0 },
    { bairros: ['santa olímpia', 'santa olimpia'], dist: 4.0 },
    { bairros: ['monsenhor martinho', 'martinho'], dist: 5.0 },
    
    // Zona mais distante (6-10 km)
    { bairros: ['campestre'], dist: 6.0 },
    { bairros: ['tupi', 'tupy'], dist: 6.5 },
    { bairros: ['aguas claras', 'aguas'], dist: 7.0 },
    { bairros: ['irmãos camargo', 'irmaos camargo'], dist: 7.5 },
    { bairros: ['alfredo guedes'], dist: 8.0 },
    { bairros: ['jardim gloria', 'jd. gloria'], dist: 8.5 },
    { bairros: ['esplanada', 'esplanada i', 'esplanada ii'], dist: 9.0 },
    { bairros: ['céu azul', 'ceu azul'], dist: 7.0 },
    { bairros: ['vila monteiro', 'monteiro'], dist: 8.0 },
    { bairros: ['geraldão', 'geraldao'], dist: 9.0 },
    { bairros: ['potumirim'], dist: 10.0 },
    
    // Região rural/longe (10-15 km)
    { bairros: ['santa teresa', 'sta. teresa'], dist: 11.0 },
    { bairros: ['anhumas'], dist: 12.0 },
    { bairros: ['salmourão', 'salmao'], dist: 13.0 },
    { bairros: ['taiúva', 'taiuva'], dist: 14.0 },
    { bairros: ['encruzilhada'], dist: 15.0 },
  ];
  
  var encontrada = null;
  
  // Procura por nome do bairro
  for (var i = 0; i < DISTANCIAS.length; i++) {
    for (var j = 0; j < DISTANCIAS[i].bairros.length; j++) {
      if (bn.indexOf(DISTANCIAS[i].bairros[j]) >= 0 || DISTANCIAS[i].bairros[j].indexOf(bn) >= 0) {
        encontrada = DISTANCIAS[i];
        break;
      }
    }
    if (encontrada) break;
  }
  
  // Se nao encontrou por bairro, estima pelo CEP
  if (!encontrada) {
    // CEPs de Piracicaba: 13400-13499
    if (cepNum >= 13400000 && cepNum < 13410000) encontrada = { dist: 2.0 }; // Centro
    else if (cepNum >= 13410000 && cepNum < 13420000) encontrada = { dist: 3.5 };
    else if (cepNum >= 13420000 && cepNum < 13430000) encontrada = { dist: 4.0 };
    else if (cepNum >= 13430000 && cepNum < 13440000) encontrada = { dist: 5.0 };
    else if (cepNum >= 13440000 && cepNum < 13450000) encontrada = { dist: 6.0 };
    else if (cepNum >= 13450000 && cepNum < 13460000) encontrada = { dist: 7.0 };
    else if (cepNum >= 13460000 && cepNum < 13470000) encontrada = { dist: 8.0 };
    else encontrada = { dist: 10.0 }; // Default para areas desconhecidas
  }
  
  var dist = encontrada.dist;
  var totalPed = 0; 
  for (var i = 0; i < cart.length; i++) totalPed += cart[i].preco * cart[i].qty;
  var taxa = calcTaxaEntrega(dist, totalPed);
  var tMin = Math.round(dist * 5 + 20);
  var tMax = Math.round(dist * 7 + 30);
  
  box.className = 'zona-box zona-ok';
  document.getElementById('zonaNome').textContent = '~' + dist.toFixed(1) + ' km (estimado)';
  document.getElementById('zonaValor').textContent = taxa === 0 ? 'GRATIS' : 'R$ ' + taxa.toFixed(2);
  document.getElementById('zonaValor').style.color = taxa === 0 ? '#4ade80' : '#a855f7';
  document.getElementById('zonaTempo').textContent = tMin + '-' + tMax + ' min';
  status.textContent = 'Entrega calculada (estimativa por bairro)';
  status.style.color = '#4ade80';
  
  zonaAtual = { valor: taxa, tempo: tMin + '-' + tMax + ' min', distKm: dist, nome: '~' + dist.toFixed(1) + ' km' };
  renderCheckoutSummary();
}"""

content = content[:start_idx] + new_func + content[end_idx:]

with open('app.html', 'w') as f:
    f.write(content)

print("OK: calcularEntrega reescrita com fallback por bairro!")
