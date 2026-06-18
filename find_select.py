with open('app.html', 'r') as f:
    lines = f.readlines()

# Encontrar a linha que comeca com "function selectTamanho"
start = None
end = None
for i, line in enumerate(lines):
    if 'function selectTamanho(idx)' in line:
        start = i
    if start is not None and line.strip() == '}' and i > start:
        end = i
        break

if start is not None and end is not None:
    print(f"Encontrado: linhas {start+1} a {end+1}")
    print("Conteudo atual:")
    for i in range(start, end+1):
        print(f"  {i+1}: {lines[i].rstrip()}")
else:
    print(f"ERRO: start={start}, end={end}")
