import ollama
import re
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

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
    path = files.get(market.upper(), "regulations/uk_mhra.txt")
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        defaults = {
            "UK": "MHRA rules: Include black triangle ▼ for new medicines. Mandatory ISI footer. No unsubstantiated efficacy claims. WCAG 2.1 AA accessibility required.",
            "USA": "FDA rules: Include full prescribing information link. Fair Balance required. Risk information must be prominent. No superiority claims without head-to-head data.",
            "JAPAN": "PMDA rules: Japanese regulatory approval number required. All claims must reference Japanese clinical trial data. Mandatory adverse event reporting section."
        }
        return defaults.get(market.upper(), defaults["UK"])

# -----------------------------
# Extract drug name from brief
# -----------------------------
def extract_drug_name(text):
    match = re.search(r"for\s+([A-Za-z0-9\-]+)", text, re.IGNORECASE)
    return match.group(1).strip(",.") if match else "the medication"

# -----------------------------
# Parse tidy fix list from raw text
# -----------------------------
def extract_fix_list(raw_text):
    fixes = []
    lines = raw_text.split("\n")
    for line in lines:
        if re.search(r"FAIL", line, re.IGNORECASE):
            clean = re.sub(r"Check\s*\d+\s*[-–]?\s*FAIL:?\s*", "", line, flags=re.IGNORECASE).strip()
            if clean:
                fixes.append(clean)
    return fixes[:5]

# -----------------------------
# Parse rule check results
# -----------------------------
def extract_rule_checks(raw_text):
    checks = []
    lines = raw_text.split("\n")
    for line in lines:
        match = re.search(r"Check\s*(\d+)\s*[-–]?\s*(PASS|FAIL):?\s*(.*)", line, re.IGNORECASE)
        if match:
            checks.append({
                "number": int(match.group(1)),
                "status": match.group(2).upper(),
                "description": match.group(3).strip()
            })
    return checks

# -----------------------------
# Parse role sections from raw text
# -----------------------------
def extract_role_sections(raw_text):
    sections = {}
    roles = ["DESIGNER", "DEVELOPER", "QA / REGULATORY", "LEGAL"]
    for i, role in enumerate(roles):
        next_role = roles[i + 1] if i + 1 < len(roles) else "SCORE"
        pattern = rf"{re.escape(role)}\s*\n(.*?)(?={re.escape(next_role)}|\Z)"
        match = re.search(pattern, raw_text, re.DOTALL | re.IGNORECASE)
        sections[role] = match.group(1).strip() if match else ""
    return sections

# -----------------------------
# Clean HTML helper
# -----------------------------
def clean_html(raw):
    raw = re.sub(r"```html\n?", "", raw)
    raw = re.sub(r"```\n?", "", raw)
    return raw.strip()

# -----------------------------
# Health check
# -----------------------------
@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "✅ RegulaFlow backend running",
        "version": "3.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": ["/process", "/generate-html", "/apply-fixes", "/health"]
    })

# -----------------------------
# Main process endpoint
# -----------------------------
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    user_input = data.get("content") or data.get("brief") or ""
    mode = data.get("mode", "generate")
    market = data.get("market", "UK")

    if isinstance(market, dict):
        market = market.get("value", "UK")
    market = market.upper()

    if not user_input:
        user_input = "Create a landing page for Zyloprin, a hypertension medication for healthcare professionals."

    drug_name = extract_drug_name(user_input)
    rules = load_rules(market)

    system_prompt = """
You are a strict pharmaceutical AI reviewer and copywriter.
Never output UI instructions like 'logo', 'navigation menu', 'hero image placeholder'.
Only produce professional pharmaceutical marketing copy and compliance analysis.
Always use the actual drug name provided — never use ** as a placeholder.
"""

    if mode == "audit":
        prompt = f"""
You are a pharmaceutical compliance auditor.
Market: {market}
Regulatory Rules: {rules}

Audit the following webpage content for compliance.
CONTENT: {user_input}

Return EXACTLY this structure:

RULE CHECK RESULTS
Check 1 - [PASS/FAIL]: ISI footer present
Check 2 - [PASS/FAIL]: No unsubstantiated efficacy claims
Check 3 - [PASS/FAIL]: Safety warnings included
Check 4 - [PASS/FAIL]: WCAG 2.1 AA accessibility met
Check 5 - [PASS/FAIL]: Prescribing information link present
Check 6 - [PASS/FAIL]: Adverse event reporting section present
Check 7 - [PASS/FAIL]: Citation references included

TIDY FIX LIST
List each FAIL item as a one-line actionable fix.

DESIGNER
Layout and branding feedback.

DEVELOPER
Accessibility and technical issues with exact fixes.

QA / REGULATORY
Compliance risks and remediation steps.

LEGAL
Regulatory exposure and liability flags.

SCORE:
[number 0-100]
"""
    else:
        prompt = f"""
You are an expert pharmaceutical marketing copywriter and regulatory reviewer.
Drug Name: {drug_name}
Market: {market}
Regulatory Rules: {rules}

Generate compliant landing page content for healthcare professionals.
Use "{drug_name}" as the actual drug name throughout — not ** or placeholders.

Return EXACTLY these sections:

TITLE
A clear, compliant product headline using {drug_name}.

HERO_TEXT
2-3 sentences describing what {drug_name} treats and its mechanism.

BENEFITS
- Benefit 1 (with clinical backing)
- Benefit 2
- Benefit 3
- Benefit 4

SAFETY_INFORMATION
Important safety warnings, contraindications, and mandatory disclaimers per {market} regulations.

REFERENCES
1. [Author et al., Journal, Year]
2. [Author et al., Journal, Year]

RULE CHECK RESULTS
Check 1 - [PASS/FAIL]: ISI footer present
Check 2 - [PASS/FAIL]: No unsubstantiated efficacy claims
Check 3 - [PASS/FAIL]: Safety warnings included
Check 4 - [PASS/FAIL]: WCAG 2.1 AA accessibility met
Check 5 - [PASS/FAIL]: Prescribing information link present
Check 6 - [PASS/FAIL]: Adverse event reporting section present
Check 7 - [PASS/FAIL]: Citation references included

TIDY FIX LIST
List each FAIL as a one-line actionable fix.

DESIGNER
Visual clarity and branding feedback.

DEVELOPER
Accessibility and HTML structure recommendations.

QA / REGULATORY
Compliance considerations and required additions.

LEGAL
Regulatory exposure and liability flags.

SCORE:
[number 0-100]

BRIEF: {user_input}
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": 0.2}
        )

        raw_text = response["message"]["content"]
        score_match = re.search(r"SCORE:\s*(\d+)", raw_text)
        score = int(score_match.group(1)) if score_match else 70
        fix_list = extract_fix_list(raw_text)
        rule_checks = extract_rule_checks(raw_text)
        roles = extract_role_sections(raw_text)

        return jsonify({
            "result": raw_text,
            "score": score,
            "market": market,
            "drug_name": drug_name,
            "fix_list": fix_list,
            "rule_checks": rule_checks,
            "roles": roles,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# HTML generation endpoint
# -----------------------------
@app.route("/generate-html", methods=["POST"])
def generate_html():
    data = request.get_json()
    brief = data.get("brief", "")
    market = data.get("market", "UK").upper()
    fixes = data.get("fixes", [])
    drug_name = extract_drug_name(brief)
    rules = load_rules(market)

    fix_instructions = ""
    if fixes:
        fix_instructions = "APPLY THESE SPECIFIC FIXES IN THE HTML:\n" + \
                           "\n".join(f"- {fix}" for fix in fixes)

    prompt = f"""
