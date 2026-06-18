with open('app.html', 'r') as f:
    content = f.read()

old = """function selectTamanho(idx) {
  selTamanho = currentItem.tamanhos[idx];
  document.querySelectorAll('.size-btn').forEach(function(b) { b.classList.remove('active'); });
  event.target.closest('.size-btn').classList.add('active');
  
  // Atualiza preco no botao inteira
  var btn = document.getElementById('btnInteira');
  if (btn) btn.innerHTML = 'Inteira<div style="font-size:11px;opacity:0.7">R$ ' + selTamanho.preco.toFixed(2) + '</div>';
  
  updateAddBtn();
}"""

new = """function selectTamanho(idx) {
  selTamanho = currentItem.tamanhos[idx];
  document.querySelectorAll('.size-btn').forEach(function(b) { b.classList.remove('active'); });
  event.target.closest('.size-btn').classList.add('active');
  
  // Atualiza preco no botao inteira
  var btn = document.getElementById('btnInteira');
  if (btn) btn.innerHTML = 'Inteira<div style="font-size:11px;opacity:0.7">R$ ' + selTamanho.preco.toFixed(2) + '</div>';
  
  // Atualiza precos da 2a metade se estiver no modo metade
  if (selMetade) {
    var sec = document.getElementById('metadeSection');
    if (sec) {
      // Atualiza o preco da 1a metade exibida
      var metadeInfo = sec.querySelector('.metade-row span:last-child');
      if (metadeInfo) metadeInfo.textContent = 'R$ ' + selTamanho.preco.toFixed(2);
      
      // Atualiza os precos de todos os botoes de sabor da 2a metade
      var saborBtns = sec.querySelectorAll('.sabor-btn');
      for (var i = 0; i < saborBtns.length; i++) {
        var btnEl = saborBtns[i];
        var saborId = btnEl.getAttribute('onclick');
        if (saborId) {
          var match = saborId.match(/selectSegundo\\('([^']+)'\\)/);
          if (match) {
            var sid = match[1];
            var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; });
            var s = todos.find(function(i) { return i.id === sid; });
            if (s) {
              var sp = s.tamanhos.find(function(t) { return t.nome === selTamanho.nome; }) || s.tamanhos[0];
              var pm = Math.max(selTamanho.preco, sp.preco);
              var span = btnEl.querySelector('span');
              if (span) span.textContent = 'R$ ' + pm.toFixed(2);
            }
          }
        }
      }
    }
  }
  
  updateAddBtn();
}"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: selectTamanho agora atualiza precos da 2a metade")
else:
    print("ERRO: nao encontrou selectTamanho")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
