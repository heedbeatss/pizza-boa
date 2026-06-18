with open('app.html', 'r') as f:
    content = f.read()

# Substituir a parte que monta as opcoes de 2a metade dentro de setMetade
old = """    // Pizzas salgadas
    var salgadas = CARDAPIO.categorias[0].itens.filter(function(i) { return i.id !== currentItem.id; });
    if (salgadas.length > 0) {
      h += '<div class="cat-label">🍕 Pizzas Salgadas</div><div class="sabor-grid">';
      for (var i = 0; i < salgadas.length; i++) {
        var s = salgadas[i];
        var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
        var pm = Math.max(selTamanho.preco, sp.preco);
        h += '<button class="sabor-btn" onclick="selectSegundo(\\'' + s.id + '\\')">' + s.nome + ' <span>R$ ' + pm.toFixed(2) + '</span></button>';
      }
      h += '</div>';
    }
    
    // Pizzas doces
    var doces = CARDAPIO.categorias[1].itens;
    if (doces.length > 0) {
      h += '<div class="cat-label">🍫 Pizzas Doces</div><div class="sabor-grid">';
      for (var i = 0; i < doces.length; i++) {
        var s = doces[i];
        var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
        var pm = Math.max(selTamanho.preco, sp.preco);
        h += '<button class="sabor-btn" onclick="selectSegundo(\\'' + s.id + '\\')">' + s.nome + ' <span>R$ ' + pm.toFixed(2) + '</span></button>';
      }
      h += '</div>';
    }"""

new = """    // Percorre todas as categorias de pizza dinamicamente
    for (var c = 0; c < CARDAPIO.categorias.length; c++) {
      var cat = CARDAPIO.categorias[c];
      // So mostra categorias que sejam pizza (salgadas, especiais, doces)
      if (cat.id.indexOf('pizza') < 0) continue;
      
      var itens = cat.itens.filter(function(i) { return i.id !== currentItem.id; });
      if (itens.length === 0) continue;
      
      var icone = cat.id.indexOf('doce') >= 0 ? '🍫' : (cat.id.indexOf('especial') >= 0 ? '⭐' : '🍕');
      h += '<div class="cat-label">' + icone + ' ' + cat.nome + '</div><div class="sabor-grid">';
      for (var i = 0; i < itens.length; i++) {
        var s = itens[i];
        var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
        var pm = Math.max(selTamanho.preco, sp.preco);
        h += '<button class="sabor-btn" onclick="selectSegundo(\\'' + s.id + '\\')">' + s.nome + ' <span>R$ ' + pm.toFixed(2) + '</span></button>';
      }
      h += '</div>';
    }"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: categorias de pizza corrigidas - agora mostra salgadas, especiais e doces")
else:
    print("ERRO: nao encontrou o bloco")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
