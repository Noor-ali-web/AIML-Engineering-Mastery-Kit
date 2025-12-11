#!/usr/bin/env python3
"""
Batch Notebook Generator
Generates remaining notebooks (079-190) in organized batches
"""

import os
from pathlib import Path
from notebook_generator import NotebookGenerator

# Notebook specifications for remaining notebooks
NOTEBOOK_SPECS = [
    # 08_Modern_AI (079-090)
    {
        "number": "079",
        "title": "RAG_Fundamentals",
        "category": "Modern_AI",
        "topics": [
            "Retrieval-Augmented Generation architecture",
            "Vector databases and embeddings",
            "Document chunking strategies",
            "Semantic search with FAISS/Pinecone",
            "RAG pipeline implementation",
            "Query optimization and caching"
        ],
        "post_silicon_focus": [
            "Technical documentation search (datasheets, test specs)",
            "Failure analysis report retrieval system",
            "Test parameter recommendation engine",
            "Design verification query assistant"
        ],
        "prerequisites": ["078_Multimodal_LLMs", "072_GPT_Large_Language_Models"]
    },
    {
        "number": "080",
        "title": "Advanced_RAG_Techniques",
        "category": "Modern_AI",
        "topics": [
            "Hybrid search (dense + sparse)",
            "Query rewriting and expansion",
            "Re-ranking strategies",
            "Context compression techniques",
            "Multi-hop reasoning",
            "RAG evaluation metrics"
        ],
        "post_silicon_focus": [
            "Multi-document correlation analysis",
            "Cross-test failure pattern detection",
            "Historical data contextualization",
            "Intelligent test coverage recommendations"
        ],
        "prerequisites": ["079_RAG_Fundamentals"]
    },
    {
        "number": "081",
        "title": "Prompt_Engineering_Advanced",
        "category": "Modern_AI",
        "topics": [
            "Advanced prompting techniques (CoT, ToT, ReAct)",
            "Few-shot and zero-shot learning",
            "Instruction tuning strategies",
            "Prompt optimization frameworks",
            "Prompt injection and security",
            "Prompt versioning and A/B testing"
        ],
        "post_silicon_focus": [
            "Automated test failure root cause prompts",
            "Yield analysis report generation",
            "Parametric correlation explanation prompts",
            "Design review assistance prompts"
        ],
        "prerequisites": ["072_GPT_Large_Language_Models"]
    },
    {
        "number": "082",
        "title": "LLM_Fine_Tuning",
        "category": "Modern_AI",
        "topics": [
            "Full fine-tuning vs PEFT methods",
            "LoRA and QLoRA implementations",
            "Dataset preparation and quality",
            "Training monitoring and evaluation",
            "Catastrophic forgetting mitigation",
            "Deployment considerations"
        ],
        "post_silicon_focus": [
            "Domain-specific semiconductor terminology fine-tuning",
            "Custom failure analysis models",
            "Test specification comprehension models",
            "Manufacturing yield prediction fine-tuning"
        ],
        "prerequisites": ["072_GPT_Large_Language_Models", "061_RLHF_Instruction_Following"]
    },
    {
        "number": "083",
        "title": "AI_Agents_Fundamentals",
        "category": "Modern_AI",
        "topics": [
            "Agent architectures (ReAct, AutoGPT, BabyAGI)",
            "Tool use and function calling",
            "Memory systems (short-term, long-term)",
            "Planning and reasoning loops",
            "Multi-agent systems",
            "Agent evaluation frameworks"
        ],
        "post_silicon_focus": [
            "Automated test debug agent",
            "Yield optimization agent system",
            "Multi-agent failure analysis team",
            "Design-for-test recommendation agent"
        ],
        "prerequisites": ["081_Prompt_Engineering_Advanced", "079_RAG_Fundamentals"]
    },
    {
        "number": "084",
        "title": "LangChain_LlamaIndex",
        "category": "Modern_AI",
        "topics": [
            "LangChain framework fundamentals",
            "LlamaIndex for document processing",
            "Chain composition patterns",
            "Agent executors and tools",
            "Memory management",
            "Production deployment patterns"
        ],
        "post_silicon_focus": [
            "Automated test documentation pipeline",
            "Failure database query interface",
            "Design knowledge base system",
            "Manufacturing data analysis chatbot"
        ],
        "prerequisites": ["079_RAG_Fundamentals", "083_AI_Agents_Fundamentals"]
    },
    {
        "number": "085",
        "title": "Vector_Databases",
        "category": "Modern_AI",
        "topics": [
            "Vector database fundamentals (FAISS, Pinecone, Weaviate)",
            "Indexing strategies (IVF, HNSW, PQ)",
            "Similarity search algorithms",
            "Hybrid search implementations",
            "Metadata filtering and faceting",
            "Performance optimization"
        ],
        "post_silicon_focus": [
            "Test parameter similarity search",
            "Wafer map pattern matching",
            "Historical failure case retrieval",
            "Design pattern similarity analysis"
        ],
        "prerequisites": ["079_RAG_Fundamentals"]
    },
    {
        "number": "086",
        "title": "LLM_Evaluation_Benchmarking",
        "category": "Modern_AI",
        "topics": [
            "Automatic evaluation metrics (BLEU, ROUGE, BERTScore)",
            "Human evaluation frameworks",
            "Benchmark datasets and tasks",
            "A/B testing methodologies",
            "Cost-performance tradeoffs",
            "Model selection criteria"
        ],
        "post_silicon_focus": [
            "Failure report quality assessment",
            "Test coverage recommendation evaluation",
            "Documentation generation benchmarks",
            "Query response accuracy metrics"
        ],
        "prerequisites": ["072_GPT_Large_Language_Models", "081_Prompt_Engineering_Advanced"]
    },
    {
        "number": "087",
        "title": "Guardrails_Safety_LLMs",
        "category": "Modern_AI",
        "topics": [
            "Input/output validation frameworks",
            "Content filtering and moderation",
            "Bias detection and mitigation",
            "Hallucination detection",
            "Fact-checking pipelines",
            "Safety layers and circuit breakers"
        ],
        "post_silicon_focus": [
            "Test specification validation guardrails",
            "Manufacturing data privacy protection",
            "Failure analysis accuracy verification",
            "Design recommendation safety checks"
        ],
        "prerequisites": ["072_GPT_Large_Language_Models", "083_AI_Agents_Fundamentals"]
    },
    {
        "number": "088",
        "title": "Semantic_Search_Embeddings",
        "category": "Modern_AI",
        "topics": [
            "Embedding models (Sentence-BERT, OpenAI, Cohere)",
            "Fine-tuning embeddings for domain",
            "Semantic similarity metrics",
            "Cross-encoder re-ranking",
            "Multilingual embeddings",
            "Embedding visualization"
        ],
        "post_silicon_focus": [
            "Test failure semantic clustering",
            "Design document similarity search",
            "Multi-language specification search",
            "Parameter correlation semantic analysis"
        ],
        "prerequisites": ["079_RAG_Fundamentals", "085_Vector_Databases"]
    },
    {
        "number": "089",
        "title": "LLM_Serving_Optimization",
        "category": "Modern_AI",
        "topics": [
            "Model serving frameworks (vLLM, TGI, TensorRT-LLM)",
            "Batching strategies",
            "KV cache optimization",
            "Quantization for inference",
            "Load balancing and scaling",
            "Cost optimization techniques"
        ],
        "post_silicon_focus": [
            "High-throughput failure analysis service",
            "Real-time test assistance system",
            "Batch documentation processing",
            "Cost-effective manufacturing insights"
        ],
        "prerequisites": ["072_GPT_Large_Language_Models", "068_Model_Compression_Quantization"]
    },
    {
        "number": "090",
        "title": "Agentic_Workflows",
        "category": "Modern_AI",
        "topics": [
            "Workflow orchestration patterns",
            "Task decomposition strategies",
            "Human-in-the-loop systems",
            "Error handling and recovery",
            "Workflow monitoring and logging",
            "Production deployment patterns"
        ],
        "post_silicon_focus": [
            "Automated yield investigation workflow",
            "Multi-stage failure analysis pipeline",
            "Design review automation workflow",
            "Test coverage optimization flow"
        ],
        "prerequisites": ["083_AI_Agents_Fundamentals", "084_LangChain_LlamaIndex"]
    }
]

