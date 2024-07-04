"""

@author: Jinal Shah

This file is a tutorial for LangChain.
Just meant to get my hands dirty with LangChain.

Tutorial Video: https://www.youtube.com/watch?v=aywZrzNaKjs
"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore

# Loading environment
load_dotenv()

# Loading model
model = ChatOpenAI(
    model='gpt-4o',
    temperature=0.7,
    max_tokens=4096
)

messages = [
    (
        "system",
        'You are an expert data scientist'
    ),
    ('human','Write a Python script that trains a neural network on simulated data')
]

# Prompt Templates -> Setting a template for the prompt and allowing the user to dynamically change it 
# based on the user's input
template = """
You are an expert data scientist with an expertise in building deep learning models.
Explain the concept of {concept} in a couple of lines.
"""
prompt = PromptTemplate(
    input_variables=['concept'],
    template=template
)

# print(model.invoke(prompt.format(concept='regularization')).content)
# print()
# print(prompt.invoke({'concept':'regularization'}))

# Chain -> chains the components of the application together
# I.e chain the prompt and the model together such that you just have 
# to run the chain (think of it like the pipeline in scikit-learn)

chain = prompt | model | StrOutputParser() # pipe function langchain, piping the output to the next module
# print(chain.invoke('autoencoder').content)
# print()

second_prompt = """
Turn the concept description of {ml_concept} and explain it to me like I'm five in 500 words"
"""
second_template = PromptTemplate(
    input_variables=['ml_concept'],
    template=second_prompt
)
chain_two = second_template | model | StrOutputParser()
overall_chain = chain | chain_two
explanation = overall_chain.invoke('autoencoder')
# print()

# Embeddings & VectorStores
# Chunking the documents recursively -> first split by the first splitter, if the split is >= len, recursively split the split until 
# split is smaller than len. 
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
)
texts = text_splitter.create_documents([explanation])
# print(texts)
# print()
# print(texts[0].page_content)
# print()

# Getting the embeddings using OpenAI's embedding model
embedding_model = OpenAIEmbeddings(model='text-embedding-3-large')
texts_str = [text.page_content for text in texts]
embeddings = embedding_model.embed_documents(texts_str)
# print(len(embeddings[1])) # How big the embedding is

# Putting the vectors into Pinecone
search = PineconeVectorStore.from_documents(
    documents=texts,
    embedding=embedding_model,
    index_name='langchain-tutorial'
)
# print(len(embeddings))
# print(len(embeddings[0]))
# print(len(texts_str))
# print(texts_str[:2])
print(search.similarity_search("What is magical about an autoencoder?"))
print()






