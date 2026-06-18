with open('app.html', 'r') as f:
    content = f.read()

old = '      <span class="badge">\ud83d\udd50 45-60 min</span>\n      <button onclick="showAdminLogin()"'

new = '      <span class="badge">\ud83d\udd50 45-60 min</span>\n      <span class="badge" id="openBadge" style="color:#4ade80;background:rgba(74,222,128,.15)">Aberto</span>\n      <div id="horarioAviso" style="display:none;margin-top:8px;padding:8px 12px;background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);border-radius:8px;font-size:12px;color:#f87171;text-align:center"></div>\n      <button onclick="showAdminLogin()"'

if old in content:
    content = content.replace(old, new, 1)
    print("OK: badge de status e aviso adicionados no header")
else:
    print("ERRO: nao encontrou o ponto")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
