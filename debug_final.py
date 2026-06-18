with open('app.html', 'r') as f:
    content = f.read()

# Encontrar o JS
start = content.find('<script>') + 8
end = content.find('</script>')
js = content[start:end]

# Contar chaves linha a linha
lines = js.split('\n')
balance = 0
for i, line in enumerate(lines):
    o = line.count('{')
    c = line.count('}')
    balance += o - c
    if balance < 0:
        print(f"Linha {i+1}: balance={balance}, linha: {line[:80]}")
        break
    # Mostrar linhas com muitas chaves
    if o > 3:
        print(f"Linha {i+1}: +{o} chaves, balance={balance}: {line[:60]}")

print(f"\nBalance final: {balance}")

# Procurar por chaves extras em strings
# O problema comum e ter { dentro de strings como 'itemModal'
import re
# Procurar padrao '\\'' seguido de {
matches = re.findall(r"\\'[^']*\\{[^']*\\'", js)
for m in matches[:5]:
    print(f"Possivel problema: {m}")
