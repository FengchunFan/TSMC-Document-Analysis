# ChatGPT Closed Domain Question Answering (CDQA)

This repository implements a **Retrieval-Augmented Generation (RAG)** system to support grounded and efficient research on complex questions such as TSMC’s motivations for operations in the United States. The system allows users to ask natural-language questions and receive semantically relevant, context-aware answers backed by article evidence.

---

## 🔍 Retrieval-Augmented Generation (RAG)

Our system follows the standard RAG framework, which enhances language models by incorporating relevant external content at inference time. This approach ensures up-to-date, verifiable, and well-scoped answers.

**Pipeline Overview ([adapted from Gao et al., 2024](https://arxiv.org/abs/2312.10997)):**

1. **Indexing:**  
   - Raw documents are minimally cleaned and split into sentence-level chunks.
   - Each sentence is embedded using the `all-mpnet-base-v2` model from Sentence-BERT.
   - Vectors are stored in a FAISS index (IndexFlatIP with cosine similarity).
   - Associated metadata, like article titles, are retained for traceability.

2. **Retrieval:**  
   - User queries are embedded using the same model.
   - FAISS returns top-k similar sentences with a cosine similarity threshold of 0.6.
   - To provide context, we expand the result with 2 sentences before and after the matched sentence.

3. **Generation (Optional):**  
   - Retrieved passages are input to an LLM with a strict prompt that limits generation to only the retrieved context.
   - Summarization improves readability while avoiding hallucination.
   - The original evidence remains accessible for verification.

---

## 🧠 System Architecture

![System Structure](/Screenshot/System%20Structure.png)

- **Corpus Source:** Articles were collected from Nexis Uni and major U.S. outlets like WSJ, NYT, and WaPo.
- **Preprocessing:** Line breaks normalized; stopword removal and lowercasing avoided to preserve semantic structure.
- **Embedding:** Sentence-BERT's MPNet model generates dense vectors for semantic matching.
- **Storage:** FAISS index ensures fast and accurate retrieval.
- **Context Expansion:** Each retrieved sentence is returned with surrounding text for contextual fidelity.
- **Output:** Both raw results and optionally LLM-synthesized explanations are provided to users.

---

## 🖼️ RAG Pipeline Illustration

![RAG pipeline](/Screenshot/RAG%20pipeline.png)

Adapted from Gao et al. (2024), the pipeline reflects our approach: indexing, retrieval, and LLM-based generation.

---

## 🧪 Topic Modeling (Alternative Approach)

As an alternate strategy, we applied **BERTopic** to perform unsupervised topic modeling on our corpus to uncover underlying themes. We followed best practices by avoiding aggressive preprocessing—maintaining punctuation and stopwords for optimal transformer embedding.

However, **topic modeling was ultimately insufficient** for our task, providing limited value in answering precise, document-grounded queries. Thus, our final pipeline centers around semantic retrieval and generation instead.

Topic modeling experimentation is available in:
```
Document_Analyzer_BERTopic.ipynb
```

---

## 📁 File Structure

- `Chatgpt_CDQA.ipynb` – Main notebook for semantic search and RAG pipeline.
- `/Screenshot/` – Contains:
  - `System Structure.png` – Our pipeline architecture.
  - `RAG pipeline.png` – Standard RAG flow adapted from Gao et al. (2024).
- `Document_Analyzer_BERTopic.ipynb` – Topic modeling code with BERTopic.

---

## 📚 Main References

- Gao et al. (2024). Retrieval-Augmented Generation for Large Language Models: A Survey. [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)  
- Reimers & Gurevych (2019). Sentence-BERT: [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)  
- Sentence-BERT Official Website: [https://sbert.net/](https://sbert.net/) 
- FAISS documentation: [https://faiss.ai](https://faiss.ai)  
- BERTopic Tips: [Grootendorst Documentation](https://maartengr.github.io/BERTopic/getting_started/tips_and_tricks/tips_and_tricks.html)