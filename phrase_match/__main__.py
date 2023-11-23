from .phrase_match import phrase_match
import fitz
import html2text

h = html2text.HTML2Text()
doc = fitz.open('attention.pdf')
page = doc[0]
txt = ''.join(page.get_text().splitlines())
html = page.get_text("html")
md = h.handle(html)

rhizomes = phrase_match(md, txt)
for ((a1, a2), (b1, b2)) in rhizomes:
    print('{}-{} -> {}-{}'.format(a1, a2, b1, b2))
    print(md[a1:a2+1])
    print(txt[b1:b2+1])
    print('------')
