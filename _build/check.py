import json, re, sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'source-body.en.html')).read()
d = json.load(open(sys.argv[1]))
err = []
for k in ['lang', 'title', 'meta_description', 'h1', 'updated', 'home', 'nav_label', 'body_html']:
    if not str(d.get(k, '')).strip(): err.append(f'missing {k}')
b = d.get('body_html', '')
tags = lambda h: re.findall(r'</?([a-z0-9]+)', h)
if tags(b) != tags(src): err.append(f'tag sequence differs from source:\n  src {tags(src)}\n  out {tags(b)}')
for a in re.findall(r'href="[^"]+"', src):
    if a not in b: err.append(f'missing link {a}')
for w in ['Sonus', 'Sonus Pro', 'Apple', 'App Store', 'PostHog', 'RevenueCat', 'LGPD', 'GDPR', 'AdServices', 'Google', 'Firebase', 'Vinícius Soares', 'vcsoares42@gmail.com']:
    if src.count(w) and not b.count(w): err.append(f'missing {w!r}')
arrow = '◂' if d.get('lang') == 'ar' else '▸'
if b.count(arrow) != src.count('▸'): err.append(f'settings paths must have exactly {src.count("▸")} {arrow}')
if d.get('lang') != 'en' and ('Share Usage Data' in b or 'Settings ▸' in b): err.append('English settings path left in')
print('\n'.join(err) if err else f"OK {d.get('lang')}")
sys.exit(1 if err else 0)
