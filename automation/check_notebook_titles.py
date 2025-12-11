#!/usr/bin/env python3
"""
Check and add proper titles to all notebooks
Ensures consistent structure across all 78 notebooks
"""

import json
from pathlib import Path
from typing import Dict, List

# Title mapping for all notebooks
NOTEBOOK_TITLES = {
    "001": "Data Structures, Algorithms & Python Mastery",
    "002": "Python Advanced Concepts",
    "010": "Linear Regression",
    "016": "Decision Trees",
    "019": "XGBoost",
    "022": "Voting & Stacking Ensembles",
    "023": "K-Nearest Neighbors (KNN)",
    "024": "Support Vector Machines (SVM)",
    "025": "Naive Bayes",
    "026": "K-Means Clustering",
    "027": "Hierarchical Clustering",
    "028": "DBSCAN",
    "029": "Gaussian Mixture Models (GMM)",
    "030": "Dimensionality Reduction (PCA, t-SNE, UMAP)",
    "031": "Time Series Fundamentals (ARIMA, SARIMA)",
    "032": "Exponential Smoothing (Holt-Winters)",
    "033": "Prophet - Modern Time Series",
    "034": "VAR - Multivariate Time Series",
    "036": "Isolation Forest",
    "037": "One-Class SVM",
    "038": "Autoencoders for Anomaly Detection",
    "039": "Association Rules (Apriori, FP-Growth)",
    "040": "Recommender Systems",
    "046": "Model Interpretation & Explainability",
    "047": "ML Pipelines & Automation",
    "049": "Imbalanced Data Handling",
    "050": "AutoML Frameworks",
    "051": "Neural Networks Foundations",
    "052": "Deep Learning Frameworks (PyTorch & TensorFlow)",
    "053": "CNN Architectures (LeNet, AlexNet, VGG, ResNet)",
    "054": "Transfer Learning & Fine-Tuning",
    "055": "Object Detection (YOLO, R-CNN)",
    "056": "RNN, LSTM, GRU",
    "057": "Seq2Seq & Attention Mechanisms",
    "058": "Transformers & Self-Attention",
    "059": "BERT & Transfer Learning in NLP",
    "060": "GPT & Autoregressive Language Models",
    "061": "RLHF & Instruction Following",
    "062": "Seq2Seq Neural Machine Translation",
    "063": "Generative Adversarial Networks (GANs)",
    "064": "Reinforcement Learning Basics",
    "065": "Deep Reinforcement Learning",
    "066": "Attention Mechanisms",
    "067": "Neural Architecture Search (NAS)",
    "068": "Model Compression & Quantization",
    "069": "Federated Learning",
    "070": "Edge AI & TinyML",
    "071": "Transformers & BERT",
    "072": "GPT & Large Language Models",
    "073": "Vision Transformers (ViT)",
    "074": "Multimodal Models",
    "075": "Reinforcement Learning",
    "076": "Deep Reinforcement Learning (DQN, A3C)",
    "077": "Multi-Agent Reinforcement Learning",
    "078": "Multimodal Large Language Models",
    "079": "RAG (Retrieval-Augmented Generation) Fundamentals",
}

def check_notebook_title(notebook_path: Path) -> Dict:
    """Check if notebook has proper title structure"""
    
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    first_cell = notebook['cells'][0]
    
    # Extract notebook number from filename
    filename = notebook_path.name
    number = filename.split('_')[0]
    
    result = {
        "path": str(notebook_path),
        "number": number,
        "filename": filename,
        "has_title": False,
        "current_first_line": "",
        "needs_update": False
    }
    
    if first_cell['cell_type'] == 'markdown':
        source = ''.join(first_cell['source'])
        lines = source.split('\n')
        first_line = lines[0].strip() if lines else ""
        
        result["current_first_line"] = first_line
        
        # Check if it starts with "# NNN:" format
        if first_line.startswith(f"# {number}:") or first_line.startswith(f"# {number} -"):
            result["has_title"] = True
        else:
            result["needs_update"] = True
    else:
        result["needs_update"] = True
    
    return result

def scan_all_notebooks(workspace_root: Path) -> List[Dict]:
    """Scan all notebooks in workspace"""
    
    results = []
    
    # Find all .ipynb files
    for notebook_path in workspace_root.rglob("*.ipynb"):
        # Skip checkpoints and X-prefixed files
        if '.ipynb_checkpoints' in str(notebook_path) or notebook_path.name.startswith('X'):
            continue
        
        try:
            result = check_notebook_title(notebook_path)
            results.append(result)
        except Exception as e:
            print(f"❌ Error checking {notebook_path.name}: {e}")
    
    return results

def print_report(results: List[Dict]):
    """Print summary report"""
    
    total = len(results)
    has_title = sum(1 for r in results if r['has_title'])
    needs_update = sum(1 for r in results if r['needs_update'])
    
    print(f"\n{'='*80}")
    print(f"NOTEBOOK TITLE AUDIT REPORT")
    print(f"{'='*80}")
    print(f"\n📊 Summary:")
    print(f"   Total notebooks: {total}")
    print(f"   ✅ Has proper title: {has_title} ({has_title/total*100:.1f}%)")
    print(f"   ⚠️  Needs update: {needs_update} ({needs_update/total*100:.1f}%)")
    
    if needs_update > 0:
        print(f"\n⚠️  Notebooks needing title updates:")
        print(f"{'='*80}")
        
        for r in sorted(results, key=lambda x: x['number']):
            if r['needs_update']:
                expected_title = NOTEBOOK_TITLES.get(r['number'], "Unknown")
                print(f"\n📝 {r['filename']}")
                print(f"   Current: {r['current_first_line'][:70]}...")
                print(f"   Expected: # {r['number']}: {expected_title}")
    
    print(f"\n{'='*80}\n")

def main():
    workspace_root = Path(__file__).parent.parent
    
    print("🔍 Scanning all notebooks for title consistency...")
    results = scan_all_notebooks(workspace_root)
    
    print_report(results)
    
    print("💡 To fix notebooks:")
    print("   1. Update .github/copilot-instructions.md with title requirements")
    print("   2. Run title-fix script (to be created)")
    print("   3. Verify changes with git diff")

if __name__ == "__main__":
    main()
