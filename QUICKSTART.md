# ⚡ Quick Start Guide

Get up and running with the Scientific Paper RAG Chatbot in 5 minutes!

## 🚀 Option 1: Automated Setup (Recommended)

### Step 1: Run Setup Script
```bash
python setup.py
```

This will:
- ✅ Check Python version
- ✅ Install all dependencies
- ✅ Verify OpenAI API key
- ✅ Download embedding model

### Step 2: Set OpenAI API Key

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-api-key-here"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

### Step 3: Launch the App
```bash
streamlit run ui/app.py
```

### Step 4: Start Analyzing!
1. Upload a scientific paper PDF
2. Wait for processing (~10-30 seconds)
3. Ask questions!

---

## 🔧 Option 2: Manual Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set API Key
```bash
export OPENAI_API_KEY="your-key-here"
```

### Step 3: Run App
```bash
streamlit run ui/app.py
```

---

## 🎓 Using Google Colab (No Installation Required!)

### Step 1: Open the Notebook
Upload `RAG_Chatbot_Colab.ipynb` to Google Colab

### Step 2: Run All Cells
Click `Runtime > Run all`

### Step 3: Provide API Key
When prompted, enter your OpenAI API key

### Step 4: Upload Paper & Query
Follow the interactive prompts!

---

## 📝 Example Usage

### Basic Questions:
```
Q: What is the main contribution of this paper?
Q: What methodology was used?
Q: What were the key results?
```

### Section-Specific Questions:
1. In sidebar, select "Methods"
2. Ask: "What datasets were used?"

### Advanced Queries:
- "How does this approach compare to prior work?"
- "What are the limitations mentioned?"
- "What future work is suggested?"

---

## 🎯 Pro Tips

### 1. Adjust Retrieval Settings
- **More chunks** (7-10): Comprehensive but may include noise
- **Fewer chunks** (3-5): Focused and precise

### 2. Use Section Filtering
For targeted questions, filter by specific sections:
- "Methods" → Implementation details
- "Results" → Findings and metrics
- "Conclusion" → Takeaways and impact

### 3. Review Retrieved Chunks
Expand "Retrieved Chunks Details" to:
- See which chunks were used
- Verify relevance weights
- Check source sections

### 4. Check Section Detection
- View detected sections in sidebar
- Ensure paper was parsed correctly
- If sections missing, paper may have non-standard formatting

---

## ⚠️ Troubleshooting

### "OpenAI API key not found"
**Solution**: Set the environment variable (see Step 2 above)

### "Module not found" errors
**Solution**: Run `pip install -r requirements.txt --upgrade`

### Slow processing
**Normal**: First run downloads the embedding model (~100MB)
**Solution**: Be patient during initial setup

### Poor section detection
**Cause**: Non-standard paper formatting
**Solution**: Papers work best with clear section headers (Abstract, Introduction, Methods, etc.)

### App won't start
**Check**:
- Python version (must be 3.8+)
- All dependencies installed
- Port 8501 not in use

---

## 📊 What to Expect

### Processing Time:
- **10-page paper**: ~15-20 seconds
- **20-page paper**: ~30-40 seconds
- **50-page paper**: ~60-90 seconds

### Sections Detected:
- Typical paper: 6-10 sections
- Thesis/dissertation: 10-20 sections

### Query Response Time:
- 2-5 seconds per question
- Depends on OpenAI API latency

---

## 🎨 Interface Overview

### Sidebar:
- 📄 Upload paper
- 📊 View document stats
- 🔍 Configure retrieval settings
- 📑 Browse detected sections

### Main Area:
- 💬 Ask questions
- ✅ View answers with citations
- 🔎 Inspect retrieval details
- 💡 See example questions

---

## 🔥 Quick Feature Tour

### 1. Section Detection
Watch as the app automatically identifies paper sections!

### 2. Semantic Search
Ask questions in natural language - no keywords needed

### 3. Rank-Based Weighting
See how chunks are weighted by relevance (PRIMARY > SECONDARY > SUPPORTING)

### 4. Source Attribution
Every answer shows which sections were used

### 5. Configurable Retrieval
Adjust chunk count and section filters on the fly

---

## 📚 Example Papers to Try

Good candidates for testing:
- ✅ ArXiv papers (standard format)
- ✅ Conference papers (ACL, NeurIPS, CVPR, etc.)
- ✅ Journal articles
- ✅ Technical reports
- ✅ PhD theses

Less ideal:
- ❌ Scanned PDFs (text extraction issues)
- ❌ Papers without clear sections
- ❌ Non-English papers
- ❌ Slides or presentations

---

## 🆘 Need Help?

1. **Check the README**: Comprehensive documentation
2. **Read IMPROVEMENTS.md**: Detailed feature explanations
3. **Review code comments**: Inline documentation
4. **Test with sample paper**: Verify setup with a known good paper

---

## 🎉 You're Ready!

Start uploading scientific papers and discover:
- 📖 Main contributions
- 🔬 Methodologies used
- 📊 Key findings
- 🔮 Future work directions
- 📝 Related work comparisons

**Happy researching!** 🚀

---

*For advanced configuration and customization, see the full README.md*

