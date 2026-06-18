with open('app.html', 'r') as f:
    content = f.read()

# 1. Adicionar constante de pedido minimo para entrega gratis
old = "var RAIO_MAXIMO_KM = 15; // Nao entrega acima de X km"
new = "var RAIO_MAXIMO_KM = 15; // Nao entrega acima de X km\nvar MIN_PEDIDO_GRATIS = 100; // Pedido acima de R$ 100 tem entrega gratis"

if old in content:
    content = content.replace(old, new, 1)
    print("OK: MIN_PEDIDO_GRATIS adicionado")
else:
    print("ERRO: nao encontrou RAIO_MAXIMO_KM")

# 2. Atualizar calcTaxaEntrega para considerar pedido gratis
old2 = """function calcTaxaEntrega(distKm) {
  if (distKm <= 0) return TAXA_FIXA_MOTOBOY;
  var kmArredondado = Math.ceil(distKm); // Arredonda km pra cima
  var taxa = TAXA_FIXA_MOTOBOY + (kmArredondado * TAXA_POR_KM);
  taxa = Math.min(taxa, TAXA_MAXIMA); // Aplica taxa maxima
  return taxa;
}"""

new2 = """function calcTaxaEntrega(distKm, totalPedido) {
  if (distKm <= 0) return TAXA_FIXA_MOTOBOY;
  // Entrega gratis para pedidos acima de R$ 100
  if (totalPedido >= MIN_PEDIDO_GRATIS) return 0;
  var kmArredondado = Math.ceil(distKm); // Arredonda km pra cima
  var taxa = TAXA_FIXA_MOTOBOY + (kmArredondado * TAXA_POR_KM);
  taxa = Math.min(taxa, TAXA_MAXIMA); // Aplica taxa maxima
  return taxa;
}"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("OK: calcTaxaEntrega atualizado com pedido gratis")
else:
    print("ERRO: nao encontrou calcTaxaEntrega")

# 3. Atualizar a chamada de calcTaxaEntrega em calcularEntrega
old3 = """    // Verifica se bairro e gratuito
    var bn = norm(bairro);
    var isGratis = BAIRROS_GRATIS.indexOf(bn) >= 0;
    var totalPedido = 0;
    for (var i = 0; i < cart.length; i++) totalPedido += cart[i].preco * cart[i].qty;
    if (isGratis && totalPedido >= MIN_GRATIS) taxa = 0;"""

new3 = """    // Calcula total do pedido
    var totalPedido = 0;
    for (var i = 0; i < cart.length; i++) totalPedido += cart[i].preco * cart[i].qty;
    
    // Verifica se bairro e gratuito OU pedido acima de R$ 100
    var bn = norm(bairro);
    var isGratis = BAIRROS_GRATIS.indexOf(bn) >= 0;
    if ((isGratis && totalPedido >= MIN_GRATIS) || totalPedido >= MIN_PEDIDO_GRATIS) taxa = 0;"""

if old3 in content:
    content = content.replace(old3, new3, 1)
    print("OK: verifica de gratis atualizada")
else:
    print("ERRO: nao encontrou verificacao de gratis")

# 4. Atualizar a outra chamada de calcTaxaEntrega (na renderCheckoutSummary)
old4 = """    var taxa = calcTaxaEntrega(distKm);"""
new4 = """    var totalPedido = 0;
    for (var i = 0; i < cart.length; i++) totalPedido += cart[i].preco * cart[i].qty;
    var taxa = calcTaxaEntrega(distKm, totalPedido);"""

if old4 in content:
    content = content.replace(old4, new4, 1)
    print("OK: chamada de calcTaxaEntrega atualizada")
else:
    print("ERRO: nao encontrou chamada de calcTaxaEntrega")

# 5. Adicionar aviso de promocao no resumo do checkout
old5 = """  if (zonaAtual) {
    h += '<div class="cart-summary-row"><span class="lbl">Distancia</span><span class="val">' + distInfo + '</span></div>';
    h += '<div class="cart-summary-row"><span class="lbl">Entrega</span><span class="val" style="color:' + (zonaAtual.valor === 0 ? '#4ade80' : '#a855f7') + '">' + (zonaAtual.valor === 0 ? 'GRATIS' : 'R$ ' + zonaAtual.valor.toFixed(2)) + '</span></div>';
    h += '<div class="cart-summary-row"><span class="lbl">Tempo estimado</span><span class="val">' + zonaAtual.tempo + '</span></div>';
  }"""

new5 = """  if (zonaAtual) {
    h += '<div class="cart-summary-row"><span class="lbl">Distancia</span><span class="val">' + distInfo + '</span></div>';
    h += '<div class="cart-summary-row"><span class="lbl">Entrega</span><span class="val" style="color:' + (zonaAtual.valor === 0 ? '#4ade80' : '#a855f7') + '">' + (zonaAtual.valor === 0 ? 'GRATIS' : 'R$ ' + zonaAtual.valor.toFixed(2)) + '</span></div>';
    h += '<div class="cart-summary-row"><span class="lbl">Tempo estimado</span><span class="val">' + zonaAtual.tempo + '</span></div>';
  }
  // Aviso de promocao
  if (total > 0 && total < MIN_PEDIDO_GRATIS && zonaAtual && zonaAtual.valor > 0) {
    var falta = MIN_PEDIDO_GRATIS - total;
    h += '<div style="margin-top:8px;padding:8px;background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.3);border-radius:8px;font-size:12px;color:#4ade80;text-align:center">';
    h += 'Falta R$ ' + falta.toFixed(2) + ' para entrega GRATIS!</div>';
  }"""

if old5 in content:
    content = content.replace(old5, new5, 1)
    print("OK: aviso de promocao adicionado no checkout")
else:
    print("ERRO: nao encontrou resumo do checkout")

# 6. Adicionar banner de promocao no topo do cardapio
old6 = '<div class="cat-nav"><div class="cat-nav-inner" id="catNavMenu"></div></div>'
new6 = """<div style="background:linear-gradient(90deg,rgba(88,28,135,.3),rgba(168,85,247,.2));padding:10px 16px;text-align:center;font-size:13px;color:#a855f7;border-bottom:1px solid rgba(88,28,135,.2)">
    PEDIDOS ACIMA DE R$ 100 TÊM ENTREGA GRATIS!
  </div>
  <div class="cat-nav"><div class="cat-nav-inner" id="catNavMenu"></div></div>"""

if old6 in content:
    content = content.replace(old6, new6, 1)
    print("OK: banner de promocao adicionado no topo")
else:
    print("ERRO: nao encontrou cat-nav")

with open('app.html', 'w') as f:
    f.write(content)

print("\nTudo pronto!")
