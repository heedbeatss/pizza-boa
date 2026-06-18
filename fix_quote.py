with open('app.html', 'r') as f:
    content = f.read()

# O problema: a string usa ' como delimitador e tambem ' dentro
# Solucao: usar \" ao inves de \'
old = "h += '<div class=\"modal-header\"><div><h2>' + item.nome + '</h2><p>' + item.descricao + '</p></div><button class=\"modal-close\" onclick=\"closeModal('itemModal')\">✕</button></div>';"
new = 'h += \'<div class="modal-header"><div><h2>\' + item.nome + \'</h2><p>\' + item.descricao + \'</p></div><button class="modal-close" onclick="closeModal(\\\'itemModal\\\')">✕</button></div>\';'

print(f"Old: {old[:80]}...")
print(f"New: {new[:80]}...")

if old in content:
    content = content.replace(old, new, 1)
    print("OK!")
else:
    print("ERRO: nao encontrou")

with open('app.html', 'w') as f:
    f.write(content)

# Testar
import subprocess
start = content.find('<script>') + 8
end = content.find('</script>')
js = content[start:end]
with open('/tmp/test.js', 'w') as f:
    f.write(js)
result = subprocess.run(['node', '-c', '/tmp/test.js'], capture_output=True, text=True)
if result.returncode == 0:
    print("JS VALIDO!")
else:
    print("ERRO:", result.stderr[:200])
