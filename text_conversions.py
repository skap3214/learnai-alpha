from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
class Converter:
    '''
    converts to everything from text. To call a specific method, 
    the method name will be whateer you want to convert the text to.
    e.g:
    If you want to convert text to mcq, then you will call mcq() method.
    '''
    def __init__(self,text):
        self.text = text
    
    def mcq(self):
        '''
        converts to mcq(in dictionary format)
        '''
        pass
    
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

        embeddings = OpenAIEmbeddings(openai_api_key="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")
        docsearch = FAISS.from_texts(texts, embeddings)
        llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        docs = docsearch.similarity_search(question)
        result = chain.run(input_documents = docs, question = question)
        return result

    def code_question(self):
        '''
        converts text to a coding question
        '''
        pass
    
    def summary(self):
        '''
        converts text to a summary
        '''
        pass

    def cheat_sheet(self):
        '''
        converts text to cheat sheet
        '''
        pass