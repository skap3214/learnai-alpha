from PyPDF2 import PdfReader, PdfMerger
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os
import api

# Constants
SUMMARIZE_PROMPT = '''Write a brief outline on what the document is about.'''
QUESTION_ANSWERS_PROMPT = '''Please divide the given text into sections, provide an excerpt from each section, create a relevant question for each excerpt, and then provide an answer based on the content.'''

# Function to merge PDFs into a single file
def merge_pdfs(pdfs, output):
    pdf_merger = PdfMerger()
    for pdf in pdfs:
        pdf_merger.append(pdf)
    with open(output, 'wb') as f:
        pdf_merger.write(f)

# Function to preprocess the text by merging the PDFs, extracting the text, and initializing the search and chain objects
def preprocess_text(pdf_files_lst, merged_output):
    merge_pdfs(pdf_files_lst, merged_output)
    reader = PdfReader(merged_output)

    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    embeddings = OpenAIEmbeddings(openai_api_key=api.OPENAI_API_KEY)
    docsearch = FAISS.from_texts(texts, embeddings)
    llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api.OPENAI_API_KEY)

    chain = load_qa_chain(llm=llm, chain_type="stuff")

    return docsearch, chain

# Function to generate the summary of the document
def pdf_summary(docsearch, chain):
    docs = docsearch.similarity_search(SUMMARIZE_PROMPT)
    result = chain.run(input_documents=docs, question=SUMMARIZE_PROMPT)
    summary = '\n' + result + '\n\n'
    return summary

# Function to generate the questions and answers based on the document
def pdf_questions_answers(docsearch, chain):
    docs = docsearch.similarity_search(QUESTION_ANSWERS_PROMPT)
    result = chain.run(input_documents=docs, question=QUESTION_ANSWERS_PROMPT)
    questions_answers = result
    return questions_answers


# if __name__ == '__main__':
#     pdf = ['physics.pdf']  # Add your own pdf
#     merged_output = 'output.pdf'
#     docsearch, chain = preprocess_text(pdf, merged_output)

#     print(pdf_summary(docsearch, chain))  # Print part_1 (summary)
#     print(pdf_questions_answers(docsearch, chain))  # Print part_2 (questions and answers)
#     os.remove(merged_output)
