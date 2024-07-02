"""

@author: Jinal Shah

A module to get papers for search queries

"""
import os
import arxiv 

class ArxivAPI:
    def __init__(self):
        self.client = arxiv.Client()
    
    # Function to get papers
    def get_papers(self, query, max_results=20, sort_by=arxiv.SortCriterion.Relevance):
        search = arxiv.Search(
            query = query,
            max_results = max_results,
            sort_by = sort_by
        )
        results = self.client.results(search)
        return results
    
    # Function to download papers
    def download_papers(self, results, dirpath='../papers'):
        # Making the directory if it doesn't exist
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        for r in results:
            r.download_pdf(dirpath=dirpath,filename=f"{r.title}.pdf")