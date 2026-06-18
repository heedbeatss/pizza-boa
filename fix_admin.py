with open("app.html", "r") as f:
    content = f.read()

# Substituir a função carregarAdminPedidos para ter mais informações de debug
old_func = """function carregarAdminPedidos() {
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
  var el = document.getElementById('adminPedidosList');
  if (!el) return;
  if (pedidos.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido recebido</div>'; document.getElementById('adminPedidoDetalhe').innerHTML = ''; return; }
  var h = '';
  var temPedido = false;
  for (var i = pedidos.length - 1; i >= 0; i--) {
    var p = pedidos[i]; var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido;
    temPedido = true;
    h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer;margin-bottom:12px" onclick="verPedidoAdmin(\\'' + p.id + '\\')">';
    h += '<div style="display:flex;justify-content:space-between"><strong>' + p.id + '</strong><span class="status-badge ' + st.class + '">' + st.icon + ' ' + st.nome + '</span></div>';
    h += '<div style="font-size:12px;color:#a1a1a1;margin-top:4px">👤 ' + p.nome + ' - 📱 ' + p.telefone + '</div>';
    h += '<div style="font-size:12px;color:#a1a1a1">📍 ' + p.endereco.rua + ', ' + p.endereco.numero + ' - ' + p.endereco.bairro + '</div>';
    h += '<div style="font-size:12px;color:#a1a1a1;margin-top:4px">';
    for (var j = 0; j < p.itens.length; j++) { h += '• ' + p.itens[j].qty + 'x ' + p.itens[j].nome + ' (' + p.itens[j].tamanho + ')<br>'; }
    h += '</div>';
    h += '<div style="display:flex;justify-content:space-between;border-top:1px solid rgba(88,28,135,.2);padding-top:8px;margin-top:8px">';
    h += '<span style="color:#a1a1a1;font-size:12px">💳 ' + (p.pagamento === 'dinheiro' ? 'Dinheiro' : p.pagamento) + (p.troco ? ' (Troco: R$ ' + p.troco + ')' : '') + '</span>';
    h += '<strong style="color:#a855f7">R$ ' + p.totalFinal.toFixed(2) + '</strong></div>';
    h += '</div>';
  }
  if (!temPedido) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido em andamento</div>'; }
  else { el.innerHTML = h; }
}"""

new_func = """function carregarAdminPedidos() {
  var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
  var el = document.getElementById('adminPedidosList');
  if (!el) return;
  console.log('[ADMIN] Total pedidos:', pedidos.length);
  if (pedidos.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido recebido</div>'; document.getElementById('adminPedidoDetalhe').innerHTML = ''; return; }
  var h = '';
  var temPedido = false;
  for (var i = pedidos.length - 1; i >= 0; i--) {
    var p = pedidos[i];
    if (!p || !p.id) continue;
    var st = STATUS_PEDIDO[p.status] || STATUS_PEDIDO.recebido;
    temPedido = true;
    var endereco = p.endereco || {};
    h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer;margin-bottom:12px" onclick="verPedidoAdmin(\\'' + p.id + '\\')">';
    h += '<div style="display:flex;justify-content:space-between"><strong>' + p.id + '</strong><span class="status-badge ' + st.class + '">' + st.icon + ' ' + st.nome + '</span></div>';
    h += '<div style="font-size:12px;color:#a1a1a1;margin-top:4px">👤 ' + (p.nome||'') + ' - 📱 ' + (p.telefone||'') + '</div>';
    h += '<div style="font-size:12px;color:#a1a1a1">📍 ' + (endereco.rua||'') + ', ' + (endereco.numero||'') + ' - ' + (endereco.bairro||'') + '</div>';
    h += '<div style="font-size:12px;color:#a1a1a1;margin-top:4px">';
    if (p.itens) { for (var j = 0; j < p.itens.length; j++) { h += '• ' + p.itens[j].qty + 'x ' + p.itens[j].nome + ' (' + p.itens[j].tamanho + ')<br>'; } }
    h += '</div>';
    h += '<div style="display:flex;justify-content:space-between;border-top:1px solid rgba(88,28,135,.2);padding-top:8px;margin-top:8px">';
    h += '<span style="color:#a1a1a1;font-size:12px">💳 ' + (p.pagamento === 'dinheiro' ? 'Dinheiro' : (p.pagamento||'')) + (p.troco ? ' (Troco: R$ ' + p.troco + ')' : '') + '</span>';
    h += '<strong style="color:#a855f7">R$ ' + (p.totalFinal||0).toFixed(2) + '</strong></div>';
    h += '</div>';
  }
  console.log('[ADMIN] Pedidos renderizados:', temPedido);
  if (!temPedido) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido em andamento</div>'; }
  else { el.innerHTML = h; }
}"""

content = content.replace(old_func, new_func)

with open("app.html", "w") as f:
    f.write(content)

print("Função carregarAdminPedidos atualizada!")
