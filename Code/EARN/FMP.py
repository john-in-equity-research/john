import requests

def clean_earnings_calls_for_year(ticker, year, key):
    url = f"https://financialmodelingprep.com/api/v4/batch_earning_call_transcript/{ticker}?year={year}&apikey={key}"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if not data:
        print(f"Failure; No data for: {ticker}, {year}")
        return False

    return [
        clean_earnings_call(d, year=year, ticker=ticker) for d in data
    ]


def clean_earnings_call(data, **kwargs):
    date = data["date"]
    quarter = data["quarter"]
    transcript = data["content"]

    transcript_cleaned = []

    for i, c in enumerate(transcript.split("\n")):

        split_two = c.split(":")
        speaker = split_two[0]
        merged = "".join(split_two[1:])

        transcript_cleaned.append(
            {
                "speaker": speaker,
                "text": merged.replace("’", "'").strip(" ")
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
