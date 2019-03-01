"""Write a 'roses are red' style poem."""

import json
import random

def roses_are_red():
    """Write a 'roses are red' style poem."""
    try:
        # TODO: Resolve paths in a better way
        infile = open('data/red_roses_rhymes.json', 'r')
    except Exception as e:
        print('Error opening roses json!', e)
        quit()
    
    try:
        rhymes = json.load(infile)
        infile.close()
    except:
        print('Invalid json!')
    
    choices = list(rhymes.keys())
    # TODO: Make sure these two don't rhyme
    line2, line3 = random.choice(choices), random.choice(choices)
    line4 = random.choice(list(rhymes[line2].keys()))

    return '\n'.join([
        'Roses are red.',
        line2,
        line3,
        line4
    ])

if __name__ == '__main__':
    print(roses_are_red())