#!/usr/bin/env python
"""
Setup script for Scientific Paper RAG Chatbot
Handles installation and environment setup
"""

import subprocess
import sys
import os

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Ensure Python 3.8+"""
    print_header("🐍 Checking Python Version")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. You have {version.major}.{version.minor}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def install_dependencies():
    """Install required packages"""
    print_header("📦 Installing Dependencies")
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            "requirements.txt",
            "--upgrade"
        ])
        print("\n✅ All dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)

def verify_openai_key():
    """Check for OpenAI API key"""
    print_header("🔑 Checking OpenAI API Key")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️  OpenAI API key not found in environment variables")
        print("\nPlease set your API key using one of these methods:\n")
        
        if sys.platform == "win32":
            print("Windows (PowerShell):")
            print('  $env:OPENAI_API_KEY="your-api-key-here"')
            print("\nWindows (CMD):")
            print('  set OPENAI_API_KEY=your-api-key-here')
        else:
            print("Linux/Mac:")
            print('  export OPENAI_API_KEY="your-api-key-here"')
        
        print("\nOr add it to your .env file")
        return False
    else:
        masked_key = api_key[:8] + "..." + api_key[-4:]
        print(f"✅ API key found: {masked_key}")
        return True

def download_model():
    """Pre-download sentence-transformers model"""
    print_header("🤖 Downloading Embedding Model")
    try:
        from sentence_transformers import SentenceTransformer
        print("Downloading all-MiniLM-L6-v2 model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model downloaded and cached successfully!")
    except Exception as e:
        print(f"⚠️  Model download failed: {e}")
        print("The model will be downloaded on first use instead.")

def print_next_steps():
    """Print instructions for running the app"""
    print_header("🎉 Setup Complete!")
    print("Next steps:\n")
    print("1. Make sure your OpenAI API key is set (see above)")
    print("2. Run the application:")
    print("   streamlit run ui/app.py")
    print("\n3. Upload a scientific paper PDF")
    print("4. Ask questions about the paper!\n")
    print("For more information, see:")
    print("  - README.md (comprehensive guide)")
    print("  - IMPROVEMENTS.md (what's new)")
    print("\n" + "="*60 + "\n")

def main():
    """Main setup process"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  🔬 Scientific Paper RAG Chatbot - Setup               ║
    ║  Section-Level Querying + Rank-Based Re-weighting       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Run setup steps
    check_python_version()
    install_dependencies()
    has_key = verify_openai_key()
    
    try:
        download_model()
    except:
        pass  # Non-critical
    
    print_next_steps()
    
    if not has_key:
        print("⚠️  Remember to set your OpenAI API key before running!")

if __name__ == "__main__":
    main()

