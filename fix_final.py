#!/usr/bin/env python3
# Script para corrigir a linha 761 do app.html

# A linha JavaScript correta que queremos:
# h += '<div class="pedido-card ' + st.class + '" style="cursor:pointer" onclick="verPedidoAdmin(\'' + p.id + '\')">';

# Vamos escrever a linha byte por byte para evitar confusão com escapes

linha_bytes = b"h += '<div class=\"pedido-card ' + st.class + '\" style=\"cursor:pointer\" onclick=\"verPedidoAdmin(\\'\\'' + p.id + '\\'\\')\"'; \n"

linha_str = linha_bytes.decode('utf-8')
print("Linha a escrever:", repr(linha_str))

# Ler o arquivo
with open("app.html", "r") as f:
    lines = f.readlines()

# Substituir a linha 761 (índice 760)
lines[760] = linha_str

# Escrever de volta
with open("app.html", "w") as f:
    f.writelines(lines)

print("Feito! Linha 761 corrigida.")

# Verificar
with open("app.html", "r") as f:
    lines = f.readlines()
print("Conteúdo:", repr(lines[760]))
