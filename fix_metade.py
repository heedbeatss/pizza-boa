with open('app.html', 'r') as f:
    content = f.read()

# Substituir a funcao setMetade inteira
old = """function setMetade(val) {
  selMetade = val;
  selSegundo = null;
  
  document.getElementById('btnInteira').classList.toggle('active', !val);
  document.getElementById('btnMetade').classList.toggle('active', val);
  
  var sec = document.getElementById('metadeSection');
  
  if (val) {
    // Mostra 1 metade
    var h = '<div class="metade-info">';
    h += '<div class="metade-row"><span>1a metade: <strong>' + currentItem.nome + '</strong></span>';
    h += '<span style="color:#a855f7">R$ ' + selTamanho.preco.toFixed(2) + '</span></div>';
    h += '<div style="font-size:12px;color:#a1a1a1">Escolha a 2a metade:</div>';
    h += '<div style="font-size:11px;color:#f59e0b;margin-top:4px">O preco final sera da metade mais cara</div></div>';
    
    // Pizzas salgadas
    var salgadas = CARDAPIO.categorias[0].itens.filter(function(i) { return i.id !== currentItem.id; });
    if (salgadas.length > 0) {
      h += '<div class="cat-label">Pizzas Salgadas</div><div class="sabor-grid">';
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
      h += '<div class="cat-label">Pizzas Doces</div><div class="sabor-grid">';
      for (var i = 0; i < doces.length; i++) {
        var s = doces[i];
        var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
        var pm = Math.max(selTamanho.preco, sp.preco);
        h += '<button class="sabor-btn" onclick="selectSegundo(\\'' + s.id + '\\')">' + s.nome + ' <span>R$ ' + pm.toFixed(2) + '</span></button>';
      }
      h += '</div>';
    }
    
    sec.innerHTML = h;
  } else {
    sec.innerHTML = '';
  }
  
  updateAddBtn();
}"""

new = """function setMetade(val) {
  selMetade = val;
  selSegundo = null;
  
  document.getElementById('btnInteira').classList.toggle('active', !val);
  document.getElementById('btnMetade').classList.toggle('active', val);
  
  var sec = document.getElementById('metadeSection');
  
  if (val) {
    // Mostra 1 metade
    var h = '<div class="metade-info">';
    h += '<div class="metade-row"><span>1a metade: <strong>' + currentItem.nome + '</strong></span>';
    h += '<span style="color:#a855f7">R$ ' + selTamanho.preco.toFixed(2) + '</span></div>';
    h += '<div style="font-size:12px;color:#a1a1a1">Escolha a 2a metade:</div>';
    h += '<div style="font-size:11px;color:#f59e0b;margin-top:4px">O preco final sera da metade mais cara</div></div>';
    
    // Percorre todas as categorias de pizza (salgadas, especiais, doces)
    for (var c = 0; c < CARDAPIO.categorias.length; c++) {
      var cat = CARDAPIO.categorias[c];
      // So mostra categorias de pizza (salgadas, especiais, doces)
      if (cat.id.indexOf('pizza') < 0 && cat.id.indexOf('especial') < 0) continue;
      
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
    }
    
    sec.innerHTML = h;
  } else {
    sec.innerHTML = '';
  }
  
  updateAddBtn();
}"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: setMetade corrigido - agora mostra todas as categorias de pizza")
else:
    print("ERRO: nao encontrou a funcao setMetade")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
