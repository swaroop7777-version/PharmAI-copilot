click this repo for  full pharmaAI CODE AND TO USE OUR AI: https://github.com/keilahchemu7/pharmaaiaccelerator

click here for using live AI Application: https://pharmaaiaccelerator.lovable.app

Pharma AI: AI-Powered Regulatory Compliance Assistant
Pharma AI is an intelligent assistant designed to transform the traditionally slow Medical-Legal-Regulatory (MLR) review process. By bridging the gap between creative design and strict pharmaceutical standards, the platform allows teams to generate, audit, and validate marketing content in seconds rather than weeks. The system functions as a digital bridge where brand consistency meets regulatory safety, ensuring that every landing page or marketing brief adheres to global standards before it ever reaches a human legal team.

The Problem and Our Solution
The current pharmaceutical landscape suffers from massive bottlenecks in content approval. Designers and developers often work in silos, leading to multiple rounds of revisions when content fails to meet fair balance or safety disclosure requirements. Pharma AI solves this by implementing an automated auditing engine. By using a "Human-in-the-Loop" workflow, the AI provides real-time compliance scoring and remediation guidance, allowing teams to identify and fix legal risks at the moment of creation.

Intelligent Content and Multi-Market Auditing
The application empowers users to generate pharma-compliant landing pages from a simple brief, such as a campaign for Paracetamol 500mg. The AI doesn't just generate marketing copy; it produces a full suite of necessary components including headlines, clinical benefits, and mandatory safety disclosures. Once content is generated, the system audits it against specific international standards, including the UK MHRA, USA FDA, and Japan PMDA. It meticulously checks for the "Fair Balance" of risks and benefits, mandatory statutory cautions, and proper contraindication warnings.

A Multi-Persona Collaborative Engine
What sets Pharma AI apart is its ability to analyze content from three distinct professional perspectives. The Designer persona evaluates visual clarity and structural hierarchy; the Developer persona ensures technical accessibility and clean code; and the QA/Regulatory persona flags specific legal risks while providing a final Compliance Score. This holistic approach ensures that the output is not just legally sound, but also technically functional and aesthetically professional.

Technical Architecture and Data Privacy
The project is built on a sophisticated Local-Cloud Hybrid architecture. We utilize a Lovable AI (React/Vite) frontend that communicates through a secure ngrok tunnel to a local Python Flask backend. At the heart of the system is Ollama (running Llama 3.2), which processes data against custom regulatory text files. This setup is crucial for the pharmaceutical industry because it ensures full data sovereignty. Sensitive drug briefs and proprietary information are processed locally on the machine, meaning no data is ever transmitted to external AI APIs, maintaining strict alignment with corporate security policies.

Pharma AI – AI-Powered Regulatory Compliance Assistant

Pharma AI is an AI-powered Medical-Legal-Regulatory (MLR) assistant designed to help pharmaceutical teams generate and audit marketing content while ensuring compliance with regulatory standards.

The system automatically evaluates landing pages and marketing briefs against pharmaceutical regulatory rules and provides compliance scores, explanations, and remediation guidance.

This reduces the traditional weeks-long review process between designers, developers, and regulatory teams to seconds.

⸻

Key Features

AI Landing Page Generation

Generate pharmaceutical marketing landing page content from a simple campaign brief.

Example input:
Create a landing page for Zyloprin, a hypertension medication.

The AI generates:
	•	Product headline
	•	Medical description
	•	Clinical benefits
	•	Safety information
	•	References

⸻

Regulatory Compliance Auditing

The system audits generated or existing content against regulatory frameworks.

Supported markets:
	•	UK – MHRA
	•	USA – FDA
	•	Japan – PMDA

The AI checks for:
	•	Fair balance between benefits and risks
	•	Safety disclosures
	•	Proper references and citations
	•	Accessibility and design clarity
	•	Technical compliance

⸻

Compliance Score:
Compliance Score: 92
Market: UK (MHRA)

Multi-Persona AI Review

The system analyzes the content from three perspectives.

Designer
Evaluates visual clarity and content structure.

Developer
Checks accessibility and technical implementation.

QA / Regulatory
Reviews regulatory risks and compliance issues.

⸻

Actionable Feedback

Instead of only identifying problems, the system provides clear remediation guidance.

Example:
QA / Regulatory
The page lacks adequate safety information.
Add contraindications and prescribing details
to achieve fair balance.

Architecture

The project uses a local-cloud hybrid AI architecture.

Frontend (Lovable UI)
        ↓
Ngrok Secure Tunnel
        ↓
Python Flask Backend
        ↓
Ollama Local LLM
        ↓
Regulatory Rule Engine
        ↓
Compliance Score + Feedback

Technology Stack

Frontend

Lovable AI (UI builder)

Backend

Python
Flask API

AI Model

Ollama
Llama 3.2

Connectivity

Ngrok secure tunnel

Regulatory Data

Custom rule files

regulations/
  uk_mhra.txt
  usa_fda.txt
  japan_pmda.txt

  pharma-ai
│
├── backend
│   └── app.py
│
├── regulations
│   ├── uk_mhra.txt
│   ├── usa_fda.txt
│   └── japan_pmda.txt
│
├── requirements.txt
│
└── README.md

Security and Privacy

The system uses local AI processing via Ollama, ensuring that sensitive pharmaceutical data is not transmitted to external APIs.

Benefits:
	•	Data privacy
	•	Offline capability
	•	Lower operational cost
	•	Faster inference

⸻

Future Improvements

Planned enhancements include:
	•	Integration with regulatory systems like Veeva Vault
	•	Predictive regulatory risk scoring
	•	Automated AI content correction
	•	Enterprise cloud deployment
	•	RLHF training with legal feedback

⸻

Use Cases

Pharma AI can assist with:
	•	pharmaceutical marketing compliance
	•	regulatory review automation
	•	medical content auditing
	•	pharma digital campaign approval
	•	healthcare website compliance

⸻

Contributing

Contributions are welcome.

Steps:

1 Fork the repository
2 Create a feature branch
3 Submit a pull request
