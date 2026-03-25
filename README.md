# MedReport Translator: Patient-Friendly AI 🩺

An AI Agent System for the **ET Hackathon 2026 (Phase 2)**. 
**Problem Statement 5**: Domain-Specialized AI Agents with Compliance Guardrails.

***

## 🚀 The Solution
Medical reports are written for doctors, not patients. MedReport Translator is a multi-agent system that bridges this gap by automatically parsing PDF blood reports and transforming clinical jargon into simple, actionable insights. 

It implements a 4-Agent Workflow:
1. **Extraction Agent (VLM Simulator):** Securely extracts raw text and data from uploaded medical PDFs.
2. **Medical Agent (RAG Simulator):** Identifies key health markers (e.g., Hemoglobin, Glucose, Cholesterol), references normal ranges, and flags abnormalities.
3. **Safety Agent (Compliance Guardrail):** Enforces strict "Inform, Do Not Diagnose" policies and attaches necessary medical disclaimers. 
4. **Output Agent:** Synthesizes the final patient-friendly UI and generates suggested questions for the patient's next doctor visit.

## ✨ Key Features
* **Full Workflow Automation:** Upload a PDF → See plain-English results. No intermediate human steps required.
* **Domain Guardrails:** Hardcoded safety layers ensuring the AI never provides diagnostic advice.
* **Edge-Case Handling:** Fallback mechanisms for image-based PDFs or missing data fields.
* **Beautiful, Premium UI:** Engaging Dark Mode interface built for trust and readability, showcasing dynamic AI agent states.

## 🛠 Setup Instructions

### 1. Requirements
* Python 3.9+
* Pip

### 2. Installation
Clone the repository, then install requirements:
```bash
git clone https://github.com/YourUsername/MedReport-Translator.git
cd MedReport-Translator
pip install -r requirements.txt
```

### 3. Running the App
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`

### 4. How to Test
1. Click **Browse Files** and upload any sample PDF medical report. 
2. (For the demo, keyword matching on 'hemoglobin', 'glucose', and 'cholesterol' triggers specific visual states). 
3. Watch the multi-agent simulation pipeline activate.
4. Review the generated insights, normal/abnormal tags, and suggested doctor questions.

## 📊 Evaluation Focus Alignment
* **Domain Expertise Depth:** Focused entirely on standardizing complex biochemical marker analysis.
* **Compliance & Guardrails:** The Safety Agent is non-bypassable and hardcoded into the pipeline.
* **Full Task Completion:** Zero clicks between upload and final insight generation.

---
Built by Siddem Anil Kumar.
