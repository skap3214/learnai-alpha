from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import json
import streamlit as st
from text_grabber import Text
class Converter:
    '''
    Supported text conversion methods:
    - mcq->json
    - chatbot
    '''
    API_KEY = st.secrets["OPENAI_API_KEY"]

    def __init__(self, text : str):
        '''
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
        self.llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=self.API_KEY, temperature=0)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.API_KEY)
        self.chain = load_qa_chain(llm=self.llm, chain_type="stuff")
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def _process_text(self, question: str, prompt: str):
        texts = self.text_splitter.split_text(self.text)
        docsearch = FAISS.from_texts(texts, self.embeddings)
        docs = docsearch.similarity_search(question)
        return self.chain.run(input_documents=docs, question=question)

    def mcq(self):
        question = "Create a multiple choice question and answer sequence using the whole text as context. Create as many relevant questions as possible"
        result = self._process_text(question, '')

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

        to_json = eval(self.llm(convert_json + "\nThis is the result:\n" + result))
        json_object = json.dumps(to_json) 
        # output = json.loads(to_json.strip())
        with open("mcq.json", "w") as outfile:
            outfile.write(json_object)
        # return output

    def chatbot(self, question):
        result = self._process_text(question, '')

        return result
    
    def summary(self, as_list=False):
        prompt = "Create a summary in a Python list format"
        result = self._process_text(prompt, '')

        return result

    def cheat_sheet(self):
        prompt = "Create a cheat sheet"
        result = self._process_text(prompt, '')

        return result
    
    def generate_code(self, youtube_url):
        to_text = Text()
        transcript = to_text.youtube(youtube_url)
        self.text = transcript
        question = "Create a code prompt and correct code answer using the whole text as context"
        result = self._process_text(question, '')

        convert_json = '''
        I will give you a code prompt and correct code answer, with their prompt and answer. I need to convert it to a json object. This is an example of how I want the json object to look like:
        {
            "prompt": "Write a range of 1,2,3,4,5 and the print the range out",
            "answer": "my_range = range(1,6) 
            print(my_range)"
        }
        Strictly output ONLY the json object.
        '''

        to_json = self.llm(convert_json + "\nThis is the result:\n" + result)
        output = json.loads(to_json.strip())
        return output

