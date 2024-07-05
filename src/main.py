"""

@author: Jinal Shah


This file integrates all modules together
and runs the application.

"""
from arxivAPI.arxivAPI import ArxivAPI
from database.database import PineconeDatabase
from dotenv import load_dotenv
import shutil

# Loading environment
load_dotenv()

query = input('Enter your research question or research area:\n')

# Getting the papers 
print('Getting papers...')
print()

"""

TODO: Build Keyword Extractor (using KeyBert)

"""
keywords = ["SVG AND (large language models)"]
arxiv = ArxivAPI()
papers = []
for keyword in keywords:
    papers.extend(arxiv.get_papers(query=keyword,max_results=5))

print(f'Found total {len(papers)} papers')
print()

# Downloading the papers
print('Downloading papers...')
arxiv.download_papers(papers)
print('Downloaded all papers')
print()

# Putting the papers into the Pinecone database
print('Putting papers into Pinecone database...')
pinecone_db = PineconeDatabase()
paths = []
for paper in papers:
    paths.append(f'./papers/{paper.get_short_id()}.pdf')
pinecone_db.put_pdfs(paths,papers)
print('Put all papers into Pinecone database')
print()

"""

TODO: Build module to take in research question & relevant chunks
from Pinecone and return a literature review (Claude 3.5, Pinecone, Langchain)

"""

# Deleting the papers if needed
paper_deletion = input('Do you want to delete the papers? (y/n)\n')
if paper_deletion == 'y':
    shutil.rmtree('papers')
    print('Deleted all papers')
    print()

# Deleting the index if needed
index_deletion = input('Do you want to delete the Pinecone index? (y/n)\n')
if index_deletion == 'y':
    pinecone_db.delete_index()
    print('Deleted the Pinecone index')
    print()