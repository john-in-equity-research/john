
def ninja_split_earnings_call(ticker, y, q, key):
    """

     Using free account for 2024/25 transcripts, bypasses the transcript_split by handling it manually,

    """


    url = f"https://api.api-ninjas.com/v1/earningstranscript?ticker={ticker}&year={y}&quarter={q}"
    response = requests.get(url, headers={"X-Api-Key": key})
    response.raise_for_status()
    data = response.json()

    if not data:
        print(f"Failure; No data for: {ticker}, {y}, {q}")
        return False

    date = data["date"]
    transcript = data["transcript"]
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

    return transcript_cleaned
  
