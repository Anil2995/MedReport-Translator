# 3-Minute Demo Video Script: MedReport Translator

## [0:00 - 0:30] The Problem & Solution
**(Camera on You)**
"Hello! I am Siddem Anil Kumar. For the ET Hackathon Phase 2, my team addressed Problem Statement 5: Domain-Specialized AI Agents with Compliance Guardrails.
Medical reports are written for doctors, but 90% of patients struggle to understand them, causing anxiety and draining hospital resources with clarification calls. 
Our solution is **MedReport Translator**: A multi-agent AI system that transforms dense clinical blood work into actionable, patient-friendly insights, all while strictly adhering to non-diagnostic safety rules."

## [0:30 - 1:15] Demo: Upload & Mult-Agent Simulation
**(Screen Recording of the App Dashboard)**
"Let's look at the prototype. The UI is designed to be highly accessible and reassuring. I will upload a standard PDF lab report here.
Notice what happens: instead of a black box, the user sees our 4-agent pipeline working in real-time.
First, the **Extraction Agent** pulls unstructured text from the PDF.
Second, the **Medical Agent**, theoretically grounded in MedlinePlus RAG data, translates the terminology.
Crucially, the **Safety & Compliance Agent** acts as an impassable guardrail, ensuring no diagnostic language slips through."

## [1:15 - 2:20] Demo: The Explanations & Guardrails
**(Screen Recording: The Results View)**
"Here is the translated report. The clinical jargon is gone. 
Our agent recognized 'Hemoglobin' and instead of just showing '11.2', it explains what hemoglobin is, flags it as 'Abnormal' with a clear color code, and tells the patient why it matters.
On the right, we have two profound features:
1. **Suggested Doctor Questions:** Our Output Agent read the 'Abnormal' tag and proactively generated questions like 'What dietary changes should I make?'
2. **Responsible AI Guardrails:** The mandatory disclaimer created by our Safety Agent is locked on screen. We inform, we never diagnose."

## [2:20 - 3:00] Business Impact & Conclusion
**(Camera on You / Slide of Impact Model)**
"Why does this matter to enterprises? Our impact model shows that by deploying this alongside digital patient portals, clinics can reduce post-test clarification calls by 60%. That saves an estimated 32 hours of nursing time per clinic per month—translating to over $500,000 in operational savings annually for a mid-sized network.
We built this with Python, Flask, and an Agentic framework because patient clarity is the future of healthcare. Thank you!"
