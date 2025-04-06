import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def embed_chunks(chunks):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(chunks).toarray().astype("float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return index, vectors, vectorizer

def get_top_k_chunks(query, chunks, index, vectorizer, k=3):
    query_vec = vectorizer.transform([query]).toarray().astype("float32")
    D, I = index.search(query_vec, k)
    return [chunks[i] for i in I[0]]
