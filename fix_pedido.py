with open('app.html', 'r') as f:
    content = f.read()

# 1. Corrigir submitOrder - limpar carrinho e mostrar tela de sucesso
old_submit = """  salvarPedido(pedidoId, nome, telefone);
  document.getElementById('checkoutForm').style.display = 'none';
  document.getElementById('checkoutSuccess').style.display = 'block';
  document.getElementById('pedidoNum').textContent = pedidoId;
  document.getElementById('waLink').href = 'https://wa.me/5519984356289?text=' + encodeURIComponent(msg);
}"""

new_submit = """  salvarPedido(pedidoId, nome, telefone);
  
  // Salva o numero do pedido e telefone para exibicao
  localStorage.setItem('ultimoPedido', pedidoId);
  localStorage.setItem('ultimoTelefone', telefone);
  
  // Limpa o carrinho
  cart = [];
  localStorage.removeItem('pizzaCart');
  updateCartButton();
  
  // Mostra tela de sucesso
  document.getElementById('checkoutForm').style.display = 'none';
  document.getElementById('checkoutSuccess').style.display = 'block';
  document.getElementById('pedidoNum').textContent = pedidoId;
  document.getElementById('waLink').href = 'https://wa.me/5519984356289?text=' + encodeURIComponent(msg);
}"""

if old_submit in content:
    content = content.replace(old_submit, new_submit, 1)
    print("OK: submitOrder corrigido")
else:
    print("ERRO: submitOrder")

# 2. Corrigir goBack - limpar carrinho e resetar tudo
old_goBack = """function goBack() {
  document.getElementById('checkoutPage').style.display = 'none';
  document.getElementById('adminPage').style.display = 'none';
  document.getElementById('cardapio').style.display = 'block';
  document.getElementById('catNavMenu').style.display = 'flex';
}"""

new_goBack = """function goBack() {
  document.getElementById('checkoutPage').style.display = 'none';
  document.getElementById('adminPage').style.display = 'none';
  document.getElementById('cardapio').style.display = 'block';
  document.getElementById('catNavMenu').style.display = 'flex';
  
  // Resetar formulario de checkout
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
  document.getElementById('checkoutForm').style.display = 'block';
  document.getElementById('checkoutSuccess').style.display = 'none';
  document.getElementById('checkoutError').style.display = 'none';
  zonaAtual = null;
  
  // Limpar carrinho se ainda tiver itens
  if (cart.length > 0) {
    cart = [];
    localStorage.removeItem('pizzaCart');
    updateCartButton();
  }
  
  // Recarregar pedidos
  carregarPedidos();
  
  window.scrollTo(0, 0);
}"""

if old_goBack in content:
    content = content.replace(old_goBack, new_goBack, 1)
    print("OK: goBack corrigido")
else:
    print("ERRO: goBack")

# 3. Corrigir carregarPedidos - usar ultimo telefone se campo estiver vazio
old_carregar = """function carregarPedidos() {
  try {
    var telefone = document.getElementById('telefone').value.trim();
    if (!telefone) return;
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var meus = pedidos.filter(function(p) { return p.telefone === telefone; });
    var el = document.getElementById('meusPedidos');
    if (!el) return;
    if (meus.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido encontrado</div>'; return; }"""

new_carregar = """function carregarPedidos() {
  try {
    var telefone = document.getElementById('telefone').value.trim();
    // Se campo vazio, tenta usar o ultimo telefone usado
    if (!telefone) telefone = localStorage.getItem('ultimoTelefone') || '';
    if (!telefone) return;
    var pedidos = JSON.parse(localStorage.getItem('pizzaPedidos') || '[]');
    var meus = pedidos.filter(function(p) { return p.telefone === telefone; });
    var el = document.getElementById('meusPedidos');
    if (!el) return;
    if (meus.length === 0) { el.innerHTML = '<div style="text-align:center;color:#a1a1a1;padding:20px">Nenhum pedido encontrado</div>'; return; }"""

