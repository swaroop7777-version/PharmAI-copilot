import ollama
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# --------------------------------
# Load regulation rules from files
# --------------------------------

def load_rules(market):

    files = {
        "UK": "regulations/uk_mhra.txt",
        "USA": "regulations/usa_fda.txt",
        "JAPAN": "regulations/japan_pmda.txt"
    }

    path = files.get(market, "regulations/uk_mhra.txt")

    with open(path, "r") as f:
        return f.read()


# --------------------------------
# Main API
# --------------------------------

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
        user_input = "Create a landing page for a diabetes medication."

    drug_match = re.search(r'for\s+([A-Za-z0-9\-]+)', user_input)
    drug_name = drug_match.group(1) if drug_match else "the medication"

    if mode == "audit":

        prompt = f"""
You are a pharmaceutical compliance auditor.

Regulatory Compliance Checks:
{rules}

Audit the following page content.

CONTENT:
{user_input}

Return results using this structure:

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

SCORE
Return one number between 0 and 100.
"""

    else:

        prompt = f"""
You are a pharmaceutical marketing AI.

Drug name: {drug_name}

Regulatory Compliance Checks:
{rules}

Generate a compliant pharmaceutical landing page.

Return these sections exactly:

COMPONENTS
List recommended UI components for this page.

TITLE
HERO_TEXT
BENEFITS
SAFETY_INFORMATION
REFERENCES

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
DEVELOPER
QA / REGULATORY

SCORE
Return one number between 0 and 100.

BRIEF:
{user_input}
"""

    try:

        response = ollama.chat(
            model='llama3.2',
            messages=[{"role": "user", "content": prompt}]
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


if __name__ == "__main__":
    print("Pharma AI backend running on port 5001")
    app.run(host="0.0.0.0", port=5001)