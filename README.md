# 🔬 Scientific Paper RAG Chatbot

A sophisticated Retrieval-Augmented Generation (RAG) chatbot specifically designed for analyzing scientific papers. Features section-level semantic querying and rank-based re-weighting for improved factual accuracy.

## ✨ Key Features

- **📑 Section-Level Semantic Querying**: Automatically detects and extracts scientific paper sections (Abstract, Introduction, Methods, Results, Discussion, Conclusion, etc.)
- **🎯 Rank-Based Re-weighting**: Implements intelligent weighting of retrieved chunks based on relevance ranking, prioritizing the most pertinent information
- **🧠 Advanced Semantic Embeddings**: Uses state-of-the-art sentence transformers (all-MiniLM-L6-v2) for superior semantic understanding
- **🔍 Section Filtering**: Query specific sections of the paper or search across all sections
- **📊 Source Attribution**: Displays which sections were used to generate answers with relevance scores
- **🎨 Modern UI**: Clean, intuitive Streamlit interface with visualization of retrieval details

## 🏗️ Architecture

### Core Components

1. **embedding_utils.py**: Document processing and intelligent retrieval
   - PDF text extraction with page tracking
   - Scientific paper section detection using regex patterns
   - Semantic chunking with section preservation
   - FAISS vector indexing with cosine similarity
   - Rank-based re-weighting algorithm

2. **generator.py**: Context-aware response generation
   - Weighted chunk integration with section context
   - GPT-4 powered responses with scientific reasoning
   - Temperature-controlled output for factual accuracy
   - Automatic source citation

3. **app.py**: Interactive web interface
   - Real-time section detection and statistics
   - Configurable retrieval parameters
   - Visual display of chunk rankings and relevance scores
   - Expandable retrieval details

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd RAG-Based-Chatbot

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'  # Linux/Mac
# or
set OPENAI_API_KEY=your-api-key-here  # Windows CMD
# or
$env:OPENAI_API_KEY='your-api-key-here'  # Windows PowerShell
```

### Run the Application

```bash
streamlit run ui/app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📖 Usage

1. **Upload a Scientific Paper**: Click "Browse files" and upload a PDF of a research paper
2. **Wait for Processing**: The system will automatically:
   - Extract text from the PDF
   - Detect paper sections
   - Create semantic embeddings
   - Build the vector index
3. **View Detected Sections**: Check the sidebar to see all detected sections
4. **Configure Query Settings**:
   - Select specific sections to search (or "All Sections")
   - Adjust number of chunks to retrieve (3-10)
   - Toggle source attribution display
5. **Ask Questions**: Enter natural language questions about the paper
6. **Review Answers**: Get detailed answers with section citations and relevance scores
7. **Inspect Retrieval**: Expand "Retrieved Chunks Details" to see exactly what context was used

## 🎯 Example Questions

- What is the main contribution of this paper?
- What methodology was used in this research?
- What were the key results and findings?
- What datasets were used for evaluation?
- What are the limitations mentioned by the authors?
- What future work is suggested?

## 🧪 Technical Details

### Section Detection
Automatically recognizes common scientific paper sections:
- Abstract, Introduction, Background
- Related Work, Literature Review
- Methodology, Methods, Materials and Methods
- Experimental Setup, Results, Findings
- Discussion, Conclusion
- References, Bibliography, Acknowledgments, Appendix

### Rank-Based Re-weighting Algorithm
```python
weights = exp(-0.3 * (rank - 1))
normalized_weights = weights / sum(weights)
```
This exponential decay function ensures:
- Top-ranked chunks receive significantly higher weight
- Information quality degrades gracefully with rank
- Total weight sums to 1 for balanced integration

### Embedding Model
- **Model**: all-MiniLM-L6-v2 (sentence-transformers)
- **Dimension**: 384
- **Similarity**: Cosine similarity via FAISS IndexFlatIP
- **Performance**: Fast inference, high quality semantic representations

## 📦 Dependencies

- **streamlit**: Web interface framework
- **faiss-cpu**: Efficient similarity search
- **PyPDF2**: PDF text extraction
- **langchain**: Text splitting utilities
- **sentence-transformers**: Semantic embeddings
- **openai**: GPT-4 API access
- **scikit-learn**: Additional ML utilities
- **numpy**: Numerical operations

## 🚀 Future Enhancements

- [ ] Support for multiple document comparison
- [ ] Citation extraction and linking
- [ ] Figure and table extraction
- [ ] Export conversation history
- [ ] Custom section definitions
- [ ] Multi-modal support (images, equations)

## 📄 License

MIT License

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
