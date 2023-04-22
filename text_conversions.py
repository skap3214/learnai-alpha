from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import json
import apikey as api
import streamlit as st

class Converter:
    '''
    converts to everything from text. To call a specific method, 
    the method name will be whateer you want to convert the text to.
    e.g:
    If you want to convert text to mcq, then you will call mcq() method.

    Supported text conversion methods:
    - mcq->json
    - chatbot
    '''
    API_KEY = st.secrets["OPENAI_API_KEY"]

    def __init__(self, text : str):
        '''
        Constructor which takes in text as input.
        :param text: text to be converted.
        :type text: str
        
        :Example:
        >>> text = "This is a sample text to be converted"
        >>> converter = Converter(text)
        >>> converter.mcq()
        >>> converter.chatbot()
        >>> converter.json()
        
        '''
        self.text = text
    
    def mcq(self):
        '''
        converts to mcq(in dictionary format)
        '''
        question = "Create a multiple choice question and answer sequence using the whole text as context. Create as many relevant questions as possible"
        convert_json = '''
        I will give you a series of Multiple Choice Questions, with their options and answers. I need to convert all of it to a json object. This is an example of how I want the json object to look like:
        {
            "1" : {
                "question": "q",
                "A": "answer a",
                "B": "answer b",
                "C": "answer c",
                "D": "answer d",
                "correct":"A/B/C/D"
                
            },
            "2" : {
                "question": "q",
                "A": "answer a",
                "B": "answer b",
                "C": "answer c",
                "D": "answer d",
                "correct":"A/B/C/D"
                
            }
        }
        Strictly output ONLY the json object.
        '''
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_text(self.text)

        embeddings = OpenAIEmbeddings(openai_api_key=self.API_KEY)
        docsearch = FAISS.from_texts(texts, embeddings)
        llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=self.API_KEY, temperature=0)

        chain = load_qa_chain(llm=llm, chain_type="stuff")
        docs = docsearch.similarity_search(question)
        result = chain.run(input_documents = docs, question = question)

                
        llm = OpenAI(temperature=0, openai_api_key=self.API_KEY, model_name="gpt-3.5-turbo")
        to_json = llm(convert_json+"\nThis is the result:\n"+result)
        output = json.loads(to_json.strip())
        return output
    
    def chatbot(self,question):
        '''
        converts to chatbot(Q/A)
        - does not retain context
        - you need to call chatbot everytime you want to ask a question
        '''
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_text(self.text)

        embeddings = OpenAIEmbeddings(openai_api_key=self.API_KEY)
        docsearch = FAISS.from_texts(texts, embeddings)
        llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=self.API_KEY)
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        docs = docsearch.similarity_search(question)
        result = chain.run(input_documents = docs, question = question)
        return result

    def code_question(self):
        '''
        converts text to a coding question
        '''
        pass
    
    def summary(self,as_list = False):
        '''
        converts text to a summary
        as_list: If you want each of the points in the summary as a list.

        #TODO: CONVERT SUMMARY TO LIST
        #TODO: CONVERT LIST TO A FORMATTED STRING FOR OUTPUT

        currently outputs a summary as a string in a python list format
        '''
        prompt = "Create a summary in a Python list format"
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_text(self.text)

        embeddings = OpenAIEmbeddings(openai_api_key=self.API_KEY)
        docsearch = FAISS.from_texts(texts, embeddings)
        llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=self.API_KEY)
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        docs = docsearch.similarity_search(prompt)
        result = chain.run(input_documents = docs, question = prompt)
        return result

    def cheat_sheet(self):
        '''
        converts text to cheat sheet
        '''
        pass