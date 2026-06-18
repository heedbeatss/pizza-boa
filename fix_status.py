with open("app.html", "r") as f:
    content = f.read()

# 1. Substituir carregarPedidos para mostrar TODOS os pedidos em andamento
old_carregar = """function carregarPedidos() {
  var telefone = localStorage.getItem('ultimoTelefone') || '';
  if (!telefone) return;
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
  // Mostra apenas pedidos em andamento (não entregues, não cancelados)
  var meus = pedidos.filter(function(p) { return p.telefone === telefone && p.status !== 'entregue' && p.status !== 'cancelado'; });
  var el = document.getElementById('meusPedidos');
  var section = document.getElementById('meusPedidosSection');
  if (!el || !section) return;
  if (meus.length === 0) { section.style.display = 'none'; el.innerHTML = ''; return; }
  section.style.display = 'block';
  var h = '';
  for (var i = meus.length - 1; i >= 0; i--) {
    var p = meus[i]; var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido;
    h += '<div class="pedido-card ' + st.class + '" style="margin-bottom:12px">';
    h += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><strong style="font-size:16px">' + p.id + '</strong><span class="status-badge ' + st.class + '">' + st.icon + ' ' + st.nome + '</span></div>';
    h += '<div style="font-size:12px;color:#a1a1a1;margin-bottom:8px">' + new Date(p.data).toLocaleString('pt-BR') + '</div>';
    h += '<div style="font-size:13px;margin-bottom:4px">';
    for (var j = 0; j < p.itens.length; j++) { h += '• ' + p.itens[j].qty + 'x ' + p.itens[j].nome + ' (' + p.itens[j].tamanho + ')<br>'; }
    h += '</div>';
    h += '<div style="display:flex;justify-content:space-between;border-top:1px solid rgba(88,28,135,.2);padding-top:8px"><span style="color:#a1a1a1;font-size:12px">Entrega: ' + (p.entrega === 0 ? 'GRATIS' : 'R$ ' + p.entrega.toFixed(2)) + '</span><strong style="color:#a855f7">R$ ' + p.totalFinal.toFixed(2) + '</strong></div>';
    h += '</div>';
  }
  el.innerHTML = h;
}"""

new_carregar = """function carregarPedidos() {
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
  // Mostra TODOS os pedidos em andamento (não entregues, não cancelados)
  var emAndamento = pedidos.filter(function(p) { return p && p.status && p.status !== 'entregue' && p.status !== 'cancelado'; });
  var el = document.getElementById('meusPedidos');
  var section = document.getElementById('meusPedidosSection');
  if (!el || !section) return;
  if (emAndamento.length === 0) { section.style.display = 'none'; el.innerHTML = ''; return; }
  section.style.display = 'block';
  var h = '';
  for (var i = emAndamento.length - 1; i >= 0; i--) {
    var p = emAndamento[i]; var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido;
    h += '<div class="pedido-card ' + st.class + '" style="margin-bottom:12px">';
    h += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><strong style="font-size:16px">' + p.id + '</strong><span class="status-badge ' + st.class + '">' + st.icon + ' ' + st.nome + '</span></div>';
    h += '<div style="font-size:12px;color:#a1a1a1;margin-bottom:8px">' + new Date(p.data).toLocaleString('pt-BR') + '</div>';
    h += '<div style="font-size:13px;margin-bottom:4px">';
    if (p.itens) { for (var j = 0; j < p.itens.length; j++) { h += '• ' + p.itens[j].qty + 'x ' + p.itens[j].nome + ' (' + p.itens[j].tamanho + ')<br>'; } }
    h += '</div>';
    h += '<div style="display:flex;justify-content:space-between;border-top:1px solid rgba(88,28,135,.2);padding-top:8px"><span style="color:#a1a1a1;font-size:12px">Entrega: ' + (p.entrega === 0 ? 'GRATIS' : 'R$ ' + p.entrega.toFixed(2)) + '</span><strong style="color:#a855f7">R$ ' + (p.totalFinal||0).toFixed(2) + '</strong></div>';
    h += '</div>';
  }
  el.innerHTML = h;
}"""

content = content.replace(old_carregar, new_carregar)

# 2. Substituir alterarStatus para também carregar pedidos do usuario
old_alterar = "function alterarStatus(id, status) { var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]'); var p = pedidos.find(function(x) { return x.id === id; }); if (p) { p.status = status; localStorage.setItem('pizzaPedidos', JSON.stringify(pedidos)); carregarAdminPedidos(); verPedidoAdmin(id); } }"
new_alterar = "function alterarStatus(id, status) { var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]'); var p = pedidos.find(function(x) { return x.id === id; }); if (p) { p.status = status; localStorage.setItem('pizzaPedidos', JSON.stringify(pedidos)); carregarAdminPedidos(); verPedidoAdmin(id); carregarPedidos(); } }"

content = content.replace(old_alterar, new_alterar)

# 3. Adicionar setInterval para atualizar pedidos do usuario a cada 5 segundos
old_init = "setInterval(carregarPedidos, 10000);"
new_init = "setInterval(carregarPedidos, 5000);"

content = content.replace(old_init, new_init)

with open("app.html", "w") as f:
    f.write(content)

print("Correções aplicadas!")
