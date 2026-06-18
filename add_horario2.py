with open('app.html', 'r') as f:
    content = f.read()

# 1. Adicionar funcoes de horario depois do var cart
old1 = "var cart = [];\nvar zonaAtual = null;"

new1 = """var cart = [];
var zonaAtual = null;

// ========== HORARIO DE FUNCIONAMENTO ==========
// Terca a Domingo, 18h as 00h
// Dias: 0=Domingo, 1=Segunda, 2=Terca, 3=Quarta, 4=Quinta, 5=Sexta, 6=Sabado
var DIAS_FUNCIONAMENTO = [0, 2, 3, 4, 5, 6]; // Sem segunda-feira
var HORA_INICIO = 18; // 18h
var HORA_FIM = 24;    // 00h (meia-noite)

function isPizzariaAberta() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) return false;
  if (hora >= HORA_INICIO && hora < HORA_FIM) return true;
  return false;
}

function getHorarioInfo() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  var diaNome = ['Domingo','Segunda','Terca','Quarta','Quinta','Sexta','Sabado'][dia];
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) {
    return 'Hoje e ' + diaNome + '. Estamos fechados. Funcionamos de Terca a Domingo, das 18h as 00h.';
  }
  if (hora < HORA_INICIO) {
    return 'Ainda nao abrimos. Hoje abrimos as ' + HORA_INICIO + 'h.';
  }
  if (hora >= HORA_FIM) {
    return 'Ja fechamos por hoje. Abrimos novamente amanha as ' + HORA_INICIO + 'h.';
  }
  return 'Estamos abertos!';
}"""

if old1 in content:
    content = content.replace(old1, new1, 1)
    print("OK: funcoes de horario adicionadas")
else:
    print("ERRO: ponto 1")

# 2. Adicionar aviso de horario no header
old2 = '    <span class="badge" id="openBadge">Aberto</span>'

new2 = """    <span class="badge" id="openBadge" style="color:#4ade80;background:rgba(74,222,128,.15)">Aberto</span>
    <div id="horarioAviso" style="display:none;margin-top:8px;padding:8px 12px;background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);border-radius:8px;font-size:12px;color:#f87171;text-align:center"></div>"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("OK: aviso de horario no header")
else:
    print("ERRO: ponto 2")

# 3. Atualizar updateHorarioHeader (ja existe do script anterior, mas vamos garantir que esta certo)
# Primeiro remove se ja existe
if 'function updateHorarioHeader()' in content:
    # Ja existe, nao precisa adicionar de novo
    print("OK: updateHorarioHeader ja existe")
else:
    # Adiciona antes do updateCartButton
    old3 = "function updateCartButton() {"
    new3 = """function updateHorarioHeader() {
  var aberta = isPizzariaAberta();
  var badge = document.getElementById('openBadge');
  var aviso = document.getElementById('horarioAviso');
  if (badge) {
    if (aberta) {
      badge.textContent = 'Aberto';
      badge.style.color = '#4ade80';
      badge.style.background = 'rgba(74,222,128,.15)';
    } else {
      badge.textContent = 'Fechado';
      badge.style.color = '#f87171';
      badge.style.background = 'rgba(248,113,113,.15)';
    }
  }
  if (aviso) {
    if (!aberta) {
      aviso.style.display = 'block';
      aviso.textContent = getHorarioInfo();
    } else {
      aviso.style.display = 'none';
    }
  }
}
document.addEventListener('DOMContentLoaded', updateHorarioHeader);
setInterval(updateHorarioHeader, 60000);

function updateCartButton() {"""
    if old3 in content:
        content = content.replace(old3, new3, 1)
        print("OK: updateHorarioHeader adicionado")
    else:
        print("ERRO: ponto 3")

# 4. Atualizar updateCartButton para mostrar "Fechado" quando aplicavel
old4 = """function updateCartButton() {
  var btn = document.getElementById('cartBtn');
  var count = 0, total = 0;
  for (var i = 0; i < cart.length; i++) { count += cart[i].qty; total += cart[i].preco * cart[i].qty; }
  
  if (count > 0) {
    btn.style.display = 'block';
    document.getElementById('cartCount').textContent = count + ' item' + (count > 1 ? 's' : '');
    document.getElementById('cartTotal').textContent = 'R$ ' + total.toFixed(2);
  } else {
    btn.style.display = 'none';
  }
}"""

new4 = """function updateCartButton() {
  var btn = document.getElementById('cartBtn');
  var count = 0, total = 0;
  for (var i = 0; i < cart.length; i++) { count += cart[i].qty; total += cart[i].preco * cart[i].qty; }
  
  if (count > 0) {
    btn.style.display = 'block';
    var aberta = isPizzariaAberta();
    if (aberta) {
      document.getElementById('cartCount').textContent = count + ' item' + (count > 1 ? 's' : '');
      document.getElementById('cartTotal').textContent = 'R$ ' + total.toFixed(2);
      btn.querySelector('button').style.opacity = '1';
      btn.querySelector('button').style.cursor = 'pointer';
    } else {
      document.getElementById('cartCount').textContent = 'Fechado';
      document.getElementById('cartTotal').textContent = 'R$ ' + total.toFixed(2);
      btn.querySelector('button').style.opacity = '0.6';
      btn.querySelector('button').style.cursor = 'not-allowed';
    }
  } else {
    btn.style.display = 'none';
  }
}"""

if old4 in content:
    content = content.replace(old4, new4, 1)
    print("OK: updateCartButton atualizado")
else:
    print("ERRO: ponto 4")

# 5. Bloquear toggleCart (ja foi adicionado no script anterior)
if "if (!isPizzariaAberta())" in content:
    print("OK: toggleCart ja tem bloqueio")
else:
    old5 = "function toggleCart() {"
    new5 = """function toggleCart() {
  if (!isPizzariaAberta()) {
    alert('Estamos fechados!\\n\\nHorario de funcionamento:\\nTerca a Domingo, das 18h as 00h.\\n\\nFavor voltar quando estivermos abertos.');
    return;
  }
"""
    if old5 in content:
        content = content.replace(old5, new5, 1)
        print("OK: toggleCart com bloqueio")
    else:
        print("ERRO: ponto 5")

with open('app.html', 'w') as f:
    f.write(content)

print("\nPronto!")
