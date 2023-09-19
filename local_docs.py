import os

from PyPDF2 import PdfReader
from langchain import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

os.environ["OPENAI_API_KEY"] = "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"

def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    text_splitter = CharacterTextSplitter(
        separator = " ",
        chunk_size = 2000,
        chunk_overlap  = 500,
        length_function = len,
    )
    texts = text_splitter.split_text(raw_text)
    return texts


fds_path = 'src/wiper_manual_mechanical.pdf'
####default embedding model is text-embedding-ada-002
embeddings = OpenAIEmbeddings()
fds_retriever = None
fds_texts = read_pdf(fds_path)
# fds_texts = read_from_image_pdf(fds_path)
fds_retriever = FAISS.from_texts(fds_texts, embeddings)
fds_retriever.save_local("local_docs")




# 本地知识库2
# idl_retriever = None
# idl_texts = read_pdf(idl_path)
# if idl_enable:
#     print("######## embedding idl and store into vector db ########")
#     idl_retriever = FAISS.from_texts(idl_texts, embeddings).as_retriever(search_kwargs = {"k": 5})