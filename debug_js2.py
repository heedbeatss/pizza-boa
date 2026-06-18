with open('app.html', 'r') as f:
    content = f.read()

start = content.find('<script>')
end = content.rfind('</script>')
js = content[start+8:end]

# Contar linha a linha e mostrar onde passa de 2 extras
lines = js.split('\n')
balance = 0
for i, line in enumerate(lines):
    o = line.count('{')
    c = line.count('}')
    balance += o - c
    # Mostrar linhas que adicionam muitas chaves
    if o > 2:
        print(f"Linha {i+1} (+{o} chaves, balance={balance}): {line[:80]}")

print(f"\nBalance final: {balance}")

# Procurar por chaves soltas ou duplicadas
print("\n=== Procurando chaves duplicadas ===")
for i, line in enumerate(lines):
    if '{{' in line or '}}' in line:
        print(f"Linha {i+1}: {line[:100]}")
