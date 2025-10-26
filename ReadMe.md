# 🧠 Prompt Variance Analyzer

**Prompt Variance Analyzer** is a tool for visualizing and quantifying the variability of Large Language Model (LLM) outputs under a fixed system prompt, rubric, or plan.  
It allows AI engineers and prompt designers to empirically study the *distribution* of generated responses rather than relying on one or two subjective samples.

---

## 🚀 Overview

When developing prompt-based AI systems (such as rubric-driven document analyzers or plan-guided reasoning chains), it’s often unclear how consistent or diverse the model’s outputs are.  
This tool provides a statistical and visual perspective:

1. **Runs an LLM N times** with a given rubric or system prompt.
2. **Embeds** each output in semantic space.
3. **Projects** embeddings to 2D for visualization.
4. **Identifies** the centroid (average semantic meaning).
5. **Displays** the average output and lets users inspect all samples interactively.

This approach borrows from **quantum algorithm analysis**, where probabilistic results are run thousands of times and aggregated into a distribution to understand overall system behavior.

---

## ✨ Core Features

- 🔁 Run an LLM multiple times with the same prompt/rubric
- 🧭 Compute semantic embeddings for each response
- 📊 Visualize the distribution of outputs in 2D space
- 🧩 Identify the centroid and nearest representative output
- 🖱️ Click any data point to view its corresponding text
- 🧮 Quantitative insight into prompt stability, variance, and clustering

---

## 🏗️ Architecture

The project is built in two layers:


### **Backend**
- Written in **Python (FastAPI)**
- Handles orchestration of multiple LLM calls, embedding generation, and variance analysis
- Supports both **internal orchestrator APIs** and **external LLM providers** (OpenAI, Azure, etc.)
- Provides JSON results containing embeddings, centroid output, and all sample texts

### **Frontend**
- Implemented in **Streamlit** (for MVP)
- Handles prompt/rubric input, optional document upload, and visualizes embeddings using Plotly
- Interactive visualization allows exploring each sample output directly on the plot