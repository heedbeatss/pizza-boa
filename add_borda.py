with open('app.html', 'r') as f:
    content = f.read()

# 1. Adicionar toggle de borda depois da metade section
old = """    h += '<div id="metadeSection"></div>';
  }
  
  // Quantidade"""

new = """    h += '<div id="metadeSection"></div>';
  }
  
  // Borda recheada
  if (isPizza) {
    h += '<label class="label">Borda Recheada</label><div class="toggle-row">';
    h += '<button class="toggle-btn active" id="btnBordaNao" onclick="setBorda(0)">Sem borda</button>';
    h += '<button class="toggle-btn" id="btnBordaSim" onclick="setBorda(1)">Catupiry <span style="font-size:11px;opacity:0.7">+ R$ 8,00</span></button>';
    h += '</div>';
  }
  
  // Quantidade"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: toggle de borda adicionado")
else:
    print("ERRO: nao encontrou o ponto de insercao")

# 2. Atualizar calcPrice() pra incluir borda
old2 = """function calcPrice() {
  var preco = selTamanho.preco;
  if (selMetade && selSegundo) {
    var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; });
    var s = todos.find(function(i) { return i.id === selSegundo; });
    if (s) {
      var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
      preco = Math.max(preco, sp.preco);
    }
  }
  return preco * selQty;
}"""

new2 = """function calcPrice() {
  var preco = selTamanho.preco;
  if (selMetade && selSegundo) {
    var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; });
    var s = todos.find(function(i) { return i.id === selSegundo; });
    if (s) {
      var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
      preco = Math.max(preco, sp.preco);
    }
  }
  if (selBorda) preco += 8;
  return preco * selQty;
}"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("OK: calcPrice atualizado com borda")
else:
    print("ERRO: nao encontrou calcPrice")

# 3. Adicionar funcao setBorda()
old3 = """function setMetade(val) {"""

new3 = """function setBorda(val) {
  selBorda = val;
  document.getElementById('btnBordaNao').classList.toggle('active', val === 0);
  document.getElementById('btnBordaSim').classList.toggle('active', val === 1);
  updateAddBtn();
}

function setMetade(val) {"""

if old3 in content:
    content = content.replace(old3, new3, 1)
    print("OK: funcao setBorda adicionada")
else:
    print("ERRO: nao encontrou setMetade")

# 4. Atualizar addToCart() pra incluir borda no nome
old4 = """  var nome = currentItem.nome;
  if (selMetade && selSegundo) {
    var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; });
    var s = todos.find(function(i) { return i.id === selSegundo; });
    if (s) nome = '1/2 ' + currentItem.nome + ' / 1/2 ' + s.nome;
  }"""

new4 = """  var nome = currentItem.nome;
  if (selMetade && selSegundo) {
    var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; });
    var s = todos.find(function(i) { return i.id === selSegundo; });
    if (s) nome = '1/2 ' + currentItem.nome + ' / 1/2 ' + s.nome;
  }
  if (selBorda) nome += ' (borda catupiry)';"""

if old4 in content:
    content = content.replace(old4, new4, 1)
    print("OK: addToCart atualizado com borda")
else:
    print("ERRO: nao encontrou addToCart")

with open('app.html', 'w') as f:
    f.write(content)

print("\nTudo pronto!")
