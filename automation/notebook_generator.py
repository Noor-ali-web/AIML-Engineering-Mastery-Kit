#!/usr/bin/env python3
"""
Automated Notebook Generator for AI/ML Complete Mastery
Uses OpenAI GPT-5 to generate high-quality Jupyter notebooks following workspace standards
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from openai import OpenAI

class NotebookGenerator:
    """Generate comprehensive Jupyter notebooks using OpenAI GPT-5"""
    
    def __init__(self, api_key: str, workspace_root: str):
        self.client = OpenAI(api_key=api_key)
        self.workspace_root = Path(workspace_root)
        self.instructions_path = self.workspace_root / ".github" / "copilot-instructions.md"
        
        # Load workspace instructions (condensed version)
        self.workspace_instructions = """
# Notebook Quality Standards

**Cell Structure:**
- Alternate markdown explanations and code cells
- Every code cell MUST have markdown explanation before it
- Code cells: 20-100 lines maximum (meaningful blocks)
- Pattern: Markdown → Code → Markdown → Code

**Content Requirements:**
- Post-silicon validation examples (60%) + general AI/ML (40%)
- Mathematical foundations with LaTeX equations
- From-scratch implementation (NumPy, educational)
- Production implementation (sklearn/PyTorch, practical)
- Mermaid diagrams (workflow + architecture)
- 4-8 real-world projects (NOT exercises)

**Post-Silicon Context:**
- STDF test data: wafer_id, die_x, die_y, test parameters
- Electrical parameters: Vdd, Idd, frequency, power, temperature
- Use cases: yield prediction, test optimization, failure analysis
- Realistic semiconductor testing scenarios

**Required Sections:**
1. Introduction (with Mermaid workflow)
2. Mathematical Foundation (LaTeX equations)
3. From Scratch Implementation (NumPy)
4. Production Implementation (libraries)
5. Post-Silicon Examples (semiconductor)
6. General AI/ML Examples
7. Evaluation & Diagnostics
8. Projects (4-8 ideas with objectives)
9. Best Practices & Takeaways
"""
    
    def generate_notebook_content(self, notebook_spec: Dict) -> str:
        """
        Generate complete notebook content using GPT-5
        
        Args:
            notebook_spec: Dictionary with notebook details
                - number: Notebook number (e.g., "079")
                - title: Notebook title
                - category: Category (e.g., "Modern_AI")
                - topics: List of topics to cover
                - post_silicon_focus: Post-silicon use cases
                - prerequisites: List of prerequisite notebooks
        
        Returns:
            Complete notebook JSON as string
        """
        
        system_prompt = f"""You are an expert AI/ML educator creating comprehensive Jupyter notebooks.

WORKSPACE CONTEXT:
{self.workspace_instructions}

CRITICAL REQUIREMENTS:
1. **Cell Structure**: Alternate markdown explanations and code cells
2. **Code Cell Size**: NEVER exceed 100 lines per code cell
3. **Meaningful Blocks**: Each code cell = one complete concept (20-70 lines ideal)
4. **Explanations First**: Every code cell MUST have markdown explanation before it
5. **Post-Silicon Balance**: 60% post-silicon validation + 40% general AI/ML examples
6. **Quality Standard**: Reference notebook 010_Linear_Regression.ipynb structure

NOTEBOOK STRUCTURE (Required Sections):
1. Introduction (with Mermaid workflow diagram)
2. Mathematical Foundation (LaTeX equations with explanations)
3. From Scratch Implementation (NumPy only, educational)
4. Production Implementation (sklearn/PyTorch/etc, practical)
5. Post-Silicon Validation Examples (semiconductor testing)
6. General AI/ML Examples (broader applications)
7. Evaluation & Diagnostics (metrics, visualizations)
8. Real-World Projects (4-8 project ideas, NOT exercises)
9. Best Practices & Takeaways

