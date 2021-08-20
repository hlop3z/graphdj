"""English Word(s) Pluralization"""

import re

from setup import plurals

PLURAL_NOUNS = {
    "aircraft": "aircraft",
    "alumna": "alumnae",
    "analysis": "analyses",
    "apex": "apices",
    "bison": "bison",
    "cactus": "cacti",
    "child": "children",
    "codex": "codices",
    "crisis": "crises",
    "criterion": "criteria",
    "curriculum": "curricula",
    "datum": "data",
    "diagnosis": "diagnoses",
    "ellipsis": "ellipses",
    "erratum": "errata",
    "fish": "fish",
    "focus": "foci",
    "foot": "feet",
    "genus": "genera",
    "goose": "geese",
    "index": "indices",
    "larva": "larvae",
    "louse": "lice",
    "man": "men",
    "means": "means",
    "mouse": "mice",
    "oasis": "oases",
    "ox": "oxen",
    "person": "people",
    "quiz": "quizzes",
    "series": "series",
    "sheep": "sheep",
    "species": "species",
    "swine": "swine",
    "tooth": "teeth",
    "trout": "trout",
    "tuna": "tuna",
    "vita": "vitae",
    "woman": "women",
}

# Get Custom Plurals
try:
    PLURAL_NOUNS.update(plurals.NOUNS)
except:
    pass


# Pluralize
def pluralize(word: str) -> str:
    """Singular to Plural"""
    noun = word.lower()
    output = ""
    if noun in PLURAL_NOUNS.keys():
        output = PLURAL_NOUNS[noun]
    elif re.search(r"[f][e]$", noun):
        output = re.sub("fe$", "ves", noun)
    elif re.search(r"[f]$", noun):
        output = re.sub("f$", "ves", noun)
    elif re.search(r"[sxz]$", noun) or re.search(r"[^aeioudgkprt]h$", noun):
        output = re.sub(r"$", "es", noun)
    elif re.search(r"[bcdfghjklmnpqrstvxz][y]$", noun):
        output = re.sub(r"y$", "ies", noun)
    else:
        output = noun + "s"
    return output
