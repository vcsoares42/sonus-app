"""Build every privacy page from one template. Usage: python3 build.py <web repo> [--extract-existing]"""
import json, re, sys, os, html
repo = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://vcsoares42.github.io/sonus-app/'
# (lang, file, flag, native name); pill order: current two, then by market wave
LANGS = [
    ('pt-BR', 'privacidade.html', '🇧🇷', 'Português'),
    ('en', 'privacy.html', '🇺🇸', 'English'),
    ('es', 'privacidad.html', '🇪🇸', 'Español'),
    ('fr', 'confidentialite.html', '🇫🇷', 'Français'),
    ('de', 'datenschutz.html', '🇩🇪', 'Deutsch'),
    ('it', 'informativa-privacy.html', '🇮🇹', 'Italiano'),
    ('nl', 'privacybeleid.html', '🇳🇱', 'Nederlands'),
    ('sv', 'integritetspolicy.html', '🇸🇪', 'Svenska'),
    ('da', 'privatlivspolitik.html', '🇩🇰', 'Dansk'),
    ('nb', 'personvern.html', '🇳🇴', 'Norsk'),
    ('ja', 'privacy-ja.html', '🇯🇵', '日本語'),
    ('ko', 'privacy-ko.html', '🇰🇷', '한국어'),
    ('zh-Hant', 'privacy-zh-hant.html', '🇹🇼', '繁體中文'),
    ('ar', 'privacy-ar.html', '🇸🇦', 'العربية'),
]
tmpl = open(os.path.join(here, 'template.html')).read()

def extract(path, lang):
    t = open(path).read()
    g = lambda pat: re.search(pat, t, re.S).group(1)
    return {'lang': lang, 'title': html.unescape(g(r'<title>(.*?)</title>')),
            'meta_description': html.unescape(g(r'<meta name="description" content="(.*?)">')),
            'h1': g(r'<h1>(.*?)</h1>'), 'updated': g(r'<p class="atualizacao">(.*?)</p>'),
            'home': g(r'<a href="index.html">(.*?)</a>'), 'nav_label': g(r'<nav class="idiomas" aria-label="(.*?)">'),
            'body_html': t[t.index('</h1>'):t.index('  </main>')].split('</p>\n\n', 1)[1].rstrip() + '\n'}

if '--extract-existing' in sys.argv:
    for lang, f in [('pt-BR', 'privacidade.html'), ('en', 'privacy.html')]:
        json.dump(extract(os.path.join(repo, f), lang), open(os.path.join(here, 'content', f'{lang}.json'), 'w'), ensure_ascii=False, indent=1)
    sys.exit()

alternates = '\n'.join(f'  <link rel="alternate" hreflang="{l}" href="{BASE}{f}">' for l, f, _, _ in LANGS)
for lang, fname, _, _ in LANGS:
    p = os.path.join(here, 'content', f'{lang}.json')
    if not os.path.exists(p): print('SKIP (no translation yet)', lang); continue
    d = json.load(open(p))
    pills = []
    for l, f, flag, name in LANGS:
        inner = f'<span class="bandeira">{flag}</span> {name}'
        pills.append(f'      <span class="ativo">{inner}</span>' if l == lang else f'      <a href="{f}" hreflang="{l}" lang="{l}">{inner}</a>')
    page = (tmpl.replace('{{LANG}}', lang)
            .replace('{{DIR}}', ' dir="rtl"' if lang == 'ar' else '')
            .replace('{{TITLE}}', html.escape(d['title'], quote=False))
            .replace('{{META}}', html.escape(d['meta_description']))
            .replace('{{ALTERNATES}}', alternates)
            .replace('{{NAV_LABEL}}', html.escape(d['nav_label']))
            .replace('{{PILLS}}', '\n'.join(pills))
            .replace('{{H1}}', d['h1']).replace('{{UPDATED}}', d['updated'])
            .replace('{{HOME}}', d['home'])
            .replace('{{BODY}}', d['body_html'].rstrip('\n')))
    open(os.path.join(repo, fname), 'w').write(page)
    print('wrote', fname)

# index: same pills, all languages
idx_path = os.path.join(repo, 'index.html')
idx = open(idx_path).read()
links = '\n'.join(f'    <a href="{f}" hreflang="{l}" lang="{l}"><span class="bandeira">{flag}</span> {name}</a>' for l, f, flag, name in LANGS)
idx = re.sub(r'(    <span class="rotulo">Política de Privacidade</span>\n).*?(\n  </nav>)', lambda m: m.group(1) + links + m.group(2), idx, flags=re.S)
open(idx_path, 'w').write(idx)
print('wrote index.html')
