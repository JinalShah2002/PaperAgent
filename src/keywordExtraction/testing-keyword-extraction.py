"""

@author: Jinal Shah

This file will be used to test 
keyword extraction

"""
from keybert import KeyBERT

# Testing the keyword extraction
document = 'Can large language models be used to generate SVG? If so, how?'

# Defining the model
model = KeyBERT()
keywords = model.extract_keywords(document, keyphrase_ngram_range=(1,3),stop_words=None,top_n=5)
print(keywords)