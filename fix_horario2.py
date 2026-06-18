with open('app.html', 'r') as f:
    content = f.read()

# Corrigir a funcao isPizzariaAberta para considerar o horario ate 01h
old = """function isPizzariaAberta() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) return false;
  return hora >= HORA_INICIO && hora < HORA_FIM;
}"""

new = """function isPizzariaAberta() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  
  // Verifica se o dia atual esta nos dias de funcionamento
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) return false;
  
  // Funciona das 18h ate 01h (do dia seguinte)
  // Se hora >= 18 (18h-23h) -> aberto
  // Se hora < 1 (00h-01h) -> aberto (ainda e o mesmo dia de funcionamento)
  if (hora >= 18) return true;
  if (hora < 1) return true;
  
  return false;
}"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: isPizzariaAberta corrigido")
else:
    print("ERRO: nao encontrou isPizzariaAberta")

# Corrigir getHorarioInfo tambem
old2 = """function getHorarioInfo() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  var nomes = ['Domingo','Segunda','Terca','Quarta','Quinta','Sexta','Sabado'];
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) return 'Hoje e ' + nomes[dia] + '. Fechados. Terca a Domingo, 18h-01h.';
  if (hora < HORA_INICIO) return 'Ainda nao abrimos. Hoje abrimos as ' + HORA_INICIO + 'h.';
  if (hora >= HORA_FIM) return 'Ja fechamos. Abrimos amanha as ' + HORA_INICIO + 'h.';
  return 'Estamos abertos!';
}"""

new2 = """function getHorarioInfo() {
  var agora = new Date();
  var dia = agora.getDay();
  var hora = agora.getHours();
  var nomes = ['Domingo','Segunda','Terca','Quarta','Quinta','Sexta','Sabado'];
  
  if (DIAS_FUNCIONAMENTO.indexOf(dia) < 0) {
    return 'Hoje e ' + nomes[dia] + '. Fechados. Terca a Domingo, 18h-01h.';
  }
  
  // Entre 01h e 18h -> fechado
  if (hora >= 1 && hora < 18) {
    return 'Ainda nao abrimos. Hoje abrimos as 18h.';
  }
  
  return 'Estamos abertos!';
}"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("OK: getHorarioInfo corrigido")
else:
    print("ERRO: nao encontrou getHorarioInfo")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
