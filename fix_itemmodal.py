with open('app.html', 'r') as f:
    content = f.read()

# Corrigir itemModal -> 'itemModal'
old = "onclick=\"closeModal(\\'' + itemModal\\')\""
new = "onclick=\"closeModal('itemModal')\""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: itemModal corrigido")
else:
    print("ERRO: nao encontrou itemModal")

# Verificar se tem mais erros similares
import re
# Procurar closeModal com argumento errado
matches = re.findall(r"closeModal\([^)]+\)", content)
for m in matches:
    print(f"  closeModal: {m}")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
