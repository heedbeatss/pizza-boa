with open('app.html', 'r') as f:
    lines = f.readlines()

# Linha 122 (index 121) e linha 123 (index 122)
# Inserir depois da linha 122 (badge de tempo) e antes da linha 123 (botao admin)
new_lines = lines[:122] + [
    '      <span class="badge" id="openBadge" style="color:#4ade80;background:rgba(74,222,128,.15)">Aberto</span>\n',
    '      <div id="horarioAviso" style="display:none;margin-top:8px;padding:8px 12px;background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);border-radius:8px;font-size:12px;color:#f87171;text-align:center"></div>\n'
] + lines[122:]

with open('app.html', 'w') as f:
    f.writelines(new_lines)

print("OK: badge e aviso adicionados!")
