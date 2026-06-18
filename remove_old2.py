with open('app.html', 'r') as f:
    content = f.read()

# Encontrar o ponto exato
start_marker = "  });"
end_marker = "function renderCheckoutSummary() {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx >= 0 and end_idx >= 0:
    print(f"Encontrado: start={start_idx}, end={end_idx}")
    print(f"Trecho a remover:\n{content[start_idx:end_idx]}")
    
    # Substituir tudo entre start e end por uma linha em branco
    content = content[:start_idx] + "  });\n\n" + content[end_idx:]
    
    with open('app.html', 'w') as f:
        f.write(content)
    print("\nOK: codigo antigo removido!")
else:
    print(f"ERRO: start={start_idx}, end={end_idx}")
