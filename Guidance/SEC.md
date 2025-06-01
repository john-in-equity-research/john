**Notes while working with SEC data**

It might be helpful to start with a requests wrapper, as the SEC otherwise blocks you quickly.

=> Therefore, I've created the Response class inside Guidance/sec.py


Now you can get 10 responses/second, without a block.

=> For JSON: Request("https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json").fetch()

=> For HTM: Request("https://www.sec.gov/Archives/edgar/data/789019/000095017023035122/msft-20230630.htm").fetch(as_json=False)

=> For XML: Request("https://www.sec.gov/Archives/edgar/data/789019/000118368112000024/xslF345X02/edgar.xml").fetch(as_json=False, block_XML=False)


My tip: Don't use proxies. If you think there is a need, you most likely skipped the thinking part and went quick & dirty

=> Hosting SEC documents on AWS S3 can be far more efficient than expected

=> With the help of the **datamule** package you are able to compress the html content into a structured format

=> 200 KB on AWS per 10-Q instead of 9 MB per 10-Q on SEC sounds good.

=> I'll upload the code from John.AI soon, so that you see how it works.