if old_carregar in content:
    content = content.replace(old_carregar, new_carregar, 1)
    print("OK: carregarPedidos corrigido")
else:
    print("ERRO: carregarPedidos")

# 4. Corrigir carregarAdminPedidos - adicionar chamada automatica
old_admin = """function showAdminLogin() {
  var senha = prompt('Senha admin:');
  if (senha === '1234') {
    document.getElementById('adminPage').style.display = 'block';
    document.getElementById('cardapio').style.display = 'none';
    document.getElementById('catNavMenu').style.display = 'none';
    carregarAdminPedidos();
  }
}"""

new_admin = """function showAdminLogin() {
  var senha = prompt('Senha admin:');
  if (senha === '1234') {
    document.getElementById('adminPage').style.display = 'block';
    document.getElementById('cardapio').style.display = 'none';
    document.getElementById('catNavMenu').style.display = 'none';
    document.getElementById('checkoutPage').style.display = 'none';
    carregarAdminPedidos();
  }
}"""

if old_admin in content:
    content = content.replace(old_admin, new_admin, 1)
    print("OK: showAdminLogin corrigido")
else:
    print("ERRO: showAdminLogin")

# 5. Adicionar botao "Voltar ao Cardapio" na tela de sucesso do pedido
old_success = """    <div id="checkoutSuccess" class="success-screen" style="display:none">
      <div class="emoji">✅</div>
      <h2>Pedido Confirmado!</h2>
      <p>Seu pedido <strong id="pedidoNum"></strong> foi registrado.</p>
      <p style="margin-top:16px">Envie o pedido pelo WhatsApp:</p>
      <a id="waLink" href="#" target="_blank" class="whatsapp-btn">📱 Enviar pelo WhatsApp</a>
    </div>"""

new_success = """    <div id="checkoutSuccess" class="success-screen" style="display:none">
      <div class="emoji">✅</div>
      <h2>Pedido Confirmado!</h2>
      <p>Seu pedido <strong id="pedidoNum"></strong> foi registrado.</p>
      <p style="margin-top:16px">Envie o pedido pelo WhatsApp:</p>
      <a id="waLink" href="#" target="_blank" class="whatsapp-btn">📱 Enviar pelo WhatsApp</a>
      <br><br>
      <button onclick="goBack()" class="back-btn">← Voltar ao Cardápio</button>
    </div>"""

if old_success in content:
    content = content.replace(old_success, new_success, 1)
    print("OK: botao voltar adicionado na tela de sucesso")
else:
    print("ERRO: checkoutSuccess")

# 6. Adicionar seção de "Meus Pedidos" no cardapio principal
old_cardapio_end = """</div>

<script>"""

new_cardapio_end = """</div>

<!-- Meus Pedidos -->
<div style="padding:24px 16px;border-top:1px solid rgba(88,28,135,.2)">
  <h2 style="font-size:18px;font-weight:700;margin-bottom:16px">📋 Meus Pedidos</h2>
  <p style="font-size:13px;color:#a1a1a1;margin-bottom:12px">Digite seu telefone para ver seus pedidos:</p>
  <div style="display:flex;gap:8px;margin-bottom:16px">
    <input type="tel" id="telefonePedidos" placeholder="Ex: 19 99999-9999" style="flex:1;padding:12px;border-radius:12px;background:#1a1a1a;color:#fff;border:1px solid rgba(88,28,135,.2);font-size:14px;outline:none">
    <button onclick="carregarPedidos()" style="padding:12px 20px;border-radius:12px;background:#581c87;color:#fff;border:none;cursor:pointer;font-size:14px;font-weight:600">Buscar</button>
  </div>
  <div id="meusPedidos"></div>
</div>

<script>"""

if old_cardapio_end in content:
    content = content.replace(old_cardapio_end, new_cardapio_end, 1)
    print("OK: secao de Meus Pedidos adicionada")
else:
    print("ERRO: cardapio end")

with open('app.html', 'w') as f:
    f.write(content)

print("\nTodas as correcoes aplicadas!")
