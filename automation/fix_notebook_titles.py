#!/usr/bin/env python3
"""Fix notebook titles to match workspace standards"""

import json
from pathlib import Path

NOTEBOOK_TITLES = {
    "001": "Data Structures, Algorithms & Python Mastery",
    "002": "Python Advanced Concepts",
    "010": "Linear Regression",
    "011": "Polynomial Regression",
    "016": "Decision Trees",
    "023": "K-Nearest Neighbors (KNN)",
    "024": "Support Vector Machines (SVM)",
    "036": "Isolation Forest",
    "037": "One-Class SVM",
    "038": "Autoencoders for Anomaly Detection",
    "039": "Association Rules (Apriori, FP-Growth)",
    "040": "Recommender Systems",
    "041": "Feature Engineering Masterclass",
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
    "073": "Vision Transformers (ViT)",
    "074": "Multimodal Models",
    "075": "Reinforcement Learning",
    "076": "Deep Reinforcement Learning (DQN, A3C)",
    "077": "Multi-Agent Reinforcement Learning",
}

workspace_root = Path(__file__).parent.parent
fixed_count = 0

for notebook_path in sorted(workspace_root.rglob("*.ipynb")):
    if '.ipynb_checkpoints' in str(notebook_path) or notebook_path.name.startswith('X'):
        continue
    
    number = notebook_path.name.split('_')[0]
    expected_title = NOTEBOOK_TITLES.get(number)
    
    if not expected_title:
        continue
    
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    first_cell = notebook['cells'][0]
    
    if first_cell['cell_type'] == 'markdown':
        source = ''.join(first_cell['source'])
        first_line = source.split('\n')[0].strip()
        
        if first_line.startswith(f"# {number}:"):
            continue
        
        # Prepare new title
        new_title = f"# {number}: {expected_title}\n\n"
        lines = source.split('\n')
        
        # Skip old title if present
        if lines[0].strip().startswith('#'):
            content_lines = lines[1:]
        else:
            content_lines = lines
        
        # Remove leading empty lines
        while content_lines and not content_lines[0].strip():
            content_lines.pop(0)
        
        existing_content = '\n'.join(content_lines)
        new_source = new_title + existing_content
        
        first_cell['source'] = new_source.split('\n')
        
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=1)
        
        print(f"✅ {notebook_path.name}")
        fixed_count += 1

print(f"\n✅ Fixed {fixed_count} notebooks")
