# vlyrics

### Script to pull vocaloid lyrics from the vocaloidlyrics fandom wiki and annotate/color code by part of speech

use run.sh on linux, run.bat on windows

also i haven't actually tested the .bat script

### color key:
- blue: noun/proper noun
- green: verb
- orange: adjective/adverb
- white: particle
- pink: pronoun
- teal: determiner
- red: interjection
- purple: conjunction
- yellow: prefix/suffix/unknown

### furigana:
running the first time will generate a .txt file with the lyrics

furigana has to be added manually to that file and then running the script again will generate a new html with furigana

use 「」with furigana within to add it for individual characters, or 「「」」to add it for the entire word/token

ex:

`大人「「おとな」」はもう寝「ね」る時「じ」間「かん」よ`