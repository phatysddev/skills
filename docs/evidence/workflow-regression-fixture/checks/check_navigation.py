from pathlib import Path
r=Path(__file__).resolve().parents[1]/'app'
for page in r.glob('*.html'):
 for n in range(1,5):
  assert f'href="page{n}.html"' in page.read_text()
  assert (r/f'page{n}.html').exists()
print('navigation: 4 pages x 4 targets passed')
