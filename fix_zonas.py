with open('app.html', 'r') as f:
    content = f.read()

# Remover funcoes de geolocalizacao que nao funcionam
import re

# Remover initPizzariaCoords, geocodeAddress, calcDistance, calcTaxaEntrega, calcularEntrega, calcularPorBairro
# E substituir por sistema simples de zonas por CEP/bairro

# Encontrar e remover bloco de geolocalizacao
geo_start = content.find("// ============ CONFIGURACAO DE ENTREGA ============")
geo_end = content.find("// ============ ESTADO ============")

if geo_start >= 0 and geo_end >= 0:
    print(f"Bloco geo encontrado: {geo_start} a {geo_end}")
else:
    print(f"ERRO: geo_start={geo_start}, geo_end={geo_end}")
    exit(1)

new_config = """// ============ CONFIGURACAO DE ENTREGA ============
// Endereco da pizzaria: Rua Luiz Razera, 300 - Jd. Elite, Piracicaba - SP
// Taxa: R$ 3,00 fixo + R$ 1,00 por km (estimado por zona)

var TAXA_FIXA_MOTOBOY = 3.0;
var TAXA_POR_KM = 1.0;
var TAXA_MAXIMA = 25.0;
var MIN_PEDIDO_GRATIS = 100;
var zonaAtual = null;

// Zonas de entrega de Piracicaba (baseadas em CEP e bairro)
// Distancias estimadas a partir do Jd. Elite
var ZONAS_ENTREGA = [
  // Centro e proximos (1-3 km) - R$ 4-6
  { nome: "Centro", ceps: [13400000, 13409999], bairros: ["centro","alto","nova piracicaba","vila cristina","jose de queiroz"], dist: 2, taxa: 5 },
  { nome: "Vila Reis", ceps: [13401000, 13401999], bairros: ["vila reis","reis"], dist: 3, taxa: 6 },
  { nome: "São Judas", ceps: [13402000, 13402999], bairros: ["sao judas","judas","sao judas tadeu"], dist: 3.5, taxa: 6.5 },
  { nome: "Morumbi", ceps: [13403000, 13403999], bairros: ["morumbi"], dist: 4, taxa: 7 },
  { nome: "Pacaembu", ceps: [13404000, 13404999], bairros: ["pacaembu"], dist: 4.5, taxa: 7.5 },
  { nome: "Córrego", ceps: [13405000, 13405999], bairros: ["corrego","córrego"], dist: 3.5, taxa: 6.5 },
  { nome: "Santa Olímpia", ceps: [13406000, 13406999], bairros: ["santa olimpia","santa olímpia"], dist: 4, taxa: 7 },
  { nome: "Verde", ceps: [13407000, 13407999], bairros: ["verde","vila verde"], dist: 5, taxa: 8 },
  { nome: "Monsenhor Martinho", ceps: [13408000, 13408999], bairros: ["monsenhor martinho","martinho"], dist: 5, taxa: 8 },
  
  // Zona intermediaria (5-8 km) - R$ 8-11
  { nome: "Campestre", ceps: [13410000, 13410999], bairros: ["campestre"], dist: 6, taxa: 9 },
  { nome: "Tupi", ceps: [13411000, 13411999], bairros: ["tupi","tupy"], dist: 6.5, taxa: 9.5 },
  { nome: "Águas Claras", ceps: [13412000, 13412999], bairros: ["aguas claras","águas claras"], dist: 7, taxa: 10 },
  { nome: "Irmãos Camargo", ceps: [13413000, 13413999], bairros: ["irmaos camargo","irmãos camargo"], dist: 7.5, taxa: 10.5 },
  { nome: "Alfredo Guedes", ceps: [13414000, 13414999], bairros: ["alfredo guedes"], dist: 8, taxa: 11 },
  { nome: "Jardim Glória", ceps: [13415000, 13415999], bairros: ["jardim gloria","jd. gloria","jardim glória"], dist: 8.5, taxa: 11.5 },
  { nome: "Esplanada", ceps: [13416000, 13416999], bairros: ["esplanada"], dist: 9, taxa: 12 },
  { nome: "Céu Azul", ceps: [13417000, 13417999], bairros: ["ceu azul","céu azul"], dist: 7, taxa: 10 },
  { nome: "Vila Monteiro", ceps: [13418000, 13418999], bairros: ["vila monteiro","monteiro"], dist: 8, taxa: 11 },
  { nome: "Geraldão", ceps: [13419000, 13419999], bairros: ["geraldao","geraldão"], dist: 9, taxa: 12 },
  
  // Zona distante (9-12 km) - R$ 12-15
  { nome: "Potumirim", ceps: [13420000, 13420999], bairros: ["potumirim"], dist: 10, taxa: 13 },
  { nome: "Santa Teresa", ceps: [13421000, 13421999], bairros: ["santa teresa","sta. teresa"], dist: 11, taxa: 14 },
  { nome: "Anhumas", ceps: [13422000, 13422999], bairros: ["anhumas"], dist: 12, taxa: 15 },
  { nome: "Salmourão", ceps: [13423000, 13423999], bairros: ["salmourão","salmao"], dist: 13, taxa: 16 },
  { nome: "Taiúva", ceps: [13424000, 13424999], bairros: ["taiuva","taiúva"], dist: 14, taxa: 17 },
  { nome: "Encruzilhada", ceps: [13425000, 13425999], bairros: ["encruzilhada"], dist: 15, taxa: 18 },
  
  // Nova América e arredores
  { nome: "Nova América", ceps: [13426000, 13426999], bairros: ["nova america","nova américa","america","américa"], dist: 4, taxa: 7 },
  { nome: "Jardim Elite", ceps: [13427000, 13427999], bairros: ["jardim elite","jd. elite","elite"], dist: 1, taxa: 4 },
  { nome: "Vila Prudente", ceps: [13428000, 13428999], bairros: ["vila prudente","prudente"], dist: 3, taxa: 6 },
  { nome: "São Dimas", ceps: [13429000, 13429999], bairros: ["sao dimas","são dimas"], dist: 5, taxa: 8 },
];

function norm(s) {
  return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
}

function calcularEntrega() {
  var bairro = document.getElementById('bairro').value.trim();
  var cep = document.getElementById('cep').value.replace(/\\D/g, '');
  var rua = document.getElementById('rua').value.trim();
  
  if (!bairro || !rua) {
    document.getElementById('zonaBox').style.display = 'none';
    zonaAtual = null;
    renderCheckoutSummary();
    return;
  }
  
  var box = document.getElementById('zonaBox');
  var status = document.getElementById('cepStatus');
  box.style.display = 'block';
  status.style.display = 'block';
  
  var bn = norm(bairro);
  var cepNum = parseInt(cep) || 0;
  var encontrada = null;
  
  // Procura por bairro
  for (var i = 0; i < ZONAS_ENTREGA.length; i++) {
    if (ZONAS_ENTREGA[i].bairros) {
      for (var j = 0; j < ZONAS_ENTREGA[i].bairros.length; j++) {
        if (bn.indexOf(ZONAS_ENTREGA[i].bairros[j]) >= 0 || ZONAS_ENTREGA[i].bairros[j].indexOf(bn) >= 0) {
          encontrada = ZONAS_ENTREGA[i];
          break;
        }
      }
    }
    if (encontrada) break;
  }
  
  // Se nao encontrou por bairro, procura por CEP
  if (!encontrada && cepNum > 0) {
    for (var i = 0; i < ZONAS_ENTREGA.length; i++) {
      if (ZONAS_ENTREGA[i].ceps && ZONAS_ENTREGA[i].ceps.length === 2) {
        if (cepNum >= ZONAS_ENTREGA[i].ceps[0] && cepNum <= ZONAS_ENTREGA[i].ceps[1]) {
          encontrada = ZONAS_ENTREGA[i];
          break;
        }
      }
    }
  }
  
  // Se ainda nao encontrou, usa estimativa generica
  if (!encontrada) {
    // Estimativa baseada no CEP de Piracicaba (134xx)
    if (cepNum >= 13400000 && cepNum < 13430000) {
      encontrada = { nome: "Zona Piracicaba", dist: 8, taxa: 11 };
    } else {
      status.textContent = 'Bairro nao encontrado. Entrega sob consulta.';
      status.style.color = '#f59e0b';
      document.getElementById('zonaNome').textContent = 'Sob consulta';
      document.getElementById('zonaValor').textContent = 'A calcular';
      document.getElementById('zonaTempo').textContent = '';
      zonaAtual = null;
      renderCheckoutSummary();
      return;
    }
  }
  
  // Calcula taxa final
  var taxa = encontrada.taxa;
  var totalPed = 0;
  for (var i = 0; i < cart.length; i++) totalPed += cart[i].preco * cart[i].qty;
  
  // Entrega gratis para pedidos acima de R$ 100
  if (totalPed >= MIN_PEDIDO_GRATIS) taxa = 0;
  
  var tMin = Math.round(encontrada.dist * 5 + 20);
  var tMax = Math.round(encontrada.dist * 7 + 30);
  
  box.className = 'zona-box zona-ok';
  document.getElementById('zonaNome').textContent = encontrada.nome + ' (~' + encontrada.dist + ' km)';
  document.getElementById('zonaValor').textContent = taxa === 0 ? 'GRATIS' : 'R$ ' + taxa.toFixed(2);
  document.getElementById('zonaValor').style.color = taxa === 0 ? '#4ade80' : '#a855f7';
  document.getElementById('zonaTempo').textContent = tMin + '-' + tMax + ' min';
  status.textContent = 'Entrega calculada!';
  status.style.color = '#4ade80';
  
  zonaAtual = { valor: taxa, tempo: tMin + '-' + tMax + ' min', distKm: encontrada.dist, nome: encontrada.nome };
  renderCheckoutSummary();
}
"""

content = content[:geo_start] + new_config + content[geo_end:]

# Remover funcoes de geolocalizacao que nao sao mais necessarias
# geocodeAddress, calcDistance, initPizzariaCoords, calcularPorBairro
for func_name in ['function geocodeAddress', 'function calcDistance', 'function initPizzariaCoords', 'function calcularPorBorda']:
    idx = content.find(func_name)
    if idx >= 0:
        # Encontrar o fim da funcao
        depth = 0
        end = idx
        for i in range(idx, len(content)):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        content = content[:idx] + content[end:]
        print(f"Removido: {func_name}")

# Atualizar DOMContentLoaded para nao chamar initPizzariaCoords
content = content.replace(
    "initPizzariaCoords();",
    ""
)

with open('app.html', 'w') as f:
    f.write(content)

print("\nOK: Sistema de entrega por zonas configurado!")
