with open("app.html", "r") as f:
    content = f.read()

# Substituir a linha problemática
old = '''h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer;margin-bottom:12px" onclick="verPedidoAdmin(\\\\'' + p.id + '\\\\')">';'''
new = '''h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer;margin-bottom:12px" onclick="verPedidoAdmin(\\'' + p.id + '\\')">';'''

content = content.replace(old, new)

with open("app.html", "w") as f:
    f.write(content)

print("Corrigido!")
