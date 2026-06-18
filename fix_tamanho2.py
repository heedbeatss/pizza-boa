with open('app.html', 'r') as f:
    lines = f.readlines()

# selectTamanho: linhas 511-521 (index 510-520)
new_func = """function selectTamanho(idx) {
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
      var metadeSpans = sec.querySelectorAll('.metade-row span');
      if (metadeSpans.length > 0) {
        var lastSpan = metadeSpans[metadeSpans.length - 1];
        lastSpan.textContent = 'R$ ' + selTamanho.preco.toFixed(2);
      }
      
      // Atualiza os precos de todos os botoes de sabor da 2a metade
      var saborBtns = sec.querySelectorAll('.sabor-btn');
      for (var i = 0; i < saborBtns.length; i++) {
        var btnEl = saborBtns[i];
        // Pega o id do sabor do atributo data-id
        var sid = btnEl.getAttribute('data-id');
        if (!sid) {
          // Fallback: extrai do onclick
          var onclickStr = btnEl.getAttribute('onclick') || '';
          var match = onclickStr.match(/selectSegundo\\('([^']+)'\\)/);
          if (match) sid = match[1];
        }
        if (sid) {
          var todos = CARDAPIO.categorias.flatMap(function(c) { return c.itens; });
          var s = todos.find(function(it) { return it.id === sid; });
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
  
  updateAddBtn();
}
"""

# Substituir linhas 510-520 (inclusive)
new_lines = lines[:510] + [new_func] + lines[521:]

with open('app.html', 'w') as f:
    f.writelines(new_lines)

print("OK: selectTamanho corrigido!")
