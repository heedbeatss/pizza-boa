with open('app.html', 'r') as f:
    content = f.read()

old = "document.addEventListener('DOMContentLoaded', function() { updateHorarioHeader(); initPizzariaCoords(); });"
new = "document.addEventListener('DOMContentLoaded', function() { updateHorarioHeader(); initPizzariaCoords(); render(); });"

if old in content:
    content = content.replace(old, new, 1)
    print("OK: render() adicionado ao DOMContentLoaded")
else:
    print("ERRO")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
