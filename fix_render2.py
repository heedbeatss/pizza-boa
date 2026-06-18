with open('app.html', 'r') as f:
    content = f.read()

# Remover a chamada solta de render() no final
old = """// ============ INIT ============
render();
carregarPedidos();"""

new = """// ============ INIT ============
// render() e carregarPedidos() sao chamados no DOMContentLoaded abaixo"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: chamada solta de render() removida")
else:
    print("ERRO: nao encontrou INIT")

# Garantir que render() esta no DOMContentLoaded
old2 = "document.addEventListener('DOMContentLoaded', function() { updateHorarioHeader(); initPizzariaCoords(); render(); });"
if old2 not in content:
    # Tentar versao sem render
    old3 = "document.addEventListener('DOMContentLoaded', function() { updateHorarioHeader(); initPizzariaCoords(); });"
    if old3 in content:
        content = content.replace(old3, old2, 1)
        print("OK: render() adicionado ao DOMContentLoaded")
    else:
        print("ERRO: nao encontrou DOMContentLoaded")
else:
    print("OK: DOMContentLoaded ja tem render()")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
