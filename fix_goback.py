with open('app.html', 'r') as f:
    content = f.read()

# 1. Encontrar e substituir o botão "Voltar ao Cardápio" por "Voltar ao Início"
old_btn = '<button onclick="goBack()" class="back-btn">← Voltar ao Cardápio</button>'
new_btn = '<button onclick="goBack()" class="back-btn">← Voltar ao Início</button>'

if old_btn in content:
    content = content.replace(old_btn, new_btn, 1)
    print("OK: Texto do botao alterado")
else:
    print("Botao nao encontrado, procurando alternativas...")
    # Tentar encontrar qualquer botao com goBack
    import re
    btns = re.findall(r'<button[^>]*onclick="goBack\(\)"[^>]*>[^<]*</button>', content)
    for b in btns:
        print(f"  Encontrado: {b}")

# 2. Verificar a funcao goBack
old_goback = """function goBack() {
  document.getElementById('checkoutPage').style.display = 'none';
  document.getElementById('adminPage').style.display = 'none';
  document.getElementById('cardapio').style.display = 'block';
  document.getElementById('catNavMenu').style.display = 'flex';
}"""

new_goback = """function goBack() {
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
}"""

if old_goback in content:
    content = content.replace(old_goback, new_goback, 1)
    print("OK: goBack corrigido")
else:
    print("ERRO: goBack nao encontrado - procurando...")
    # Procurar a funcao
    idx = content.find('function goBack()')
    if idx >= 0:
        print(f"  goBack encontrada na posicao {idx}")
        # Mostrar 200 chars a partir dai
        print(f"  Conteudo: {content[idx:idx+200]}")
    else:
        print("  goBack NAO encontrada no arquivo!")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
