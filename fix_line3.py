with open("app.html", "r") as f:
    lines = f.readlines()

# A linha JS correta que queremos:
# h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\'' + p.id + '\')">';

# Vamos construir caractere por caractere
result = []
result.append("h += '<div class=")
result.append('"pedido-card ')
result.append(" + st.class + ")
result.append('" style="cursor:pointer" onclick="verPedidoAdmin(')
result.append("\\'")  # aspa simples escapada em JS
result.append("' + p.id + ")
result.append("\\'")  # aspa simples escapada em JS  
result.append(")'")
result.append('">')
result.append("';")
result.append("\n")

linha = "".join(result)
print("Linha:", repr(linha))

# Verificar
if "verPedidoAdmin(\\'' + p.id + \\')" in linha:
    print("OK!")
else:
    print("Verificar manualmente")

lines[760] = linha

with open("app.html", "w") as f:
    f.writelines(lines)

print("Feito!")
