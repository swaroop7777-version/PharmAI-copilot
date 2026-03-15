import ollama
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Increase max content length to handle full website HTML transfers
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# THE WINNING "MULTI-PERSONA" PROMPT
SYSTEM_PROMPT = (
    "You are an AI expert panel consisting of a Lead Designer, a Senior Developer, and a Pharma Regulatory QA. "
    "Your task is to audit web content for strict Pharmaceutical industry standards.\n\n"
    "CRITERIA FOR EVALUATION:\n"
    "1. DESIGNER: Check brand consistency and visual hierarchy. Ensure no 'medical miracle' imagery.\n"
    "2. DEVELOPER: Check WCAG AA accessibility (contrast 4.5:1), alt-text, and semantic HTML (H1-H2-H3 flow).\n"
    "3. QA/REGULATORY: Check for 'Fair Balance' (Safety info must be prominent), Exit Disclaimers on external links, "
    "and proper medical citations [1].\n\n"
    "STRICT OUTPUT FORMAT:\n"
    "You must return your response in this exact structure so the frontend can parse it:\n"
    "DESIGNER: [Feedback + Justification]\n"
    "DEVELOPER: [Feedback + Justification]\n"
    "QA/REGULATORY: [Feedback + Justification]\n"
    "SCORE: [A single number 0-100]"
)


@app.route('/process', methods=['POST'])
def handle_ai_task():
    # 1. Get the data from Lovable
    data = request.get_json()
    print(f"\n--- DATA RECEIVED: {data} ---")

    # 2. Smart Extraction
    user_input = data.get('content') or data.get('brief') or data.get('prompt')
    mode = data.get('mode', 'generate')

    # 3. Emergency Demo Fallback
    if not user_input or user_input == "":
        user_input = "Create a medical landing page for Zyloprin (hypertension). Focus on doctors."
        print("!!! No input found, forcing Zyloprin Demo Mode !!!")

    # 4. Prompt Logic
    if mode == 'audit':
        user_prompt = f"""
AUDIT THIS WEBPAGE FOR PHARMA COMPLIANCE.

CONTENT:
{user_input}

Evaluate using these personas:

DESIGNER:
Check visual hierarchy, CTA clarity, and brand safety.

DEVELOPER:
Check WCAG accessibility, alt text, semantic HTML.

QA/REGULATORY:
Check fair balance, safety disclosures, citations.

Return in EXACT format:

DESIGNER: ...
DEVELOPER: ...
QA/REGULATORY: ...
SCORE: number between 0-100
"""
    else:
        user_prompt = f"""
You are a pharmaceutical marketing copywriter.

Generate compliant landing page content.

Return structured sections exactly like this:

TITLE:
HERO_TEXT:
BENEFITS:
SAFETY_INFORMATION:
REFERENCES:

Then perform a compliance evaluation using these personas:

DESIGNER:
DEVELOPER:
QA/REGULATORY:
SCORE:

BRIEF:
{user_input}
"""

    try:
        print(f"Ollama is thinking about: {user_input[:50]}...")

        response = ollama.chat(
            model='llama3.2',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_prompt}
            ]
        )

        raw_text = response['message']['content']
        print(f"AI FINISHED: {raw_text[:200]}...")

        # Extract Score
        import re
        score = 65
        score_match = re.search(r"SCORE:\s*(\d+)", raw_text)
        if score_match:
            score = int(score_match.group(1))

        return jsonify({
            "result": raw_text,
            "score": score
        })

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Ensure this is the very last part of the file
    print("--- PHARMA AI BACKEND STARTING ---")
    print("Listening on port 5000...")
    app.run(host='0.0.0.0', port=5001, debug=False)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "RegulaFlow backend is running ✅", "port": 5001})