OUTPUT FORMAT:
Generate complete Jupyter notebook as JSON with this structure:
{{
  "cells": [
    {{
      "cell_type": "markdown",
      "metadata": {{}},
      "source": ["# Cell content here"]
    }},
    {{
      "cell_type": "code",
      "execution_count": null,
      "metadata": {{}},
      "outputs": [],
      "source": ["# Code here (max 100 lines)"]
    }}
  ],
  "metadata": {{
    "kernelspec": {{
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    }},
    "language_info": {{
      "name": "python",
      "version": "3.12.0"
    }}
  }},
  "nbformat": 4,
  "nbformat_minor": 2
}}

QUALITY CHECKS:
- Total cells: 25-35 (alternating markdown/code)
- Code cells: Each 20-100 lines maximum
- Mermaid diagrams: At least 2 (workflow + architecture)
- Projects: 4-8 with clear objectives and business value
- Post-silicon examples: Realistic STDF data scenarios
"""

        user_prompt = f"""Generate Notebook {notebook_spec['number']}: {notebook_spec['title']}

**Category**: {notebook_spec['category']}

**Topics to Cover**:
{chr(10).join(f"- {topic}" for topic in notebook_spec['topics'])}

**Post-Silicon Focus**:
{chr(10).join(f"- {use_case}" for use_case in notebook_spec.get('post_silicon_focus', []))}

**Prerequisites**: {', '.join(notebook_spec.get('prerequisites', []))}

**Learning Objectives**:
{chr(10).join(f"- {obj}" for obj in notebook_spec.get('learning_objectives', []))}

Generate a COMPLETE, production-ready notebook following ALL workspace standards. Include:
1. Comprehensive mathematical explanations with LaTeX
2. From-scratch implementation (NumPy) for learning
3. Production implementation (appropriate library)
4. Realistic post-silicon validation examples using STDF data patterns
5. General AI/ML examples for broader applicability
6. Complete evaluation metrics and visualizations
7. 4-8 real-world project ideas (mix post-silicon and general)
8. Mermaid diagrams for workflows and architectures

