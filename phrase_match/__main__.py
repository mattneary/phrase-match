from .phrase_match import phrase_match

with open('./quoted.txt', 'r') as file:
    quoted = file.read().strip()
with open('./summary.txt', 'r') as file:
    summary = file.read().strip()

rhizomes = phrase_match(quoted, summary)
for ((a1, a2), (b1, b2)) in rhizomes:
    print('{}-{} -> {}-{}'.format(a1, a2, b1, b2))
    print(quoted[a1:a2+1])
    print(summary[b1:b2+1])
    print('------')
