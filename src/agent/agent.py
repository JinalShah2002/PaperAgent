"""

@author: Jinal Shah

This class is for the agent

"""
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers.string import StrOutputParser

load_dotenv()

class Agent:
    def __init__(self,research_question,excerpts,max_tokens=4096,temperature=0.7) -> None:
        self.research_question = research_question
        self.context = ''

        # Iterate through excerpts
        for excerpt in excerpts:
            self.context += f'Excerpt:{excerpt.page_content}\n'
            meta_data = excerpt.metadata
            self.context += f'Title: {meta_data["title"]}\n'
            self.context += f"Authors: {''.join(meta_data['authors'])}\n"
            self.context += f"DOI: {meta_data['doi']}\n"
            self.context += f"Journal Reference: {meta_data['journal_ref']}\n"
            self.context += f"Date: {meta_data['date']}\n\n"

        self.messages = ChatPromptTemplate.from_messages([
            ('system','You are an expert researcher looking to provide your colleagues with an elaborate literature review.'+
             'Given the research question and excerpts, please write a comprehensive literature review.'+ 
             'Be sure to provide citations in APA format at the end of the review and write full paragraphs!'),
            ('human', 'Research Question: {research_question}\n\nExcerpts:\n{context}'),
            MessagesPlaceholder('history'),
        ])

        # Creating the model instance
        self.model = ChatAnthropic(
            model='claude-3-5-sonnet-20240620',
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Starting chain
        self.start_chain = self.messages | self.model | StrOutputParser()

        # Creating a message history
        self.history = []
    
    # Function to generate the literature review
    def generate_literature_review(self,feedback=None):
        if feedback == None:
            agent_response = self.start_chain.invoke({'research_question':self.research_question,'context':self.context,'history':self.history})
            self.history.extend([
                ('ai',agent_response)
            ])
        else:
            self.history.extend([
                ('human',feedback)
            ])
            agent_response = self.start_chain.invoke({'research_question':self.research_question,'context':self.context,'history':self.history})
            self.history.extend([
                ('ai',agent_response)
            ])
        return agent_response

