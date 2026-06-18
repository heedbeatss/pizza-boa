with open('app.html', 'r') as f:
    content = f.read()

# 1. Corrigir salvarPedido para salvar o telefone do campo correto
old_save = """function salvarPedido(pedidoId, nome, telefone) {
  try {
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var total = 0;
    for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
    pedidos.push({ id: pedidoId, nome: nome, telefone: telefone, itens: cart.slice(), total: total, entrega: zonaAtual ? zonaAtual.valor : 0, status: 'recebido', data: new Date().toISOString() });
    localStorage.setItem('pizzaPedidos', JSON.stringify(pedidos));
  } catch(e) {}
}"""

new_save = """function salvarPedido(pedidoId, nome, telefone) {
  try {
    // Pega o telefone do campo se nao foi passado
    if (!telefone) telefone = document.getElementById('telefone').value.trim();
    
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var total = 0;
    for (var i = 0; i < cart.length; i++) total += cart[i].preco * cart[i].qty;
    
    var pedido = { 
      id: pedidoId, 
      nome: nome, 
      telefone: telefone, 
      itens: cart.slice(), 
      total: total, 
      entrega: zonaAtual ? zonaAtual.valor : 0, 
      status: 'recebido', 
      data: new Date().toISOString() 
    };
    pedidos.push(pedido);
    localStorage.setItem('pizzaPedidos', JSON.stringify(pedidos));
    
    // Salva o telefone para busca posterior
    localStorage.setItem('ultimoTelefone', telefone);
    
    console.log('[PEDIDO] Salvo:', pedidoId, 'Tel:', telefone, 'Total:', pedidos.length);
  } catch(e) { console.error('[ERRO] salvarPedido:', e); }
}"""

if old_save in content:
    content = content.replace(old_save, new_save, 1)
    print("OK: salvarPedido corrigido")
else:
    print("ERRO: salvarPedido")

# 2. Corrigir carregarPedidos para usar ultimoTelefone e tambem o campo telefone
old_carregar = """function carregarPedidos() {
  try {
    var telefone = document.getElementById('telefonePedidos').value.trim();
    // Se campo vazio, tenta usar o ultimo telefone usado
    if (!telefone) telefone = localStorage.getItem('ultimoTelefone') || '';
    if (!telefone) return;
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var meus = pedidos.filter(function(p) { return p.telefone === telefone; });
    var el = document.getElementById('meusPedidos');
    if (!el) return;
    if (meus.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido encontrado</div>'; return; }"""

new_carregar = """function carregarPedidos() {
  try {
    // Tenta varios campos de telefone
    var telefone = document.getElementById('telefonePedidos') ? document.getElementById('telefonePedidos').value.trim() : '';
    if (!telefone) telefone = document.getElementById('telefone') ? document.getElementById('telefone').value.trim() : '';
    if (!telefone) telefone = localStorage.getItem('ultimoTelefone') || '';
    if (!telefone) { 
      var el = document.getElementById('meusPedidos');
      if (el) el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Digite seu telefone acima para ver seus pedidos</div>';
      return; 
    }
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var meus = pedidos.filter(function(p) { return p.telefone === telefone; });
    var el = document.getElementById('meusPedidos');
    if (!el) return;
    if (meus.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido encontrado para este telefone</div>'; return; }"""

if old_carregar in content:
    content = content.replace(old_carregar, new_carregar, 1)
    print("OK: carregarPedidos corrigido")
else:
    print("ERRO: carregarPedidos")

# 3. Corrigir carregarAdminPedidos para garantir que funciona
old_admin = """function carregarAdminPedidos() {
  try {
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var el = document.getElementById('adminPedidosList');
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
}"""

new_admin = """function carregarAdminPedidos() {
  try {
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var el = document.getElementById('adminPedidosList');
    if (!el) { console.error('[ADMIN] Elemento adminPedidosList nao encontrado'); return; }
    if (pedidos.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido recebido</div>'; return; }
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
    console.log('[ADMIN] ' + pedidos.length + ' pedidos carregados');
  } catch(e) { console.error('[ERRO] carregarAdminPedidos:', e); }
}"""

if old_admin in content:
    content = content.replace(old_admin, new_admin, 1)
    print("OK: carregarAdminPedidos corrigido")
else:
    print("ERRO: carregarAdminPedidos")

# 4. Adicionar chamada de carregarPedidos no showHome
old_showhome = """  // Voltar ao topo
  window.scrollTo({ top: 0, behavior: 'smooth' });
}"""

new_showhome = """  // Voltar ao topo
  window.scrollTo({ top: 0, behavior: 'smooth' });
  
  // Recarregar pedidos
  setTimeout(function() { carregarPedidos(); }, 500);
}"""

if old_showhome in content:
    content = content.replace(old_showhome, new_showhome, 1)
    print("OK: showHome atualizado")
else:
    print("ERRO: showHome")

# 5. Corrigir o botao Finalizar Pedido para nao conflitar
# O problema e que o botao esta dentro do modal do carrinho
# Vamos garantir que o goCheckout fecha o modal primeiro
old_gocheckout = """function goCheckout() {
  document.getElementById('cartModal').style.display = 'none';
  document.getElementById('checkoutPage').style.display = 'block';"""

new_gocheckout = """function goCheckout() {
  // Fecha o modal do carrinho
  var cartModal = document.getElementById('cartModal');
  if (cartModal) cartModal.style.display = 'none';
  
  // Esconde o botao flutuante do carrinho
  var cartBtn = document.getElementById('cartBtn');
  if (cartBtn) cartBtn.style.display = 'none';
  
  document.getElementById('checkoutPage').style.display = 'block';"""

if old_gocheckout in content:
    content = content.replace(old_gocheckout, new_gocheckout, 1)
    print("OK: goCheckout corrigido")
else:
    print("ERRO: goCheckout")

with open('app.html', 'w') as f:
    f.write(content)

print("\nTodas as correcoes aplicadas!")
