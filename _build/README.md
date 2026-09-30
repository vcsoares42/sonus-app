# Gerador das páginas de privacidade

As 14 páginas são geradas a partir de `template.html` e dos textos em `content/<idioma>.json`.
GitHub Pages não publica pastas que começam com `_`, então nada aqui fica público no site.

Para mudar o texto da política: edite `content/<idioma>.json` (em todos os idiomas) e rode

    python3 _build/build.py .

a partir da raiz do repositório. O script reescreve as páginas e os botões de idioma do `index.html`.
`check.py content/<idioma>.json` confere se a estrutura HTML e os links batem com o inglês
(`source-body.en.html`). O árabe usa ◂ no caminho dos ajustes, então o aviso sobre ▸ é esperado.
