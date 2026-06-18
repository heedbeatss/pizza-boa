with open('app.html', 'r') as f:
    content = f.read()

old = """// Taxa por km (R$ 1,00 por km)
var TAXA_POR_KM = 1.0;
var TAXA_MINIMA = 5.0; // Taxa minima de entrega
var TAXA_MAXIMA = 25.0; // Taxa maxima de entrega"""

new = """// Taxa de entrega: R$ 3,00 fixo (motoboy) + R$ 1,00 por km
var TAXA_FIXA_MOTOBOY = 3.0;
var TAXA_POR_KM = 1.0;
var TAXA_MINIMA = 3.0; // Taxa minima (so a fixa do motoboy)
var TAXA_MAXIMA = 30.0; // Taxa maxima de entrega"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: Taxa fixa do motoboy adicionada")
else:
    print("ERRO: nao encontrou as taxas")

# Atualizar funcao calcTaxaEntrega
old2 = """function calcTaxaEntrega(distKm) {
  if (distKm <= 0) return 0;
  var taxa = Math.ceil(distKm) * TAXA_POR_KM; // Arredonda km pra cima
  taxa = Math.max(taxa, TAXA_MINIMA); // Aplica taxa minima
  taxa = Math.min(taxa, TAXA_MAXIMA); // Aplica taxa maxima
  return taxa;
}"""

new2 = """function calcTaxaEntrega(distKm) {
  if (distKm <= 0) return TAXA_FIXA_MOTOBOY;
  var kmArredondado = Math.ceil(distKm); // Arredonda km pra cima
  var taxa = TAXA_FIXA_MOTOBOY + (kmArredondado * TAXA_POR_KM);
  taxa = Math.min(taxa, TAXA_MAXIMA); // Aplica taxa maxima
  return taxa;
}"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("OK: calcTaxaEntrega atualizado")
else:
    print("ERRO: nao encontrou calcTaxaEntrega")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
