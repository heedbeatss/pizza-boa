with open('app.html', 'r') as f:
    content = f.read()

# Adicionar funcao showHome antes de goBack
old = "function goBack() {"
new = """function showHome() {
  // Esconder todas as paginas
  document.getElementById('checkoutPage').style.display = 'none';
  document.getElementById('adminPage').style.display = 'none';
  document.getElementById('checkoutSuccess').style.display = 'none';
  document.getElementById('checkoutForm').style.display = 'block';
  
  // Mostrar cardapio
  document.getElementById('cardapio').style.display = 'block';
  var catNav = document.getElementById('catNavMenu');
  if (catNav) catNav.style.display = 'flex';
  
  // Resetar formulario
  document.getElementById('cep').value = '';
  document.getElementById('rua').value = '';
  document.getElementById('bairro').value = '';
  document.getElementById('cidade').value = '';
  document.getElementById('numero').value = '';
  document.getElementById('complemento').value = '';
  document.getElementById('referencia').value = '';
  document.getElementById('nome').value = '';
  document.getElementById('telefone').value = '';
  document.getElementById('troco').value = '';
  document.getElementById('obs').value = '';
  
  // Limpar status
  var cepStatus = document.getElementById('cepStatus');
  if (cepStatus) cepStatus.style.display = 'none';
  var zonaBox = document.getElementById('zonaBox');
  if (zonaBox) zonaBox.style.display = 'none';
  var checkoutError = document.getElementById('checkoutError');
  if (checkoutError) checkoutError.style.display = 'none';
  
  zonaAtual = null;
  
  // Voltar ao topo
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function goBack() {"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: showHome adicionada")
else:
    print("ERRO")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
