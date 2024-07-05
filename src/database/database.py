"""

@author: Jinal Shah

This class is responsible for 
interacting with the Pinecone database.

"""
from dotenv import load_dotenv
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone.vectorstores import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os
from PyPDF2 import PdfReader

load_dotenv()

class PineconeDatabase:
    def __init__(self):
        self.pinecone = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
        self.index_name = 'papers'
        self.embedding_model = OpenAIEmbeddings(model='text-embedding-3-large')
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100,length_function=len)
        self.db = None

    # Function to create the index
    def create_index(self):
        if not self.check_index_exists():
            self.pinecone.create_index(
                name=self.index_name,
                dimension=3072,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
    
    # Function to delete the index
    def delete_index(self):
        if self.check_index_exists():
            self.pinecone.delete_index(name=self.index_name)
    
    # Function to check if index exists
    def check_index_exists(self):
        existing_indexes = [index_info['name'] for index_info in self.pinecone.list_indexes()]

        return self.index_name in existing_indexes
    
    # Putting the pdfs into the Pinecone database
    def put_pdfs(self,paths,papers):
        # Creating the index
        self.create_index()

        # Putting the papers into the Pinecone database
        pdf_string = []
        meta_datas = []
        for index in range(len(paths)):
            # Extract the text
            reader = PdfReader(paths[index])
            string_text = ''.join([page.extract_text() for page in reader.pages])
            meta_data = {
                'id':papers[index].get_short_id(),
                'title':papers[index].title,
                'authors':[],
                'doi':"",
                'journal_ref':"",
                'date':papers[index].published.strftime('%m-%d-%Y')
            }
            authors_list = [author.name for author in papers[index].authors]
            meta_data['authors'] = authors_list

            if papers[index].doi:
                meta_data['doi'] = papers[index].doi
            if papers[index].journal_ref:
                meta_data['journal_ref'] = papers[index].journal_ref

            pdf_string.append(string_text)
            meta_datas.append(meta_data)
        chunks = self.text_splitter.create_documents(pdf_string,meta_datas)

        # Putting chunk in database
        self.db = PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            index_name=self.index_name
        )
    
    # A function to get the similar chunks
    def get_similar_chunks(self,query):
        if self.db:
            return self.db.similarity_search(query,k=10)
        else:
            return None






