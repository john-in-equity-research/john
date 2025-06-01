import requests
from .NER import *
from .speaker import *

def clean_earnings_calls_for_year(ticker, year, known_speakers, key):
    url = f"https://financialmodelingprep.com/api/v4/batch_earning_call_transcript/{ticker}?year={year}&apikey={key}"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if not data:
        print(f"Failure; No data for: {ticker}, {year}")
        return False

    return [
        clean_earnings_call(d, year=year, ticker=ticker, known_speakers=known_speakers) for d in data
    ]


def NER_makes_sense(id_speaker: dict, known_speakers: list):
    """

     known_speakers: List of known C-levels (e.g. CEO;CFO;VP of IR;Other Exec. e.g. CTO)
     id_speaker: {full,last,first name}
     
     we must rethink this func here tbh.

    """

    return id_speaker["full_name"].upper() == "OPERATOR"


def clean_earnings_call(data, **kwargs):
    date = data["date"]
    known_speakers = kwargs.get("known_speakers")
    quarter = data["quarter"]
    transcript = data["content"].split("\n")
    transcript_cleaned = []

    identified_entities_speaker_org = {}

    org_default = kwargs["ticker"]

    for i, c in enumerate(transcript):

        chunk = c.split(":")
        speaker = chunk[0]
        passages = "".join(chunk[1:])
        id_speaker = identify_speaker(speaker)

        # used to identify analysts and non other non C-levels
        prev_chunk = transcript[i - 1].split(":")
        prev_speaker = prev_chunk[0]
        prev_passages = "".join(prev_chunk[1:])
        prev_id_speaker = identify_speaker(prev_speaker)

        # see if the prev speaker introduced the current person
        if NER_makes_sense(prev_id_speaker, known_speakers):
            identified_entities_speaker_org[id_speaker["full_name"]] = identified_entities_speaker_org.get(
                id_speaker["full_name"],
                identify_person_company_relation(prev_passages)
            )

        transcript_cleaned.append(
            {
                "text": passages.replace("’", "'").strip(" "),
                "person": id_speaker,
                "orgs": identified_entities_speaker_org.get(id_speaker["full_name"], org_default),
            }
        )

    return {
        "date": date,
        "quarter": quarter,
        "ticker": kwargs["ticker"],
        "year": kwargs["year"],
        "frame": f"{kwargs['year']}Q{quarter}",
        "transcript": transcript_cleaned
    }
