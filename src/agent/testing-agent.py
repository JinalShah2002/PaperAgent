"""

@author: Jinal Shah

In this file, I am testing the agent with various 
prompts.

"""
from dotenv import load_dotenv
import anthropic
import sys
from PyPDF2 import PdfReader

sys.path.append('../arxivAPI')
from arxivAPI import ArxivAPI

# Loading environment variables
load_dotenv()

# Getting the papers
arxiv_client = ArxivAPI()
papers = arxiv_client.get_papers("SVG AND (large language models)",max_results=2)
arxiv_client.download_papers(papers, dirpath='./papers')
ids = [paper.get_short_id() for paper in papers]
context_papers = []

def pdf_to_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''.join(page.extract_text() for page in reader.pages)
    return text

for id in ids:
    text = pdf_to_text(f"./papers/{id}.pdf")
    context_papers.append(text)

client = anthropic.Anthropic()

user_prompt = f"Research Question: How do large language models perform in generating SVGs?\n\nPaper:\n{context_papers[0]}"


message = client.messages.create(
    model='claude-3-5-sonnet-20240620',
    system="You are a researcher looking to provide your fellow colleagues with a literature review. Given the research question and papers, please "+
    "write a comprehensive literature review. Be sure to provide citations in APA format at the end of the review. Do not provide bullet points. Write paragraphs!",
    messages = [
        {
            'role':'user',
            "content":[
                {
                    'type':'text',
                    "text": user_prompt
                }
            ]
        }
    ],
    max_tokens=4096
)
print(message.content[0].text)
print()
message_2 = client.messages.create(
    model='claude-3-5-sonnet-20240620',
    system="You are a researcher looking to provide your fellow colleagues with a literature review. Given the research question and papers, please "+
    "write a comprehensive literature review. Be sure to provide citations in APA format at the end of the review. Do not provide bullet points. Write paragraphs!",
    messages = [
        {
            'role':'user',
            "content":[
                {
                    'type':'text',
                    "text": user_prompt
                }
            ]
        },
        {
            'role':'assistant',
            "content":[
                {
                    'type':'text',
                    "text": message.content[0].text
                }
            ]
        },
        {
            'role':'user',
            "content":[
                {
                    'type':'text',
                    "text": "Can you improve the review using the following paper as well:\n Paper:\n"+context_papers[1]
        }]
        }
    ],
    max_tokens=4096
)
print(message_2.content[0].text)