with open('app.html', 'r') as f:
    content = f.read()

# 1. Adicionar funcao de verificacao de horario no inicio do script (depois do CARDAPIO)
old = "var cart = JSON.parse(localStorage.getItem('pizzaCart')) || [];"

new = """var cart = JSON.parse(localStorage.getItem('pizzaCart')) || [];

// ========== HORARIO DE FUNCIONAMENTO ==========
// Terça a Domingo, 18h às 00h
// Dias: 0=Domingo, 1=Segunda, 2=Terca, 3=Quarta, 4=Quinta, 5=Sexta, 6=Sabado
var DIAS_FUNCIONAMENTO = [0, 2, 3, 4, 5, 6]; // Sem segunda-feira
var HORA_INICIO = 18; // 18h
var HORA_FIM = 24;    // 00h (meia-noite)

function isPizzariaAberta() {
  var agora = new Date();
  var dia = agora.getDay(); // 0-6
  var hora = agora.getHours();
  
  // Verifica se o dia está nos dias de funcionamento
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) return false;
  
  // Verifica se está no horário (18h às 24h)
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
  
  return 'Estamos abertos!'; // Nao deveria chegar aqui se isPizzariaAberta() for false
}
// ========== FIM HORARIO ==========
"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: funcoes de horario adicionadas")
else:
    print("ERRO: nao encontrou o ponto de insercao")

# 2. Adicionar aviso de horario no header (depois do badge)
old2 = """      <div style="display:flex;align-items:center;gap:8px">
        <span class="badge" id="openBadge">Aberto</span>
      </div>"""

new2 = """      <div style="display:flex;align-items:center;gap:8px">
        <span class="badge" id="openBadge">Aberto</span>
      </div>
      <div id="horarioAviso" style="display:none;margin-top:8px;padding:8px 12px;background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);border-radius:8px;font-size:12px;color:#f87171;text-align:center"></div>"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("OK: aviso de horario adicionado no header")
else:
    print("ERRO: nao encontrou o header badge")

# 3. Adicionar funcao que atualiza o estado do header baseada no horario
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

// Chama ao carregar
document.addEventListener('DOMContentLoaded', updateHorarioHeader);
// Atualiza a cada minuto
setInterval(updateHorarioHeader, 60000);

function updateCartButton() {"""

if old3 in content:
    content = content.replace(old3, new3, 1)
    print("OK: updateHorarioHeader adicionado")
else:
    print("ERRO: nao encontrou updateCartButton")

# 4. Bloquear botão do carrinho quando fechado
old4 = """function updateCartButton() {
  var btn = document.getElementById('cartBtn');
  if (!btn) return;
  
  var total = 0;
  for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
  
  if (cart.length === 0) {
    btn.style.display = 'none';
  } else {
    btn.style.display = 'block';
    btn.innerHTML = '<button>Ver carrinho (' + cart.length + ') — R$ ' + total.toFixed(2) + '</button>';
  }
}"""

new4 = """function updateCartButton() {
  var btn = document.getElementById('cartBtn');
  if (!btn) return;
  
  var total = 0;
  for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
  
  if (cart.length === 0) {
    btn.style.display = 'none';
  } else {
    btn.style.display = 'block';
    var aberta = isPizzariaAberta();
    if (aberta) {
      btn.innerHTML = '<button>Ver carrinho (' + cart.length + ') — R$ ' + total.toFixed(2) + '</button>';
    } else {
      btn.innerHTML = '<button style="opacity:.6;cursor:not-allowed">Fechado — R$ ' + total.toFixed(2) + '</button>';
    }
  }
}"""

if old4 in content:
    content = content.replace(old4, new4, 1)
    print("OK: botao do carrinho atualizado com bloqueio")
else:
    print("ERRO: nao encontrou updateCartButton completo")

# 5. Bloquear checkout quando fechado
old5 = "function toggleCart() {"

new5 = """function toggleCart() {
  // Bloqueia se a pizzaria estiver fechada
  if (!isPizzariaAberta()) {
    alert('Estamos fechados!\\n\\nHorario de funcionamento:\\nTerca a Domingo, das 18h as 00h.\\n\\nFavor voltar quando estivermos abertos.');
    return;
  }
"""

if old5 in content:
    content = content.replace(old5, new5, 1)
    print("OK: toggleCart com bloqueio adicionado")
else:
    print("ERRO: nao encontrou toggleCart")

with open('app.html', 'w') as f:
    f.write(content)

print("\nTudo pronto!")
