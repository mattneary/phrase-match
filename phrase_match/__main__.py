from .phrase_match import phrase_match
import fitz

doc = fitz.open('paper.pdf')
page = doc[0]
txt = ''.join(page.get_text().splitlines())
tex = open('paper.tex', 'r').read()
print(tex)

rhizomes = phrase_match(tex, txt)
for ((a1, a2), (b1, b2)) in rhizomes:
    print('{}-{} -> {}-{}'.format(a1, a2, b1, b2))
    print(tex[a1:a2+1])
    print(txt[b1:b2+1])
    print('------')
