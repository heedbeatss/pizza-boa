import re

with open('app.html', 'r') as f:
    content = f.read()

# Extrair HTML (tudo antes de <script>)
html_end = content.find('<script>')
html_part = content[:html_end]

# Extrair CARDAPIO e ZONAS do JS atual
cardapio_match = re.search(r'var CARDAPIO = \{.*?\n\};', content, re.DOTALL)
cardapio_js = cardapio_match.group() if cardapio_match else ""

print(f"HTML: {len(html_part)} chars")
print(f"CARDAPIO: {len(cardapio_js)} chars")

# Salvar HTML
with open('temp_html.html', 'w') as f:
    f.write(html_part)

print("HTML salvo!")
