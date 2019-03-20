"""Create rhyme db for limmerick style poems."""

import json
from typing import Dict, List

import pronouncing
from textblob import TextBlob

MIN_LINE_COUNT = 500

with open("data/reviews.json", "r") as infile:
    fives: List[str] = []
    sevens: List[str] = []

    fivecount = 0
    sevencount = 0

    while sevencount < MIN_LINE_COUNT or fivecount < MIN_LINE_COUNT * 2:
        line = infile.readline()
        review = json.loads(line)
        if review['stars'] > 2.0:
            continue
        
        text = review['text']
        sents = TextBlob(text).sentences

        for sent in sents:
            words = sent.tokens
            phones = [pronouncing.phones_for_word(w) for w in words]
            sylcount = sum([pronouncing.syllable_count(p[0]) if len(p) > 0 else 0 for p in phones])
            if sylcount == 5:
                fives.append(sent.raw)
                fivecount += 1
            elif sylcount == 7:
                sevens.append(sent.raw)
                sevencount += 1

lines = {
    'fives': fives,
    'sevens': sevens,
}

with open('yelpoet/rhymes/haiku_rhymes.json', 'w') as outfile:
    json.dump(lines, outfile, indent=4)
