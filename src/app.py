"""

@author: Jinal Shah

Front-end

"""
import streamlit as st
from keybert import KeyBERT
from arxivAPI.arxivAPI import ArxivAPI
from database.database import PineconeDatabase
from agent.agent import Agent
import shutil

st.markdown("<h1 style='text-align: center;'>PaperAgent</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Generate high-quality literature reviews</h2>", unsafe_allow_html=True)

# Defining states
if "extractor" not in st.session_state:
    st.session_state.extractor = KeyBERT()
if "arxiv" not in st.session_state:
    st.session_state.arxiv = ArxivAPI()
if "pinecone" not in st.session_state:
    st.session_state.pinecone = PineconeDatabase()
if "agent" not in st.session_state:
    st.session_state.agent = None
if "question" not in st.session_state:
    st.session_state.question = ""
if 'review' not in st.session_state:
    st.session_state.review = ""
if 'feedback' not in st.session_state:
    st.session_state.feedback = False

# Keyword extraction
def extract_keywords(query):
    return [pair[0] for pair in st.session_state.extractor.extract_keywords(query, keyphrase_ngram_range=(1,3),stop_words=None,top_n=5)]

# Search for papers
def paper_search(keywords):
    papers = []
    for keyword in keywords:
        papers.extend(st.session_state.arxiv.get_papers(query=keyword,max_results=5))
    return papers

# Download papers
def download_papers(papers):
    st.session_state.arxiv.download_papers(papers)

# Put papers into Pinecone database
def put_papers_into_db(papers):
    paths = []
    for paper in papers:
        paths.append(f'./papers/{paper.get_short_id()}.pdf')
    st.session_state.pinecone.put_pdfs(paths,papers)

# Get relevant chunks
def get_relevant_chunks(query):
    return st.session_state.pinecone.get_similar_chunks(query)

# Generate literature review
def generate_literature_review(query, relevant_chunks):
    st.session_state.agent = Agent(query,relevant_chunks)
    return st.session_state.agent.generate_literature_review()

def update_review(feedback):
    st.session_state.review = st.session_state.agent.generate_literature_review(feedback)

def reset_app():
    st.session_state.question = ""
    st.session_state.review = ""
    st.session_state.agent = None

    # Deleting the papers and the Pinecone Index
    shutil.rmtree('./papers')
    st.session_state.pinecone.delete_index()

def process_feedback(feedback):
    with st.spinner("Updating review based on feedback..."):
        update_review(feedback)
    st.session_state.feedback = False

def process_question(question):
    st.session_state.question = question
    placeholder = st.empty()
    with placeholder.container():
        with st.spinner("Processing your research question..."):
            st.info("Extracting keywords...")
            keywords = extract_keywords(st.session_state.question)
            st.info("Performing search...")
            papers = paper_search(keywords)
            st.info("Downloading papers...")
            download_papers(papers)
            st.info("Putting papers into Pinecone...")
            put_papers_into_db(papers)
            st.info("Getting relevant chunks...")
            relevant_chunks = get_relevant_chunks(st.session_state.question)
            st.info("Generating literature review...")
            review = generate_literature_review(st.session_state.question, relevant_chunks)
            st.session_state.review = review
            st.success("Literature review generated!")
    placeholder.empty()

# Main UI
if st.session_state.question == "":
    question = st.text_input("Enter your research question:")
    st.button('Submit Question',on_click=process_question,args=[question])
else:
    st.write(f"<b>Research Question:</b> {st.session_state.question}", unsafe_allow_html=True)

if st.session_state.review != "":
    st.write("<b>Literature Review:</b>", unsafe_allow_html=True)
    st.write(st.session_state.review)

if not st.session_state.question == "" and not st.session_state.feedback:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button('Generate New Review', on_click=reset_app)
    with col2:
        st.download_button('Download Review', data=st.session_state.review, file_name='review.txt', mime='text/plain')
    with col3:
        st.button('Provide Feedback', on_click=lambda: st.session_state.update({'feedback': True}))

if st.session_state.feedback:
    feedback = st.text_area("Enter your feedback:")
    st.button('Submit Feedback',on_click=process_feedback,args=[feedback])
    