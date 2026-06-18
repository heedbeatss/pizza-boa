with open('app.html', 'r') as f:
    content = f.read()

# Adicionar aviso de comprovante depois do botao copiar chave
old = """          <div id="copyMsg" style="font-size:11px;color:#4ade80;margin-top:6px;display:none">Copiado!</div>
        </div>
      </div>"""

new = """          <div id="copyMsg" style="font-size:11px;color:#4ade80;margin-top:6px;display:none">Copiado!</div>
          <div style="margin-top:12px;padding:10px;background:rgba(37,211,102,.1);border:1px solid rgba(37,211,102,.3);border-radius:8px;font-size:12px;color:#a1a1a1;text-align:center">
            <span style="color:#25d366;font-weight:700">Importante:</span> apos efetuar o pagamento, envie o comprovante pelo WhatsApp para confirmarmos seu pedido.
          </div>
        </div>
      </div>"""

if old in content:
    content = content.replace(old, new, 1)
    print("OK: aviso de comprovante adicionado na secao PIX")
else:
    print("ERRO: nao encontrou o ponto de insercao")

with open('app.html', 'w') as f:
    f.write(content)

print("Pronto!")
