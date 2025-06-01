import spacy
from spacy.language import Language
import re

# place for NLP tasks, namely NER at the moment

# you'd need to download en_core_web_md in the first place (Very lightweight, ~50MB)
nlp = spacy.load("en_core_web_md")

@Language.component("with_org_component")
def add_with_org_entities(doc):
  
    # Find all matches of 'with X'
    matches = re.finditer(r"\bwith\s+([A-Z][a-zA-Z0-9&\-.]+)", doc.text)

    new_spans = []
    for match in matches:
        start_char = match.start(1)
        end_char = match.end(1)

        # Try to get a valid span with alignment fallback
        span = doc.char_span(start_char, end_char, label="ORG", alignment_mode="contract")
        if span:
            # Avoid overlaps
            if not any(span.start < ent.end and span.end > ent.start for ent in doc.ents):
                new_spans.append(span)

    # Set the new entities
    doc.ents = list(doc.ents) + new_spans
    return doc


# Add it after the default NER pipe
nlp.add_pipe("with_org_component", after="ner")

# now matching => Introducing "Person ABC" with "Company: e.g. Stiffer" => Stiffer
# normal en_core_md failed to do so
