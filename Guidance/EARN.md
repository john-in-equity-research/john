**EARN**

EARN deals with tasks related to earnings call transcripts.

Current highlights:

- Speaker-Passage chunks
- Recognizing the company of analysts
- Flexible person representation 

Example:

... meta data, previous chunks ...

"The next question comes from the line of **Brad Sills** with **Bank of America**. Please proceed."

=> 'orgs': ['Bank of America']

=>  'person': {'first_name': 'Sills',
               'full_name': 'Bradley Sills',
               'full_name_2': 'Sills Bradley',
               'last_name': 'Bradley'},

=> 'text': "Wonderful. Thanks so much. Very impressive to see 
            the Office 365 commercial seat growth hanging in 
            here in that double digit range. It's very 
            impressive just given the scale of that business. 
            We think of Office as having such a dominant market 
            position. Curious, how you think about the -- where 
            that seat is coming from and how many more of those 
            seats are out there to go get?"

... other chunks ...

