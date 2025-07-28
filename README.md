# 📘 Adobe Hackathon - Round 1B: Intelligent Document Analyzer

## 🧠 Challenge Theme: “Connect What Matters — For the User Who Matters”

This repository contains our solution for Round 1B of Adobe's "Connecting the Dots" hackathon challenge. Our system analyzes a collection of documents and extracts **the most relevant sections** based on a defined **persona** and their **job-to-be-done**.

---

## 👨‍👩‍👧‍👦 Team Members

- **Chaitanya Pyla**
- **Manohar**
- **Suhel**

---

## 🚀 Problem Statement

Given:
- A set of PDFs (3–10 documents)
- A persona (e.g., researcher, student, analyst)
- A job-to-be-done (e.g., literature review, summarization)

> 📌 Objective: Identify and rank the **most relevant sections** and **sub-sections** from the documents that align with the persona’s goal.

---

## ⚙️ How It Works

1. **Preprocessing:**
   - Extract text content from all PDFs.
   - Detect and normalize headings and paragraphs using layout and font analysis.

2. **Persona Understanding:**
   - Parse the persona and job-to-be-done into a keyword vector using embeddings.

3. **Section Relevance Ranking:**
   - Compare each section’s content with the persona-task vector using cosine similarity (via TF-IDF or sentence transformers).
   - Assign importance ranks based on match score.

4. **Sub-section Analysis:**
   - Drill down into sub-paragraphs within the top-ranked sections for deeper relevance extraction.

5. **Output JSON:**
   - Generates structured JSON with metadata, ranked sections, and refined sub-sections.

---

## 📥 Input Format

- `/input`: Folder with 3–10 PDF documents
- `persona.txt`: Text file describing the user persona
- `job.txt`: Description of the task to be performed

---

## 📤 Output Format (JSON)

```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare a comprehensive literature review...",
    "timestamp": "2025-07-28T18:20:00"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page_number": 2,
      "section_title": "Graph Neural Networks Overview",
      "importance_rank": 1
    }
  ],
  "sub_section_analysis": [
    {
      "document": "doc1.pdf",
      "page_number": 2,
      "refined_text": "GNNs have shown significant promise in molecular structure analysis..."
    }
  ]
}
