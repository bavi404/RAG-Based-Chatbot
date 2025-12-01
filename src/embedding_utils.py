import faiss
import numpy as np
import re
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Initialize semantic embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Common scientific paper section headers
SECTION_PATTERNS = [
    r'^\s*abstract\s*$',
    r'^\s*introduction\s*$',
    r'^\s*background\s*$',
    r'^\s*related\s+work\s*$',
    r'^\s*literature\s+review\s*$',
    r'^\s*methodology\s*$',
    r'^\s*methods\s*$',
    r'^\s*materials\s+and\s+methods\s*$',
    r'^\s*experimental\s+setup\s*$',
    r'^\s*results\s*$',
    r'^\s*findings\s*$',
    r'^\s*results\s+and\s+discussion\s*$',
    r'^\s*discussion\s*$',
    r'^\s*conclusion\s*$',
    r'^\s*conclusions\s*$',
    r'^\s*future\s+work\s*$',
    r'^\s*references\s*$',
    r'^\s*bibliography\s*$',
    r'^\s*acknowledgments?\s*$',
    r'^\s*appendix\s*$',
]

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF with page information"""
    reader = PdfReader(uploaded_file)
    text = ""
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        text += f"\n[PAGE {page_num + 1}]\n{page_text}"
    return text

def detect_sections(text):
    """Detect scientific paper sections in the text"""
    lines = text.split('\n')
    sections = []
    current_section = {'name': 'Header', 'start_line': 0, 'content': ''}
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Check if line matches any section pattern
        is_section_header = False
        for pattern in SECTION_PATTERNS:
            if re.match(pattern, line_lower, re.IGNORECASE):
                # Save previous section
                if current_section['content'].strip():
                    sections.append(current_section)
                
                # Start new section
                current_section = {
                    'name': line.strip().title(),
                    'start_line': i,
                    'content': ''
                }
                is_section_header = True
                break
        
        if not is_section_header:
            current_section['content'] += line + '\n'
    
    # Add the last section
    if current_section['content'].strip():
        sections.append(current_section)
    
    return sections

def chunk_text_with_sections(text, chunk_size=500, chunk_overlap=100):
    """Chunk text while preserving section information"""
    sections = detect_sections(text)
    chunked_data = []
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    for section in sections:
        section_chunks = splitter.split_text(section['content'])
        for chunk in section_chunks:
            if chunk.strip():  # Only add non-empty chunks
                chunked_data.append({
                    'text': chunk,
                    'section': section['name'],
                    'section_start': section['start_line']
                })
    
    return chunked_data

def embed_chunks(chunked_data):
    """Create semantic embeddings using sentence-transformers"""
    texts = [item['text'] for item in chunked_data]
    
    # Generate embeddings
    embeddings = embedding_model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    embeddings = embeddings.astype('float32')
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    
    return index, embeddings

def apply_rank_based_weighting(distances, k=5):
    """
    Apply rank-based re-weighting to retrieved chunks
    Higher-ranked chunks get exponentially higher weights
    """
    ranks = np.arange(1, k + 1)
    # Exponential decay: first chunk gets highest weight
    weights = np.exp(-0.3 * (ranks - 1))
    # Normalize weights to sum to 1
    weights = weights / weights.sum()
    return weights

def get_top_k_chunks(query, chunked_data, index, k=5, section_filter=None):
    """
    Retrieve top-k chunks with rank-based weighting and optional section filtering
    """
    # Filter by section if specified
    if section_filter and section_filter != "All Sections":
        filtered_indices = [i for i, item in enumerate(chunked_data) if item['section'] == section_filter]
        if not filtered_indices:
            return [], [], []
        
        # Create temporary index for filtered chunks
        filtered_embeddings = np.array([index.reconstruct(i) for i in filtered_indices])
        temp_index = faiss.IndexFlatIP(filtered_embeddings.shape[1])
        temp_index.add(filtered_embeddings)
        
        query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        distances, indices = temp_index.search(query_embedding, min(k, len(filtered_indices)))
        
        # Map back to original indices
        original_indices = [filtered_indices[idx] for idx in indices[0]]
        retrieved_chunks = [chunked_data[i] for i in original_indices]
    else:
        # Search all chunks
        query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        distances, indices = index.search(query_embedding, k)
        retrieved_chunks = [chunked_data[i] for i in indices[0]]
    
    # Apply rank-based weighting
    weights = apply_rank_based_weighting(distances[0], k=len(retrieved_chunks))
    
    return retrieved_chunks, weights, distances[0]

def get_available_sections(chunked_data):
    """Get list of unique sections in the document"""
    sections = list(set([item['section'] for item in chunked_data]))
    return sorted(sections)
