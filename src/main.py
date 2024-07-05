"""

@author: Jinal Shah


This file integrates all modules together
and runs the application.

"""
from arxivAPI.arxivAPI import ArxivAPI
from database.database import PineconeDatabase
from agent.agent import Agent
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

# Getting the relevant chunks
print('Getting relevant chunks...')
relevant_chunks = pinecone_db.get_similar_chunks(query)
print('Got relevant chunks')
print()

# Getting the literature review
print('Feeding all information to agent and getting the review...')
agent = Agent(query,relevant_chunks)
review = agent.generate_literature_review()
print(review)

review_satisfaction = input('Are you satisfied with the review? (y/n)\n')
while review_satisfaction == 'n':
    feedback = input('Please provide feedback:\n')
    review = agent.generate_literature_review(feedback)
    print(review)
    review_satisfaction = input('Are you satisfied with the review? (y/n)\n')
print('Saving the review...')
with open('review.txt','w') as f:
    f.write(review)
print('Saved the review')
print()

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