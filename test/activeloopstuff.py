from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.document_loaders import UnstructuredFileLoader

from langchain.chains.summarize import load_summarize_chain
import os
os.environ['OPENAI_API_KEY'] = "OPENAI_API_KEY"
os.environ['ACTIVELOOP_TOKEN'] = "ACTIVELOOP_TOKEN"

OPENAI_API_KEY  = os.environ['OPENAI_API_KEY']
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

sm_loader = UnstructuredFileLoader("test/docs/tpt.txt")
sm_doc = sm_loader.load()
chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
chain.run(sm_doc)


"""
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(sm_doc)
print(texts)
username = "advaitpaliwal" # replace with your username from app.activeloop.ai
dataset_path = f"hub://{username}/gbl_assignment"
embeddings = OpenAIEmbeddings()
db = DeepLake.from_documents(texts, embeddings, dataset_path=dataset_path)
db.add_documents(texts)

db = DeepLake(dataset_path=dataset_path, read_only=True, embedding_function=embeddings)
retriever = db.as_retriever()
retriever = db.as_retriever()
retriever.search_kwargs['distance_metric'] = 'cos'
retriever.search_kwargs['k'] = 20

def filter(x):
    if 'com.google' in x['text'].data()['value']:
        return False
    metadata = x['metadata'].data()['value']
    return 'scala' in metadata['source'] or 'py' in metadata['source']

# Uncomment the following line to apply custom filtering
# retriever.search_kwargs['filter'] = filter


from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

model = ChatOpenAI(model='gpt-3.5-turbo')
qa = RetrievalQA.from_llm(model, retriever=retriever)


questions = [
    "What are your two (2) most significant “take-aways” from Dr. Baird’s presentations? Write at least a short paragraph for each and be specific. ",
    "Will viewing the recording affect your actions now or in your future career or personal life? If so, why? If not, why not?",
    "Write three thoughtful questions you would like to pose to Dr. Baird.",
    "What, if anything, has working on Ethics Game taught you about ethics that you did not already know?"
] 

for question in questions:  
    result = qa.run(question)
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result} \n")

"""