Return ONLY valid JSON (no markdown formatting, no code blocks).
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # GPT-4o has 128k context
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=8000  # Reduced to fit within limits
            )
            
            content = response.choices[0].message.content
            
            # Clean up response if it has markdown code blocks
            if content.startswith("```"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
            
            # Validate JSON
            notebook_data = json.loads(content)
            
            return json.dumps(notebook_data, indent=2)
        
        except Exception as e:
            print(f"Error generating notebook: {e}")
            raise
    
    def save_notebook(self, notebook_json: str, output_path: Path):
        """Save generated notebook to file"""
        with open(output_path, 'w') as f:
            f.write(notebook_json)
        print(f"✅ Saved: {output_path}")
    
    def generate_and_save(self, notebook_spec: Dict, output_dir: Optional[Path] = None):
        """Generate notebook and save to appropriate directory"""
        
        if output_dir is None:
            # Determine output directory from category
            category_map = {
                "Foundations": "01_Foundations",
                "Machine_Learning": "02_Machine_Learning",
                "ML_Engineering": "06_ML_Engineering",
                "Deep_Learning": "07_Deep_Learning",
                "Modern_AI": "08_Modern_AI",
                "Data_Engineering": "09_Data_Engineering",
                "MLOps": "10_MLOps",
                "Cloud_Deployment": "11_Cloud_Deployment"
            }
            output_dir = self.workspace_root / category_map.get(
                notebook_spec['category'], 
                "08_Modern_AI"
            )
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        number = notebook_spec['number']
        title = notebook_spec['title'].replace(' ', '_')
        filename = f"{number}_{title}.ipynb"
        output_path = output_dir / filename
        
        print(f"🔄 Generating: {filename}")
        
        # Generate notebook content
        notebook_json = self.generate_notebook_content(notebook_spec)
        
        # Save to file
        self.save_notebook(notebook_json, output_path)
        
        return output_path
    
    def validate_notebook_structure(self, notebook_path: Path) -> Dict[str, bool]:
        """Validate generated notebook meets quality standards"""
        
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        checks = {
            "has_cells": len(notebook.get('cells', [])) > 0,
            "cell_count_appropriate": 25 <= len(notebook.get('cells', [])) <= 40,
            "alternating_cells": True,
            "no_oversized_code": True,
            "has_mermaid": False,
            "has_projects": False
        }
        
        cells = notebook.get('cells', [])
        
        # Check alternating pattern
        for i in range(1, len(cells)):
            if cells[i]['cell_type'] == 'code' and cells[i-1]['cell_type'] != 'markdown':
                checks["alternating_cells"] = False
                break
        
        # Check code cell sizes
        for cell in cells:
            if cell['cell_type'] == 'code':
                line_count = len(cell.get('source', []))
                if line_count > 100:
                    checks["no_oversized_code"] = False
                    print(f"⚠️  Found {line_count}-line code cell (max 100)")
        
        # Check for Mermaid diagrams
        for cell in cells:
            if cell['cell_type'] == 'markdown':
                content = ''.join(cell.get('source', []))
                if '```mermaid' in content:
                    checks["has_mermaid"] = True
                if 'Project' in content or '## 🎯' in content:
                    checks["has_projects"] = True
        
        return checks
    
    def generate_batch(self, notebook_specs: List[Dict], delay: int = 5):
        """Generate multiple notebooks with rate limiting"""
        
        results = []
        
        for i, spec in enumerate(notebook_specs):
            print(f"\n{'='*60}")
            print(f"Processing {i+1}/{len(notebook_specs)}: Notebook {spec['number']}")
            print(f"{'='*60}")
            
            try:
                output_path = self.generate_and_save(spec)
                
                # Validate
                print(f"🔍 Validating: {output_path.name}")
                validation = self.validate_notebook_structure(output_path)
                
                all_passed = all(validation.values())
                status = "✅ PASSED" if all_passed else "⚠️  WARNINGS"
                
                print(f"{status}: {output_path.name}")
                for check, passed in validation.items():
                    symbol = "✅" if passed else "❌"
                    print(f"  {symbol} {check}")
                
                results.append({
                    "notebook": spec['number'],
                    "path": str(output_path),
                    "validation": validation,
                    "status": "success"
                })
                
                # Rate limiting
                if i < len(notebook_specs) - 1:
                    print(f"\n⏳ Waiting {delay}s before next generation...")
                    time.sleep(delay)
            
            except Exception as e:
                print(f"❌ Failed to generate {spec['number']}: {e}")
                results.append({
                    "notebook": spec['number'],
                    "status": "failed",
                    "error": str(e)
                })
        
        return results


def main():
    """Example usage"""
    
    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Set OPENAI_API_KEY environment variable")
        return
    
    workspace_root = Path(__file__).parent.parent
    
    generator = NotebookGenerator(api_key, str(workspace_root))
    
    # Example: Generate single notebook
    notebook_spec = {
        "number": "079",
        "title": "RAG_Fundamentals",
        "category": "Modern_AI",
        "topics": [
            "Retrieval-Augmented Generation architecture",
            "Vector databases and embeddings",
            "Document chunking strategies",
            "Semantic search with FAISS",
            "RAG pipeline implementation",
            "Query optimization techniques"
        ],
        "post_silicon_focus": [
            "Technical documentation search (datasheets, test specs)",
            "Failure analysis report retrieval",
            "Test parameter recommendation system",
            "Design verification query assistant"
        ],
        "prerequisites": ["078_Multimodal_LLMs", "072_GPT_Large_Language_Models"],
        "learning_objectives": [
            "Understand RAG architecture and when to use it",
            "Implement document chunking and embedding pipelines",
            "Build semantic search with vector databases",
            "Create production RAG systems with caching",
            "Apply RAG to semiconductor documentation"
        ]
    }
    
    print("🚀 Starting notebook generation...")
    output_path = generator.generate_and_save(notebook_spec)
    
    print("\n✅ Generation complete!")
    print(f"📄 Notebook saved: {output_path}")


if __name__ == "__main__":
    main()
