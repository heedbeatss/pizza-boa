with open('app.html', 'r') as f:
    content = f.read()

old = "var HORA_FIM = 24;    // 00h (meia-noite)"
new = "var HORA_FIM = 25;    // 01h (uma da manhã)"

if old in content:
    content = content.replace(old, new, 1)
    print("OK: Hora fim alterada para 01h")
else:
    print("ERRO: nao encontrou HORA_FIM")

# Atualizar tambem a mensagem de horario
old2 = "if (hora >= HORA_FIM) return 'Ja fechamos. Abrimos amanha as ' + HORA_INICIO + 'h.';"
new2 = "if (hora >= HORA_FIM || hora < HORA_INICIO) return 'Ja fechamos. Abrimos amanha as ' + HORA_INICIO + 'h.';"

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("OK: Mensagem de horario atualizada")
else:
    print("ERRO: nao encontrou mensagem de horario")

# Atualizar o alert de fechado
old3 = "Terca a Domingo, das 18h as 00h."
new3 = "Terca a Domingo, das 18h as 01h."

if old3 in content:
    content = content.replace(old3, new3, 1)
    print("OK: Alert atualizado")
else:
    print("ERRO: nao encontrou alert")

# Atualizar info de horario
old4 = "Terca a Domingo, 18h-00h."
new4 = "Terca a Domingo, 18h-01h."

if old4 in content:
    content = content.replace(old4, new4, 1)
    print("OK: Info de horario atualizada")
else:
    print("ERRO: nao encontrou info de horario")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
