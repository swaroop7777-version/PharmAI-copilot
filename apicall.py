import ollama
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


# -----------------------------
# Load regulation rules
# -----------------------------

def load_rules(market):
    files = {
        "UK": "regulations/uk_mhra.txt",
        "USA": "regulations/usa_fda.txt",
        "JAPAN": "regulations/japan_pmda.txt"
    }

    path = files.get(market, "regulations/uk_mhra.txt")

    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return "Follow strict pharmaceutical safety, disclosure, and citation rules."


# -----------------------------
# Extract drug name from brief
# -----------------------------

def extract_drug_name(text):
    match = re.search(r'for\s+([A-Za-z0-9\-]+)', text, re.IGNORECASE)

    if match:
        return match.group(1).strip(",.")

    return "the medication"


# -----------------------------
# API Endpoint
# -----------------------------

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()

    user_input = data.get('content') or data.get('brief') or ""
    mode = data.get('mode', 'generate')
    market = data.get('market', 'UK')

    if isinstance(market, dict):
        market = market.get("value", "UK")

    rules = load_rules(market)

    if not user_input:
        user_input = "Create a landing page for Zyloprin, a hypertension medication for healthcare professionals."

    drug_name = extract_drug_name(user_input)

    # -----------------------------
    # AUDIT MODE
    # -----------------------------

    if mode == "audit":

        prompt = f"""
You are a pharmaceutical compliance auditor.

Market: {market}

Regulatory Compliance Rules:
{rules}

Audit the following webpage content.

CONTENT:
{user_input}

Return results using this exact structure.

RULE CHECK RESULTS
Check 1 - PASS or FAIL
Check 2 - PASS or FAIL
Check 3 - PASS or FAIL
Check 4 - PASS or FAIL
Check 5 - PASS or FAIL
Check 6 - PASS or FAIL
Check 7 - PASS or FAIL

DESIGNER
Explain layout or branding issues.

DEVELOPER
Explain accessibility or technical issues.

QA / REGULATORY
Explain compliance risks and how to fix them.

SCORE:
Return one number between 0 and 100.
"""

    # -----------------------------
    # GENERATION MODE
    # -----------------------------

    else:

        prompt = f"""
You are an expert pharmaceutical marketing copywriter and regulatory reviewer.

Drug Name: {drug_name}
Market: {market}

Regulatory Rules:
{rules}

TASK
Generate compliant landing page marketing content for healthcare professionals.

IMPORTANT
Do NOT generate UI instructions like:
- logo
- navigation menu
- CTA layout

Write real marketing content.

Return ONLY these sections.

TITLE
Clear product headline.

HERO_TEXT
Short description explaining what {drug_name} treats.

BENEFITS
3–4 bullet points describing clinical benefits.

SAFETY_INFORMATION
Important safety warnings, contraindications, and disclaimers.

REFERENCES
1–2 placeholder scientific citations.

Then perform a compliance audit.

RULE CHECK RESULTS
Check 1 - PASS or FAIL
Check 2 - PASS or FAIL
Check 3 - PASS or FAIL
Check 4 - PASS or FAIL
Check 5 - PASS or FAIL
Check 6 - PASS or FAIL
Check 7 - PASS or FAIL

DESIGNER
Comment on visual clarity.

DEVELOPER
Comment on accessibility and HTML structure.

QA / REGULATORY
Explain compliance considerations.

SCORE:
Return one number between 0 and 100.

BRIEF:
{user_input}
"""

    # -----------------------------
    # System prompt (strong control)
    # -----------------------------

    system_prompt = """
You are a strict pharmaceutical AI reviewer.

Never output UI instructions like:
'logo', 'navigation menu', 'hero image'.

Only produce professional pharmaceutical marketing copy and compliance analysis.
"""

    try:

        response = ollama.chat(
            model='llama3.2',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0.2
            }
        )

        raw_text = response['message']['content']

        score_match = re.search(r"SCORE:\s*(\d+)", raw_text)
        score = int(score_match.group(1)) if score_match else 70

        return jsonify({
            "result": raw_text,
            "score": score,
            "market": market
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# Start Server
# -----------------------------

if __name__ == "__main__":
    print("Pharma AI backend running on port 5001")
    app.run(host="0.0.0.0", port=5001)