with open('app.html', 'r') as f:
    content = f.read()

old = """  if (s) nome = '\u00bd ' + currentItem.nome + ' / \u00bd ' + s.nome;
  }
  
  cart.push({ nome: nome, tamanho: selTamanho.nome, preco: calcPrice() / selQty, qty: selQty });"""

new = """  if (s) nome = '\u00bd ' + currentItem.nome + ' / \u00bd ' + s.nome;
  }
  if (selBorda) nome += ' (borda catupiry)';
  
  cart.push({ nome: nome, tamanho: selTamanho.nome, preco: calcPrice() / selQty, qty: selQty });"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: addToCart atualizado com borda")
else:
    print("ERRO: nao encontrou o ponto exato")
    # Tentar alternativa
    import re
    match = re.search(r"if \(s\) nome = '.*?';.*?cart\.push", content, re.DOTALL)
    if match:
        print(f"Encontrado via regex: {match.group()[:80]}...")
    else:
        print("Regex tambem nao encontrou")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
