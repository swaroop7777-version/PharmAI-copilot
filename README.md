click this repo for  full pharmaAI CODE AND TO USE OUR AI: https://github.com/keilahchemu7/pharmaaiaccelerator

live AI Application: https://pharmaaiaccelerator.lovable.app

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
