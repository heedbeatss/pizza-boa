with open("app.html", "r") as f:
    lines = f.readlines()

# A linha 761 (index 760) precisa ser corrigida
# JavaScript correto:
# h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\'' + p.id + '\')">';

# Construir a linha corretamente
js_line = "h += '<div class="
js_line += '"pedido-card '
js_line += " + st.class + "
js_line += '" style="cursor:pointer" onclick="verPedidoAdmin('
js_line += "\\'"
js_line += "' + p.id + "
js_line += "'"
js_line += "\\'"
js_line += ")'"
js_line += '">'
js_line += "';"
js_line += "\n"

lines[760] = js_line

with open("app.html", "w") as f:
    f.writelines(lines)

print("Linha 761 corrigida!")
print("Conteudo:", repr(lines[760]))
