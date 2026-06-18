# JavaScript puro que queremos:
# h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\'' + p.id + '\')">';

# Em Python, para gerar essa linha:
# Precisamos que o resultado final seja uma string JS válida

with open("app.html", "r") as f:
    lines = f.readlines()

# A linha JS correta como string Python:
# h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(' + "'" + p.id + "'" + ')">'
# Mas dentro de uma string JS, então precisamos escapar

# O conteúdo JS final deve ser:
# h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\'' + p.id + '\')">';

# Em Python, para escrever isso em um arquivo:
# Usamos aspas simples para a string Python, e escapamos as aspas simples internas com \

linha_js = "h += '<div class=\"pedido-card ' + st.class + '\" style=\"cursor:pointer\" onclick=\"verPedidoAdmin(\\'\\'' + p.id + '\\'\\')\"'; \n"
# Hmm, isso não está certo. Deixa eu pensar de outra forma.

# O arquivo JS terá esta linha:
# h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\'' + p.id + '\')">';

# Então em Python, a string é:
linha_python = 'h += \'<div class="pedido-card \' + st.class + \'" style="cursor:pointer" onclick="verPedidoAdmin(\\\'\\\'\' + p.id + \'\\\'\\\')">\'' + '\n'

# Testar
print("Linha Python:", repr(linha_python))

# Verificar se o JS gerado seria correto
js_gerado = linha_python.strip()
print("JS gerado:", js_gerado)

# Verificar: deveria conter verPedidoAdmin(\''
if "verPedidoAdmin(\\''" in js_gerado or "verPedidoAdmin(''"  in js_gerado:
    print("OK - verPedidoAdmin com aspas corretas")
else:
    print("ERRO - verPedidoAdmin com aspas erradas")

lines[760] = linha_python

with open("app.html", "w") as f:
    f.writelines(lines)

print("Feito!")
