import streamlit as st
import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.embedding_utils import (
    extract_text_from_pdf, 
    chunk_text_with_sections, 
    embed_chunks, 
    get_top_k_chunks,
    get_available_sections
)
from src.generator import generate_response

# Page configuration
st.set_page_config(
    page_title="Scientific Paper RAG Chatbot", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        background-color: #e3f2fd;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🔬 Scientific Paper RAG Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Retrieval-Augmented Generation with Section-Level Semantic Querying & Rank-Based Re-weighting</div>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.subheader("📄 Upload Paper")
    uploaded_file = st.file_uploader(
        "Upload a scientific paper (PDF)", 
        type=["pdf"],
        help="Upload a research paper to analyze"
    )
    
    if 'chunked_data' in st.session_state and st.session_state.chunked_data:
        st.success(f"✅ Paper loaded!")
        st.metric("Total Chunks", len(st.session_state.chunked_data))
        
        st.subheader("🔍 Query Settings")
        
        # Section filter
        available_sections = get_available_sections(st.session_state.chunked_data)
        section_filter = st.selectbox(
            "Filter by Section",
            ["All Sections"] + available_sections,
            help="Search only within specific paper sections"
        )
        st.session_state.section_filter = section_filter
        
        # Number of chunks
        num_chunks = st.slider(
            "Number of chunks to retrieve",
            min_value=3,
            max_value=10,
            value=5,
            help="More chunks = more context but potentially more noise"
        )
        st.session_state.num_chunks = num_chunks
        
        # Show sources
        show_sources = st.checkbox(
            "Show source sections",
            value=True,
            help="Display which sections were used to answer"
        )
        st.session_state.show_sources = show_sources
        
        st.subheader("📊 Document Sections")
        for section in available_sections:
            section_count = sum(1 for item in st.session_state.chunked_data if item['section'] == section)
            st.markdown(f"""
            <div class="section-badge">
                {section} ({section_count})
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    ### 🎯 Features
    - **Section-aware retrieval**: Query specific paper sections
    - **Semantic embeddings**: Advanced sentence transformers
    - **Rank-based weighting**: Prioritize most relevant chunks
    - **Factual accuracy**: GPT-4 with context-grounded responses
    """)

# Main content area
if uploaded_file:
    # Process document if not already processed or if new file
    if 'processed_file' not in st.session_state or st.session_state.processed_file != uploaded_file.name:
        with st.spinner("🔄 Extracting text and detecting sections..."):
            text = extract_text_from_pdf(uploaded_file)
        
        with st.spinner("📚 Chunking text with section information..."):
            chunked_data = chunk_text_with_sections(text)
            st.session_state.chunked_data = chunked_data
        
        with st.spinner("🧮 Creating semantic embeddings and building index..."):
            index, embeddings = embed_chunks(chunked_data)
            st.session_state.index = index
            st.session_state.embeddings = embeddings
        
        st.session_state.processed_file = uploaded_file.name
        st.session_state.section_filter = "All Sections"
        st.session_state.num_chunks = 5
        st.session_state.show_sources = True
        
        st.success("✅ Paper successfully processed and indexed!")
        st.rerun()
    
    # Query interface
    st.markdown("### 💬 Ask Questions About the Paper")
    
    # Example questions
    with st.expander("💡 Example Questions"):
        st.markdown("""
        - What is the main contribution of this paper?
        - What methodology was used in this research?
        - What were the key results and findings?
        - What datasets were used for evaluation?
        - What are the limitations mentioned?
        - What future work is suggested?
        """)
    
    query = st.text_input(
        "Enter your question:",
        placeholder="e.g., What is the main research question?",
        key="query_input"
    )
    
    if query:
        with st.spinner("🔍 Searching relevant sections and generating answer..."):
            # Retrieve chunks with rank-based weighting
            retrieved_chunks, weights, distances = get_top_k_chunks(
                query,
                st.session_state.chunked_data,
                st.session_state.index,
                k=st.session_state.num_chunks,
                section_filter=st.session_state.section_filter
            )
            
            if not retrieved_chunks:
                st.warning(f"⚠️ No relevant content found in section: {st.session_state.section_filter}")
            else:
                # Generate response
                answer = generate_response(
                    retrieved_chunks,
                    weights,
                    query,
                    show_sources=st.session_state.show_sources
                )
                
                # Display answer
                st.markdown("### ✅ Answer")
                st.markdown(answer)
                
                # Display retrieval details
                with st.expander("🔎 Retrieved Chunks Details"):
                    for i, (chunk, weight, dist) in enumerate(zip(retrieved_chunks, weights, distances)):
                        importance = "🥇 PRIMARY" if i == 0 else "🥈 SECONDARY" if i < 3 else "🥉 SUPPORTING"
                        
                        st.markdown(f"""
                        **{importance} - Chunk #{i+1}**
                        - **Section**: {chunk['section']}
                        - **Relevance Weight**: {weight:.2%}
                        - **Similarity Score**: {dist:.4f}
                        """)
                        
                        with st.container():
                            st.text_area(
                                f"Content",
                                chunk['text'][:500] + "..." if len(chunk['text']) > 500 else chunk['text'],
                                height=100,
                                key=f"chunk_{i}",
                                disabled=True
                            )
                        st.markdown("---")

else:
    # Welcome screen
    st.info("👆 Please upload a scientific paper PDF to get started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 How It Works
        
        1. **Upload** a scientific paper (PDF format)
        2. **Automatic section detection** (Abstract, Methods, Results, etc.)
        3. **Semantic chunking** with section preservation
        4. **Ask questions** using natural language
        5. **Get accurate answers** with source attribution
        """)
    
    with col2:
        st.markdown("""
        ### ✨ Key Features
        
        - **Section-Level Querying**: Filter by specific paper sections
        - **Semantic Search**: Advanced sentence transformers for better understanding
        - **Rank-Based Re-weighting**: Prioritizes most relevant chunks
        - **Source Attribution**: See which sections were used
        - **High Accuracy**: GPT-4 with grounded responses
        """)