def generate_batch(start_idx: int = 0, count: int = 5, delay: int = 10):
    """
    Generate notebooks in batches
    
    Args:
        start_idx: Starting index in NOTEBOOK_SPECS
        count: Number of notebooks to generate
        delay: Delay between generations (seconds)
    """
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Set OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='your-key-here'")
        return
    
    workspace_root = Path(__file__).parent.parent
    generator = NotebookGenerator(api_key, str(workspace_root))
    
    batch = NOTEBOOK_SPECS[start_idx:start_idx + count]
    
    print(f"🚀 Generating {len(batch)} notebooks")
    print(f"   Range: {batch[0]['number']} - {batch[-1]['number']}")
    print(f"   Delay: {delay}s between generations")
    print(f"{'='*60}\n")
    
    results = generator.generate_batch(batch, delay=delay)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 BATCH SUMMARY")
    print(f"{'='*60}")
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    failed_count = len(results) - success_count
    
    print(f"✅ Successful: {success_count}/{len(results)}")
    print(f"❌ Failed: {failed_count}/{len(results)}")
    
    if failed_count > 0:
        print("\nFailed notebooks:")
        for r in results:
            if r['status'] == 'failed':
                print(f"  - {r['notebook']}: {r['error']}")
    
    return results


def generate_all_modern_ai():
    """Generate all Modern AI notebooks (079-090)"""
    print("🎯 Generating ALL Modern AI notebooks (079-090)")
    print("   Total: 12 notebooks")
    print("   Estimated time: ~25 minutes (with 10s delay)")
    
    confirm = input("\nProceed? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return
    
    return generate_batch(start_idx=0, count=12, delay=10)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python batch_generator.py all              # Generate all 12 Modern AI notebooks")
        print("  python batch_generator.py 0 5              # Generate notebooks 0-4 (079-083)")
        print("  python batch_generator.py 5 5 15           # Generate notebooks 5-9, 15s delay")
        sys.exit(1)
    
    if sys.argv[1] == 'all':
        generate_all_modern_ai()
    else:
        start = int(sys.argv[1])
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        delay = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        generate_batch(start, count, delay)
