with open('app.html', 'r') as f:
    content = f.read()

# Adicionar data-id nos botoes de sabor da 2a metade
old = "h += '<button class=\"sabor-btn\" onclick=\"selectSegundo(\\'' + s.id + '\\')\">' + s.nome + ' <span>R$ ' + pm.toFixed(2) + '</span></button>';"
new = "h += '<button class=\"sabor-btn\" data-id=\"' + s.id + '\" onclick=\"selectSegundo(\\'' + s.id + '\\')\">' + s.nome + ' <span>R$ ' + pm.toFixed(2) + '</span></button>';"

if old in content:
    content = content.replace(old, new, 1)
    print("OK: data-id adicionado nos botoes de sabor")
else:
    print("ERRO: nao encontrou o botao de sabor")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
