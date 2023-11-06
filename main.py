import fandom
import json
from jisho_api import tokenize
import jinja2
from tqdm import tqdm
import webbrowser

query = input('enter query: ')
fandom.set_wiki('vocaloidlyrics')
print('Searching for song...')
res = fandom.search(query, results=1)[0]
print('Getting lyrics...')
page = fandom.page(pageid=res[1])
lyrics = page.section('Lyrics').splitlines()
jisho = tokenize.Tokens

tokens_matrix = []

end = len(lyrics) - 2

for x in range(len(lyrics)):
    if lyrics[x].startswith('English t'):
        end = x
        break

x = lyrics.index('Japanese') + 3
print('Tokenizing lyrics...')
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

with open(f'songs/{res[0]}.html', 'wb') as html:
    html.write(template.render(song_name=res[0], tokens_matrix=tokens_matrix).encode('utf-8'))

webbrowser.open(f'songs/{res[0]}.html')
