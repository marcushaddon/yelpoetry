"""Create an in memory db of rhyming phrases."""
import json
import os
import random
from typing import Dict, List
from textblob import TextBlob
import pronouncing

MAX_SENTENCE_LEN = 10
MAX_STARS = 2
MIN_SENTENCES = 5000
end_sentences: Dict[str, Dict[str, bool]] = {}

with open("data/raw/reviews.json", "r") as inf:
    sentcount = 0
    while sentcount < MIN_SENTENCES:
        line = inf.readline()
        review = json.loads(line)
        txt = review['text']
        if review['stars'] > MAX_STARS:
            continue

        sents = TextBlob(txt).sentences

        # TODO: Use numeric ids
        # Initialize each sentence
        for sent in sents:
            if len(sent.tokens) < MAX_SENTENCE_LEN:
                end_sentences[sent] = {}
                sentcount += 1
        
    # Link with rhyming end_sentences
    shortsents = list(end_sentences.keys())
    seen = {}
    for i, sent_a in enumerate(shortsents):
        seen[sent_a] = True
        # An assumption
        a_toks = sent_a.tokens
        a_last = a_toks[-2] if len(a_toks) > 1 else a_toks[0]
        for sent_b in shortsents[i:]:
            if sent_b in seen:
                continue

            b_toks = sent_b.tokens
            b_last = b_toks[-2] if len(b_toks) > 1 else b_toks[0]
            # print("do they rhyme? ", a_last, b_last)
            if not a_last.lower() == b_last.lower() and b_last in pronouncing.rhymes(a_last):
                end_sentences[sent_a.raw][sent_b.raw] = True
                end_sentences[sent_b.raw][sent_a.raw] = True


purged = { sentence.raw: end_sentences[sentence] for sentence in end_sentences.keys() if len(end_sentences[sentence]) > 0}
with open("data/red_roses_rhymes.json", "w") as outfile:
    json.dump(purged, outfile, indent=4)
