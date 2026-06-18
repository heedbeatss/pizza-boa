with open('app.html', 'r') as f:
    content = f.read()

old = '          <div id="copyMsg" style="font-size:11px;color:#4ade80;margin-top:6px;display:none">\u2705 Copiado!</div>\n        </div>\n      </div>'

new = '          <div id="copyMsg" style="font-size:11px;color:#4ade80;margin-top:6px;display:none">\u2705 Copiado!</div>\n          <div style="margin-top:12px;padding:10px;background:rgba(37,211,102,.1);border:1px solid rgba(37,211,102,.3);border-radius:8px;font-size:12px;color:#a1a1a1;text-align:center">\n            <span style="color:#25d366;font-weight:700">Importante:</span> ap\u00f3s efetuar o pagamento, envie o comprovante pelo WhatsApp para confirmarmos seu pedido.\n          </div>\n        </div>\n      </div>'

if old in content:
    content = content.replace(old, new, 1)
    print("OK: aviso de comprovante adicionado")
else:
    # Tentar sem emoji
    old2 = '<div id="copyMsg" style="font-size:11px;color:#4ade80;margin-top:6px;display:none">'
    idx = content.find(old2)
    if idx >= 0:
        # Encontrar o fechamento deste div
        end_idx = content.find('</div>', idx)
        end_idx = content.find('</div>', end_idx + 1)  # segundo </div>
        end_idx = content.find('</div>', end_idx + 1)  # terceiro </div> - fecha o pixSection
        print(f"Encontrado em {idx}, fim em {end_idx}")
        print(f"Trecho: {repr(content[idx:end_idx+6])}")
    else:
        print("ERRO: nao encontrou copyMsg")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
