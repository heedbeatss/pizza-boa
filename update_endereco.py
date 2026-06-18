with open('app.html', 'r') as f:
    content = f.read()

old = 'var PIZZARIA_ENDERECO = "Rua Exemplo, 123 - Centro, Campinas - SP";'
new = 'var PIZZARIA_ENDERECO = "Rua Luiz Razera, 300 - Jd. Elite, Piracicaba - SP";'

if old in content:
    content = content.replace(old, new, 1)
    print("OK: Endereco da pizzaria atualizado!")
else:
    print("ERRO: nao encontrou a linha do endereco")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
