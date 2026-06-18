with open('app.html', 'r') as f:
    content = f.read()

# Extrair JavaScript
start = content.find('<script>')
end = content.rfind('</script>')
js = content[start+8:end]

# Encontrar onde o balanceamento quebra
lines = js.split('\n')
balance = 0
for i, line in enumerate(lines):
    o = line.count('{')
    c = line.count('}')
    balance += o - c
    if balance < 0:
        print(f"Linha {i+1}: balance negativo ({balance})")
        print(f"  Conteudo: {line[:100]}")
        break

# Mostrar ultimas linhas
print("\nUltimas 20 linhas do JS:")
for i, line in enumerate(lines[-20:]):
    print(f"{len(lines)-20+i+1}: {line}")
