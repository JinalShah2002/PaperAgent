# PaperAgent

PaperAgent is an AI assistant that enables a user to generate literature reviews given a research question or problem. 

## Problem
Research drives innovation. As a result, millions of people around the globe are involved in research & development (R&D) work ,and thousands of papers are being published daily. With this much knowledge out there, it can become overwhelming for an individual to figure what papers are relevant to their line of work. In comes PaperAgent: an AI assistant tasked to provide you with a comprehensive literature review. This literature review can be utilized to form a foundation for your R&D work. It allows you to understand your research question thoroughly as well as understand what related work has been done. The goal of PaperAgent is to accelerate R&D work by minimizing the time individuals take to thoroughly go through research papers to understand their problem.

## Use Cases
PaperAgent is meant for the following use cases: 

1. To generate a literature review that can serve as an entry point into a research field or research topic.
2. To allow a user to understand "what's out there" in relation to their research question/topic.

PaperAgent is NOT meant for the following use case:

1. It is NOT meant to be a means to replace the act of writing a literature review. Literature reviews are critical for research papers. While PaperAgent generates literature reviews, it may lack the complexity that high quality literature reviews contain. Furthermore, it is important to be aware of the fact that PaperAgent may hallunicate. As PaperAgent is a system built using large language models (LLMs), this risk is important to be aware of. With this in mind, you should use PaperAgent as a "liftoff" point as you immerse yourself into your research area. 

## How to use PaperAgent
To use PaperAgent, please follow the following procedure:

1. Clone the repository. I would highly suggest you create a virtual environment for the project; however, that is not necessary.
2. Navigate to the project folder and install dependencies:
```
poetry install
```
3. Navigate to the src folder and create a .env file. Your .env file should have the following:
```
ANTHROPIC_API_KEY='YOUR API KEY'
OPENAI_API_KEY='YOUR API KEY'
OPENAI_ORG_ID='YOUR ORG ID'
PINECONE_API_KEY='YOUR API KEY'
```
4. Once you have all that set-up, you can choose 1 of 2 ways to run the application: 1) you can run main.py to interact with the project in terminal or 2) you can run app.py to interact with the project via a web user interface. Here are the instructions for each:

To interact with the project in terminal, navigate into the src folder and run the following command: 
```
poetry run python3 main.py
```

To interact with the project via a web user interface, navigate into the src folder and run the following command:
```
poetry run streamlit run app.py
```

Now you are all set! You can start generating literature reviews!

## Flow Diagram
``````mermaid
graph TD
    A[User] --> B[Research Question]
    B --> C[KeyBert]
    C -->|Top 5 key words/phrases| E[Search]
    E -->|Top 5 papers for every key word/phrase| F[Download]
    B -->|Querying vector store| G[Pinecone Vector Database]
    G -->|Top 10 chunks| H[Claude 3.5]
    B --> H
    H --> I[Literature Review]
    F --> K[Convert PDFs to strings]
    K --> L[Split document strings into chunks]
    L --> M[text-embedding-3-large model]
    M --> G

