with open('app.html', 'r') as f:
    content = f.read()

# Corrigir a linha 761 - verPedidoAdmin com aspas erradas
old = 'h += \'<div class="pedido-card \' + st.class + \'" style="cursor:pointer" onclick="verPedidoAdmin(\\\\\\\'\' + p.id + \\\\\\\'\\\'">\';'
new = "h += '<div class=\"pedido-card ' + st.class + '\" style=\"cursor:pointer\" onclick=\"verPedidoAdmin(\\'' + p.id + '\\')\">';"

# Tentar encontrar e substituir
import re
# Procurar a linha com verPedidoAdmin e corrigir
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'verPedidoAdmin' in line and 'carregarAdminPedidos' in line:
        print(f"Linha {i+1}: {line[:100]}")
        # Corrigir
        lines[i] = line.replace('verPedidoAdmin(\\\\\\'\\'', "verPedidoAdmin('\\''")
        print(f"Corrigida: {lines[i][:100]}")

content = '\n'.join(lines)
with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
