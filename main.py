"""One Word, First Thought — make.fun entry.

The competition asks for exactly one word: the first word that comes to
mind, nothing else. The judge compares words two at a time on surprise,
vividness and a spark of wit, and the most interesting word wins.

This program scores ten fresh candidate words on five criteria
(original, interesting to the judge, on-theme as a first thought,
exact RULES format, natural English), picks the best, validates it
against the gate (UTF-8 text, 1-24 characters, exactly one word, not
only whitespace) and writes it to /output/entry.txt.
"""

import os

# Ten candidates, each scored 1-10 on five criteria:
# (original, interesting, on-theme, exact format, natural English)
CANDIDATES = [
    ("petrichor",      7, 9, 10, 10, 10),
    ("defenestration", 9, 10, 10, 10, 10),
    ("psithurism",     10, 8, 10, 10, 9),
    ("vellichor",      9, 9, 10, 10, 9),
    ("sonder",         8, 9, 10, 10, 9),
    ("apricity",       9, 8, 10, 10, 10),
    ("kerfuffle",      8, 8, 10, 10, 10),
    ("gloaming",       8, 8, 10, 10, 10),
    ("limerence",      8, 8, 10, 10, 10),
    ("quixotic",       7, 8, 10, 10, 10),
]

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 24


def score(candidate):
    """Total score of a candidate tuple (word, s1..s5)."""
    return sum(candidate[1:])


def validate_word(word):
    """Enforce the competition gate before writing anything.

    RULES.txt gate: /output/entry.txt must be UTF-8 text of 1 to 24
    characters, not only white space, and the task demands exactly one
    word. Anything failing here aborts instead of writing a bad entry.
    """
    if not isinstance(word, str):
        raise ValueError("entry is not text")
    word.encode("utf-8")  # raises if not valid UTF-8 text
    if not (GATE_MIN_CHARS <= len(word) <= GATE_MAX_CHARS):
        raise ValueError("entry is %d chars, gate needs 1-24" % len(word))
    if not word.strip():
        raise ValueError("entry is only white space")
    if len(word.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if not word.isalpha():
        raise ValueError("entry must be letters only")
    return word


def pick_winner(candidates):
    """Highest total; ties break toward the shorter word, then earliest."""
    ranked = sorted(candidates, key=lambda c: (-score(c), len(c[0])))
    return ranked[0], ranked


def main():
    winner, ranked = pick_winner(CANDIDATES)
    word = validate_word(winner[0])
    print("Candidates (word: total/50):")
    for entry in ranked:
        print("  %s: %d" % (entry[0], score(entry)))
    print("Winner: %s (%d/50)" % (word, score(winner)))
    out_path = "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(word)
    print("Wrote %s (%d chars)" % (out_path, len(word)))


if __name__ == "__main__":
    main()
