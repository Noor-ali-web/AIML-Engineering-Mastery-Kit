#!/bin/bash
# Setup script for notebook automation

echo "🚀 Setting up Notebook Generation Automation"
echo "============================================="

# Check Python version
echo -e "\n1️⃣ Checking Python version..."
python3 --version || { echo "❌ Python 3 not found"; exit 1; }

# Install OpenAI package
echo -e "\n2️⃣ Installing OpenAI package..."
pip install openai --quiet || { echo "❌ Failed to install openai"; exit 1; }
echo "✅ OpenAI package installed"

# Check for API key
echo -e "\n3️⃣ Checking for OpenAI API key..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo ""
    echo "Please set your API key:"
    echo "  export OPENAI_API_KEY='your-gpt-5-key-here'"
    echo ""
    echo "Or add to ~/.zshrc for persistence:"
    echo "  echo 'export OPENAI_API_KEY=\"your-key\"' >> ~/.zshrc"
    echo "  source ~/.zshrc"
else
    # Mask key for security (show first 8 chars)
    masked_key="${OPENAI_API_KEY:0:8}...${OPENAI_API_KEY: -4}"
    echo "✅ API key found: $masked_key"
fi

# Verify workspace instructions exist
echo -e "\n4️⃣ Checking workspace instructions..."
if [ -f ".github/copilot-instructions.md" ]; then
    echo "✅ Workspace instructions found"
else
    echo "❌ .github/copilot-instructions.md not found"
    echo "   This file is needed for quality control"
    exit 1
fi

# Create output directories if needed
echo -e "\n5️⃣ Verifying directory structure..."
mkdir -p 08_Modern_AI
mkdir -p 09_Data_Engineering
mkdir -p 10_MLOps
mkdir -p 11_Cloud_Deployment
echo "✅ Directories ready"

# Test import
echo -e "\n6️⃣ Testing automation scripts..."
cd automation
python3 -c "from notebook_generator import NotebookGenerator; print('✅ notebook_generator.py OK')" || { echo "❌ Script import failed"; exit 1; }
python3 -c "from batch_generator import NOTEBOOK_SPECS; print(f'✅ batch_generator.py OK ({len(NOTEBOOK_SPECS)} specs loaded)')" || { echo "❌ Script import failed"; exit 1; }
cd ..

echo -e "\n============================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Set OPENAI_API_KEY if not already set"
echo "  2. Generate notebooks:"
echo "     cd automation"
echo "     python batch_generator.py 0 2  # Start with 2 notebooks"
echo ""
echo "See automation/README.md for full documentation"
