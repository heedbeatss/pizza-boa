with open('app.html', 'r') as f:
    content = f.read()

start = content.find('<script>') + 8
end = content.find('</script>')
js = content[start:end]

import re
# Remover strings
js_clean = re.sub(r'\"[^\"]*\"', '""', js)
js_clean = re.sub(r"'[^']*'", "''", js_clean)

# Contar chaves linha a linha
lines = js_clean.split('\n')
balance = 0
for i, line in enumerate(lines):
    o = line.count('{')
    c = line.count('}')
    balance += o - c
    # Mostrar linhas que adicionam muitas chaves
    if o > 2:
        print(f"Linha {i+1}: +{o} chaves, balance={balance}")

print(f"\nBalance final: {balance}")

# Mostrar fim do arquivo
print("\nUltimas 10 linhas do JS original:")
js_lines = js.split('\n')
for i in range(max(0, len(js_lines)-10), len(js_lines)):
    print(f"{i+1}: {js_lines[i]}")
