with open('app.html', 'r') as f:
    content = f.read()

# Encontrar o fim do CARDAPIO e adicionar ;
# O CARDAPIO termina com "  }\n\n// ============ HORARIO"
old = "  }\n\n// ============ HORARIO DE FUNCIONAMENTO ============"
new = "  };\n\n// ============ HORARIO DE FUNCIONAMENTO ============"

if old in content:
    content = content.replace(old, new, 1)
    print("OK: CARDAPIO fechado com ;")
else:
    print("ERRO: nao encontrou fim do CARDAPIO")

with open('app.html', 'w') as f:
    f.write(content)

# Validar
import subprocess
start = content.find('<script>') + 8
end = content.find('</script>')
js = content[start:end]
with open('/tmp/test_ok.js', 'w') as f:
    f.write(js)
result = subprocess.run(['node', '-c', '/tmp/test_ok.js'], capture_output=True, text=True)
if result.returncode == 0:
    print("JS VALIDO!")
else:
    print("ERRO:", result.stderr[:300])
