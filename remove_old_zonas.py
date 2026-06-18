with open('app.html', 'r') as f:
    content = f.read()

# Remover o codigo antigo de zonas que esta depois do callback do geocode
old = """  });
  
  var cepNum = parseInt(cep.replace(/\\D/g, '')) || 0;
  zonaAtual = null;
  
  for (var i = 0; i < ZONAS.length; i++) {
    var z = ZONAS[i];
    
    // Verifica por bairro
    if (z.bairros) {
      for (var j = 0; j < z.bairros.length; j++) {
        if (bn.indexOf(norm(z.bairros[j])) >= 0 || norm(z.bairros[j]).indexOf(bn) >= 0) {
          zonaAtual = z;
          break;
        }
      }
    }
    if (zonaAtual) break;
    
    // Verifica por CEP
    if (z.cepIni && z.cepFim && cepNum >= z.cepIni && cepNum <= z.cepFim) {
      zonaAtual = z;
      break;
    }
  }
  
  var box = document.getElementById('zonaBox');
  if (zonaAtual) {
    box.style.display = 'block';
    box.className = 'zona-box zona-ok';
    document.getElementById('zonaNome').textContent = zonaAtual.nome;
    document.getElementById('zonaValor').textContent = 'R$ ' + zonaAtual.valor.toFixed(2);
    document.getElementById('zonaValor').style.color = '#a855f7';
    document.getElementById('zonaTempo').textContent = zonaAtual.tempo;
  } else {
    box.style.display = 'none';
  }
  
  renderCheckoutSummary();
}"""

new = """  });
}"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: codigo antigo de zonas removido")
else:
    print("ERRO: nao encontrou o codigo antigo")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
