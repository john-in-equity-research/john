import unicodedata
import re

def clean_person(name: str):
    """

        Works for both, first/last and full name !

         (clean_name("L.")              # → None
         (clean_name("L")               # → None
         clean_name("M.")               # → None
         clean_name("John M. Doe")      # → "John M. Doe"
         clean_name("Dr. L.")           # → "Dr. L." (still includes invalid, but not exact match)
         clean_name("Qi")               # → "Qi" (Shortest valid name is len == 2) !

    """

    if not name:
        return None

    # Normalize Unicode
    name = unicodedata.normalize('NFKC', name)

    # Remove disallowed characters (keep letters, space, apostrophe, hyphen, period)
    allowed = re.compile(r"[^a-zA-Z\s.'-]")
    name = allowed.sub('', name)

    # Collapse multiple spaces and trim
    name = re.sub(r'\s+', ' ', name).strip()

    # Reject if name is just an initial (like "J", "L.", "X", etc.)
    if re.fullmatch(r"[A-Z]\.?", name):  # matches "J" or "J."
        return None

    return name


def identify_speaker(speaker_full_name: str):
    """

      e.g. "Jones Jona L." (SEC) became {first_name: Jona, last_name: Jones} and full_name : Jones Jona L.
      and FMP e.g. reports "Jones Jona" => Searching full_name won't match !
      => That's why we are able to search a combination of first_name + last_name to retrieve the person instead

    """

    try:
        names = speaker_full_name.split(" ")
        last_name = clean_person(names[0].lower().title())
        first_name = clean_person(names[-1].lower().title())

        if not first_name:
            # e.g. Jolla Alice L. -> Last name Jolla, First name Alice, L. dropped and only be shown under full name
            first_name = clean_person(names[1].lower().title())

    except (IndexError, AttributeError) as rep:
        print(rep)
        first_name = last_name = None

    return {
        "first_name": first_name,
        "last_name": last_name,
        "full_name": speaker_full_name,
    }


# requires: en_core_md (see machine_learning.py)

from .machine_learning import nlp

def identify_person_company_relation(
        pre_chunk: str, keep_rest=False
):
    """
    
     Identifies the company of an equity analysis by it's introductive pre chunk. 
     Also returns the other ents, if wanted:

    """
    doc = nlp(pre_chunk)
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    
    if keep_rest:
        return orgs, doc.ents
        
    return orgs
    
