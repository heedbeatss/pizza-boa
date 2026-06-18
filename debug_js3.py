with open('app.html', 'r') as f:
    content = f.read()

# Encontrar todas as chaves que nao fazem parte de objetos literais
# O problema provavelmente esta em uma string que contem { mas nao e objeto

start = content.find('<script>')
end = content.rfind('</script>')
js = content[start+8:end]

# Contar caracteres { e } que estao dentro de strings vs fora
# Uma abordagem: verificar se tem algum { ou } solto

lines = js.split('\n')
for i, line in enumerate(lines):
    # Ignorar linhas que claramente sao objetos (tem id:, nome:, etc)
    stripped = line.strip()
    if stripped.count('{') > 0 and stripped.count('}') > 0:
        # Verificar se e uma linha de objeto normal
        if 'id:' not in stripped and 'nome:' not in stripped and 'function' not in stripped and 'if' not in stripped and 'for' not in stripped:
            print(f"Linha {i+1}: {stripped[:100]}")

# Tentativa: remover chaves duplicadas em linhas especificas
print("\n=== Tentando corrigir ===")

# O erro comum e ter {{ ou }} em algum lugar
if '{{' in js or '}}' in js:
    print("Encontrado {{ ou }} - corrigindo...")
    js = js.replace('{{', '{').replace('}}', '}')
    content = content[:start+8] + js + content[end:]
    with open('app.html', 'w') as f:
        f.write(content)
    print("Corrigido!")
else:
    print("Nao encontrou {{ ou }}")
    
    # Verificar linhas com numero impar de chaves
    for i, line in enumerate(lines):
        o = line.count('{')
        c = line.count('}')
        if (o + c) % 2 != 0 and o + c > 0:
            print(f"Linha {i+1} ({o} abertas, {c} fechadas): {stripped[:80]}")