Generate a complete, deployable, WCAG 2.1 AA compliant HTML page.

Drug: {drug_name}
Market: {market}
Rules: {rules}
Brief: {brief}

{fix_instructions}

HARD REQUIREMENTS:
- Valid semantic HTML5 with DOCTYPE
- All CSS inline in <style> tag inside <head>
- Colour contrast minimum 4.5:1 ratio
- All images must have descriptive alt attributes
- Heading hierarchy: h1 → h2 → h3 only
- ISI footer section with full safety information
- Cookie consent banner at top of page
- Prescribing Information link in footer
- ARIA labels on all buttons and interactive elements
- Mobile responsive using flexbox
- Use "{drug_name}" as drug name — never use ** placeholders
- Black triangle ▼ next to drug name if market is UK

Return ONLY the complete HTML. No markdown. No explanation. Start with <!DOCTYPE html>
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": "You are an expert HTML developer for pharmaceutical websites. Return ONLY valid deployable HTML5 starting with <!DOCTYPE html>. No markdown. No explanation. No code fences."},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": 0.1}
        )

        html_content = clean_html(response["message"]["content"])

        filename = f"generated_{drug_name.lower()}_{market.lower()}.html"
        filepath = f"output/{filename}"
        with open(filepath, "w") as f:
            f.write(html_content)

        return jsonify({
            "html": html_content,
            "filename": filename,
            "drug_name": drug_name,
            "market": market,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# ✅ NEW: Apply fixes to existing HTML
# -----------------------------
@app.route("/apply-fixes", methods=["POST"])
def apply_fixes():
    data = request.get_json()
    current_html = data.get("html", "")
    fix_list = data.get("fixes", [])
    market = data.get("market", "UK").upper()
    drug_name = data.get("drug_name", "the medication")

    if not current_html:
        return jsonify({"error": "No HTML provided"}), 400

    if not fix_list:
        return jsonify({"html": current_html, "message": "No fixes to apply"})

    fixes_text = "\n".join(f"- {fix}" for fix in fix_list)

    prompt = f"""
You are a pharmaceutical web compliance engineer.

You have an existing HTML page that has compliance issues.
Apply ALL of the following fixes directly to the HTML.

FIXES TO APPLY:
{fixes_text}

Market: {market}
Drug name: {drug_name}

RULES:
- Do NOT restructure the whole page — only patch what is broken
- Add ISI footer if missing
- Add cookie consent banner if missing
- Fix colour contrast issues by updating inline CSS colour values
- Add missing ARIA labels to buttons and inputs
- Fix heading hierarchy if broken
- Add Prescribing Information link in footer if missing
- Replace any ** placeholders with "{drug_name}"
- Keep all existing content that is already compliant

CURRENT HTML:
{current_html}

Return ONLY the complete fixed HTML. Start with <!DOCTYPE html>. No explanation. No markdown.
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": "You are a pharmaceutical HTML compliance engineer. Apply fixes surgically. Return ONLY the complete fixed HTML starting with <!DOCTYPE html>. No markdown. No explanation."},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": 0.1}
        )

        fixed_html = clean_html(response["message"]["content"])

        # Save fixed version
        filename = f"fixed_{drug_name.lower()}_{market.lower()}_{datetime.now().strftime('%H%M%S')}.html"
        with open(f"output/{filename}", "w") as f:
            f.write(fixed_html)

        return jsonify({
            "html": fixed_html,
            "filename": filename,
            "fixes_applied": fix_list,
            "market": market,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Start server
# -----------------------------
if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    print("--- PHARMA AI BACKEND STARTING ---")
    print("Listening on port 5001...")
    app.run(host="0.0.0.0", port=5001, debug=True)
