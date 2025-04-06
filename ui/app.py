import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.embedding_utils import extract_text_from_pdf, chunk_text, embed_chunks, get_top_k_chunks
from src.generator import generate_response

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("📄 RAG-based Document Chatbot")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting & Processing..."):
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        index, vectors, vectorizer = embed_chunks(chunks)
    st.success("Document processed!")

    query = st.text_input("Ask your question:")
    if query:
        with st.spinner("Thinking..."):
            top_chunks = get_top_k_chunks(query, chunks, index, vectorizer)
            answer = generate_response(top_chunks, query)
        st.markdown("### ✅ Answer")
        st.write(answer)
