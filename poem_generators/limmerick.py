"""Generate limmericks."""
import random
import json

def generate_limmerick():
    with open("data/limmerick_rhymes.json", "r") as infile:
        rhymes = json.load(infile)

    a_parts = rhymes["a"]
    b_parts = rhymes["b"]

    a = random.choice(list(a_parts.keys()))
    b = random.choice(a_parts[a])
    c = random.choice(list(b_parts.keys()))
    d = random.choice(b_parts[c])
    e = random.choice(a_parts[b])

    poem = "\n".join([
        a,
        b,
        c,
        d,
        e,
    ])

    return poem

if __name__ == "__main__":
    print(generate_limmerick())