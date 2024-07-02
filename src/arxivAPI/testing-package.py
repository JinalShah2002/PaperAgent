"""

@author: Jinal Shah

In this script, I want to test
the arxiv package and figure out 
how to utilize it for my case.

"""
import arxiv 

client = arxiv.Client()

search = arxiv.Search(
    query = "SVG AND (large language models)",
    max_results = 5,
    sort_by = arxiv.SortCriterion.SubmittedDate
)

print(search)

results = client.results(search)

for r in results:
    r.download_pdf(dirpath='./test-downloads',filename=f"{r.title}.pdf")