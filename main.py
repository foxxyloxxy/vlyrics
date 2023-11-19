import fandom
import json
from jisho_api import tokenize
import jinja2
from tqdm import tqdm
import webbrowser
import os

tokenizer = tokenize.Tokens

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

lines = []

end = len(lyrics) - 2

for x, line in enumerate(lyrics):
    if line.startswith('English t'):
        end = x
        break

x = lyrics.index('Japanese') + 3
print('tokenizing lyrics...')

gen_furi = os.path.exists(f'songs/{title}.txt')
flag = 'r' if gen_furi else 'w'

with open(f'songs/{title}.txt', flag) as text:
    with tqdm(total=(end - x) / 3) as pbar:
        contents = None
        if gen_furi:
            contents = text.read()

        while x < end:
            tokens = []

            japanese = lyrics[x]

            data = json.loads(tokenizer.request(japanese).json())['data']
            for token in data:
                token['chars'] = []
                token_furi = False
                for char in token['token']:
                    char_dict = {
                        'char': char
                    }
                    if gen_furi:
                        contents = contents.split(char, 1)[1]
                        if contents[0] == '「':
                            if contents[1] == '「':
                                furi_index = 2
                                token_furi = True
                            else:
                                furi_index = 1
                            split = contents.split('」', 1)
                            char_dict['furi'] = split[0][furi_index:]
                            if len(split) != 1:
                                contents = split[1]
                    token['chars'].append(char_dict)
                if token_furi:
                    token['chars'][0]['furi'] = token['chars'][len(token['chars']) - 1]['furi']
                    for y in range(1, len(token['chars'])):
                        token['chars'][0]['char'] += token['chars'][y]['char']
                    token['chars'] = [token['chars'][0]]
                tokens.append(token)

            line = {
                'tokens': tokens,
                'trans': lyrics[x + 2]
            }

            if not gen_furi:
                text.write(f'{japanese}\n')

            lines.append(line)

            x += 3
            pbar.update(1)

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='./'))
template = env.get_template('template.html')

with open(f'songs/{title}.html', 'wb') as html:
    html.write(template.render(song_name=title, lines=lines).encode('utf-8'))

webbrowser.open(f'songs/{title}.html')
