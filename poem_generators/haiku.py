"""Generate haikus."""

import json
import random

def generate_haiku() -> str:
    """Generate a haiku."""
    try:
        infile = open('data/haiku_rhymes.json')
    except Exception as e:
        print("Promblem opening haiku json", e)
        quit()
    

    try:
        rhymes = json.load(infile)
    except Exception as e:
        print("Problem parsing haiku json", e)
        quit()

    a = random.choice(rhymes['fives'])
    b = random.choice(rhymes['sevens'])
    c = random.choice(rhymes['fives'])

    return '\n'.join([a, b, c])
    
if __name__ == '__main__':
    print(generate_haiku())