with open('app.html', 'r') as f:
    content = f.read()

# 1. Corrigir ID adminPedidosList -> adminPedidos
content = content.replace("document.getElementById('adminPedidos')", "document.getElementById('adminPedidosList')")
print("OK: adminPedidos corrigido para adminPedidosList")

# 2. Adicionar secao de Meus Pedidos no cardapio
# Procurar onde adicionar (depois do cardapio, antes do </div> final)
old_cardapio = '  <div id="cardapio"></div>'
new_cardapio = '''  <div id="cardapio"></div>
  
  <!-- Meus Pedidos -->
  <div style="padding:24px 16px;border-top:1px solid rgba(88,28,135,.2)">
    <h2 style="font-size:18px;font-weight:700;margin-bottom:16px">📋 Meus Pedidos</h2>
    <p style="font-size:13px;color:#a1a1a1;margin-bottom:12px">Digite seu telefone para ver seus pedidos:</p>
    <div style="display:flex;gap:8px;margin-bottom:16px">
      <input type="tel" id="telefonePedidos" placeholder="Ex: 19 99999-9999" style="flex:1;padding:12px;border-radius:12px;background:#1a1a1a;color:#fff;border:1px solid rgba(88,28,135,.2);font-size:14px;outline:none">
      <button onclick="carregarPedidos()" style="padding:12px 20px;border-radius:12px;background:#581c87;color:#fff;border:none;cursor:pointer;font-size:14px;font-weight:600">Buscar</button>
    </div>
    <div id="meusPedidos"></div>
  </div>'''

content = content.replace(old_cardapio, new_cardapio, 1)
print("OK: Secao de Meus Pedidos adicionada")

# 3. Atualizar carregarPedidos para usar telefonePedidos
old_tel = "var telefone = document.getElementById('telefone').value.trim();"
new_tel = "var telefone = document.getElementById('telefonePedidos').value.trim();"
content = content.replace(old_tel, new_tel, 1)
print("OK: Telefone alterado para telefonePedidos")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
