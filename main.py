import fandom
import json
from jisho_api import tokenize
import jinja2
from tqdm import tqdm
import webbrowser

fandom.set_wiki('vocaloidlyrics')

query = input('enter query: ')
print('\nsearching for song...')

res = fandom.search(query, results=5)

print('\nfirst 5 results:\n')
for x, song in enumerate(res):
    print(f'{x + 1}. {song[0]}')
print()

sel = input('which result to use?: ')
title = res[int(sel) - 1][0]

print('\ngetting lyrics...\n')
page = fandom.page(title)
lyrics = page.section('Lyrics').splitlines()
jisho = tokenize.Tokens

tokens_matrix = []

end = len(lyrics) - 2

for x, line in enumerate(lyrics):
    if line.startswith('English t'):
        end = x
        break

x = lyrics.index('Japanese') + 3
print('tokenizing lyrics...')
with tqdm(total=(end - x) / 3) as pbar:
    while x < end:
        tokens = []

        line = lyrics[x]

        data = json.loads(jisho.request(line).json())['data']
        for token in data:
            tokens.append(token)
        tokens_matrix.append(tokens)

        x += 3
        pbar.update(1)

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='./'))
template = env.get_template('template.html')

with open(f'songs/{title}.html', 'wb') as html:
    html.write(template.render(song_name=title, tokens_matrix=tokens_matrix).encode('utf-8'))

webbrowser.open(f'songs/{title}.html')
