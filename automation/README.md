# Notebook Generation Automation

Automated system for generating high-quality AI/ML notebooks using OpenAI GPT-5.

## Features

✅ **Quality-Controlled Generation**
- Follows workspace standards (max 100 lines/cell, alternating markdown/code)
- Maintains post-silicon validation focus (60/40 split)
- Includes mathematical foundations and from-scratch implementations
- Generates Mermaid diagrams and project ideas
- Validates structure automatically

✅ **Batch Processing**
- Generate notebooks in batches with rate limiting
- Progress tracking and error handling
- Comprehensive validation reports

✅ **Production-Ready Output**
- Complete Jupyter notebooks in JSON format
- Proper metadata and kernel specifications
- Ready for immediate use and Git commits

## Setup

### 1. Install Dependencies

```bash
pip install openai
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY='your-gpt-5-api-key-here'
```

Or create a `.env` file:
```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

### 3. Verify Setup

```bash
cd automation
python notebook_generator.py
```

## Usage

### Generate Single Notebook

Edit `notebook_generator.py` and modify the `notebook_spec` in `main()`, then:

```bash
python automation/notebook_generator.py
```

### Generate Batch (Recommended)

**Generate first 5 notebooks (079-083):**
```bash
python automation/batch_generator.py 0 5
```

**Generate next 5 notebooks (084-088):**
```bash
python automation/batch_generator.py 5 5
```

**Generate all 12 Modern AI notebooks (079-090):**
```bash
python automation/batch_generator.py all
```

**Custom batch with delay:**
```bash
python automation/batch_generator.py 0 3 15  # 3 notebooks, 15s delay
```

## Workflow Recommendations

### Incremental Generation (Safest)

Generate notebooks in small batches for quality control:

```bash
# Batch 1: RAG fundamentals (079-080)
python automation/batch_generator.py 0 2

# Review generated notebooks
# Test cells manually
# Fix any issues

# Batch 2: Prompt engineering (081-083)
python automation/batch_generator.py 2 3

# Continue...
```

### Push to GitHub Every 10 Notebooks

After generating batches, commit and push:

```bash
git add 08_Modern_AI/*.ipynb
git commit -m "feat: Notebooks 079-088 - Advanced RAG and LLM techniques"
git push origin main
```

### Full Automation (Advanced)

Generate all 12 Modern AI notebooks in one go:

```bash
python automation/batch_generator.py all
```

**Estimated time:** ~25 minutes (with 10s delay between generations)

## Output Structure

Generated notebooks include:

1. **Introduction** - Overview with Mermaid workflow diagram
2. **Mathematical Foundation** - LaTeX equations with explanations
3. **From Scratch** - Educational NumPy implementation
4. **Production** - Library-based implementation (sklearn/PyTorch)
5. **Post-Silicon Examples** - Semiconductor testing use cases
6. **General AI/ML Examples** - Broader applications
7. **Evaluation** - Metrics, visualizations, diagnostics
8. **Projects** - 4-8 real-world project ideas
9. **Best Practices** - Takeaways and recommendations

## Validation

Each generated notebook is automatically validated for:

- ✅ Cell count (25-35 cells)
- ✅ Alternating markdown/code pattern
- ✅ Code cell size limits (<100 lines)
- ✅ Mermaid diagram presence
- ✅ Project section inclusion

## Quality Assurance

### Manual Review Checklist

After generation, verify:

1. **Technical Accuracy**
   - Mathematical formulas correct
   - Code runs without errors
   - Examples are realistic

2. **Post-Silicon Relevance**
   - STDF data patterns used correctly
   - Semiconductor terminology accurate
   - Use cases are practical

3. **Learning Value**
   - Progressive difficulty
   - Clear explanations
   - Hands-on examples

4. **Professional Quality**
   - No internal development references
   - Recruiter-ready content
   - Proper documentation

### Fixing Generated Notebooks

If validation fails or quality issues found:

```bash
# Open notebook
jupyter notebook 08_Modern_AI/079_RAG_Fundamentals.ipynb

# Make manual fixes
# Re-run cells to verify

# Or regenerate with modified spec
# Edit batch_generator.py NOTEBOOK_SPECS
python automation/notebook_generator.py
```

## Cost Estimation

**Using GPT-4 (until GPT-5 available):**
- ~$0.50-1.00 per notebook
- 12 notebooks (079-090): ~$6-12
- 112 remaining notebooks (079-190): ~$56-112

**Optimization:**
- Use batch processing to reduce API calls
- Cache common sections (imports, utilities)
- Reuse validated patterns

## Troubleshooting

### "OPENAI_API_KEY not set"

```bash
export OPENAI_API_KEY='your-key'
# Or add to ~/.zshrc for persistence
echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc
```

### "Workspace instructions not found"

Ensure `.github/copilot-instructions.md` exists locally:
```bash
ls .github/copilot-instructions.md
```

### "JSON decode error"

GPT may return malformed JSON. The script attempts to clean responses, but manual fixes may be needed:
- Check response for markdown code blocks
- Validate JSON syntax
- Regenerate with lower temperature

### "Validation failed"

Review specific failures:
- Code cells >100 lines: Split into smaller blocks
- Missing Mermaid: Add workflow diagram
- No projects: Add 4-8 project ideas

## Extending to Other Categories

To generate notebooks for other categories (e.g., Data Engineering 091-110):

1. Add specs to `batch_generator.py`:

```python
{
    "number": "091",
    "title": "Data_Pipeline_Fundamentals",
    "category": "Data_Engineering",
    "topics": ["ETL patterns", "Data validation", ...],
    "post_silicon_focus": ["STDF parsing", "Test data pipelines"],
    "prerequisites": ["010_Linear_Regression"]
}
```

2. Generate:

```bash
python automation/batch_generator.py 12 5  # Start from index 12
```

## Next Steps

1. **Generate Modern AI notebooks (079-090)** - 12 notebooks
2. **Generate Data Engineering (091-110)** - 20 notebooks
3. **Generate MLOps (111-130)** - 20 notebooks
4. **Generate Cloud Deployment (131-150)** - 20 notebooks
5. **Generate Advanced Topics (151-170)** - 20 notebooks
6. **Generate Specializations (171-190)** - 20 notebooks

**Total remaining:** 112 notebooks

## Maintenance

As OpenAI releases GPT-5:

1. Update `notebook_generator.py`:
   ```python
   model="gpt-5"  # Change from gpt-4
   ```

2. Adjust `max_tokens` if needed (GPT-5 may support more)

3. Fine-tune temperature (0.7 is good starting point)

## Support

For issues or improvements:
1. Check validation output for specific failures
2. Review workspace instructions in `.github/copilot-instructions.md`
3. Reference gold standard: `010_Linear_Regression.ipynb`
4. Manually fix and document patterns for future improvements
