"""Create rhyming dict for limmericks."""
import re
import json
import os
import time

from typing import Dict, List

import pronouncing as p
from textblob import TextBlob

MIN_A_COUNT = 100
MIN_B_COUNT = MIN_A_COUNT * 2 / 5

# Stress pattern for limericks
limmerick_a = re.compile("0{0,2}1[01]{2}1[01]{2}1[01]{0,1}")
limmerick_b = re.compile("[01]{2}1[0]{0,2}1")

a_parts: Dict[str, List[str]] = {}
b_parts: Dict[str, List[str]] = {}

def get_emph(pos_emphs):
    """Extract desired empahsis."""
    if len(pos_emphs) == 0:
        return None
        
    return pos_emphs[0]

with open("data/reviews.json") as inf:
    acount = 0
    bcount = 0
    # TODO: not right

    print("Gathering a and b lines...")
    while acount < MIN_A_COUNT and bcount < MIN_B_COUNT:
        if acount % 50 == 0:
            os.system("clear")
            print("condition is still true at " + str(time.time()))
            print("A LINES: " + str(acount))
            print("B Lines: " + str(bcount))
        line = inf.readline()
        review = json.loads(line)
        if review["stars"] > 2:
            continue

        text = TextBlob(review["text"])
        sents = text.sentences
        for sent in sents:
            words = sent.tokens
            allemphs = [p.stresses_for_word(w) for w in words]
            posemphs = [get_emph(e) for e in allemphs]
            emphs = "".join([pe for pe in posemphs if pe]).replace("2", "1")
            
            if acount < MIN_A_COUNT:
                a_matches = [match for match in limmerick_a.findall(emphs) if len(match) == len(emphs)]

                if a_matches:
                    a_parts[sent.raw] = []
                    acount += 1

            if bcount < MIN_B_COUNT:
                b_matches = [match for match in limmerick_b.findall(emphs) if len(match) == len(emphs)]

                if b_matches:
                    b_parts[sent.raw] = []
                    bcount += 1
                    

print("Linking up rhyming A phrases...")
# Link up rhyming pairs!
# Check A Parts
a_keys = list(a_parts.keys())
for i, a_line1 in enumerate(a_keys):
    atokes = TextBlob(a_line1).tokens
    if len(atokes) == 0:
        continue
    elif len(atokes) == 1:
        a_end = atokes[0]
    else:
        a_end = atokes[-2]
    
    arhymes = p.rhymes(a_end)

    for j in range(i, len(a_keys)):
        a_line2 = a_keys[j]
        tokes = TextBlob(a_line2).tokens
        if len(tokes) == 0:
            continue
        elif len(atokes) == 1:
            end = tokes[0]
        else:
            end = tokes[-2]
        
        if end in arhymes:
            a_parts[a_line1].append(a_line2)
            a_parts[a_line2].append(a_line1)
    
print("Linking up rhyming B phrases...")
# Check B Parts
b_lines = list(b_parts.keys())
for i, b_line1 in enumerate(b_lines):
    tokes = TextBlob(b_line1).tokens
    if len(tokes) == 0:
        continue
    elif len(atokes) == 1:
        end = tokes[0]
    else:
        end = tokes[-2]
    
    b_rhymes = p.rhymes(end)
    
    for j in range(i, len(b_lines)):
        b_line2 = b_lines[j]
        tokes = TextBlob(b_line2).tokens
        if len(tokes) == 0:
            continue
        elif len(atokes) == 1:
            end = tokes[0]
        else:
            end = tokes[-2]

        if end in b_rhymes:
            b_parts[b_line1].append(b_line2)
            b_parts[b_line2].append(b_line1)

# REMOVE:
# A parts with no A mates
# B parts with no B mates
print("Removing A phrases with no mates")
a_parts = {
    part: a_parts[part] for part in a_parts.keys() if len(a_parts[part]) > 0
}

print("Removing B phrases with no mates")
b_parts = {
    part: b_parts[part] for part in b_parts.keys() if len(b_parts[part]) > 0
}

final = {
    "a": a_parts,
    "b": b_parts,
}

with open("yelpoet/rhymes/limmerick_rhymes.json", "w") as outfile:
    json.dump(final, outfile)
