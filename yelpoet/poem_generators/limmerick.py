"""Generate limmericks."""
import random
import json

def limmerick():
    with open("yelpoet/rhymes/limmerick_rhymes.json", "r") as infile:
        rhymes = json.load(infile)

    a_parts = rhymes["a"]
    b_parts = rhymes["b"]

    a = random.choice(list(a_parts.keys()))
    b = random.choice(a_parts[a])
    c = random.choice(list(b_parts.keys()))
    d = random.choice(b_parts[c])
    while True:
        e = random.choice(a_parts[b])
        if e != a:
            break

    poem = "\n".join([
        a,
        b,
        c,
        d,
        e,
    ])

    return poem

if __name__ == "__main__":
    print(limmerick())