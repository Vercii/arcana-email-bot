import json

incoming = incoming = _item["json"]
response_text = incoming["content"]["parts"][0]["text"]

# Parse Gemini's JSON response.
parse_ok = True

try:
    cleaned_text = response_text.strip()

    if cleaned_text.startswith("```"):
        lines = cleaned_text.splitlines()

        if lines and lines[0].strip().lower() in (
            "```", "```json"
        ):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned_text = "\n".join(lines).strip()

    draft = json.loads(cleaned_text)

except (json.JSONDecodeError, TypeError, AttributeError):
    draft = {}
    parse_ok = False

if not isinstance(draft, dict):
    draft = {}
    parse_ok = False

# Read expected fields.
is_email_request = draft.get("is_email_request") is True
needs_clarification = draft.get("needs_clarification") is True

fields = {
    "transcript": draft.get("transcript", ""),
    "recipient": draft.get("recipient", ""),
    "subject": draft.get("subject", ""),
    "body": draft.get("body", ""),
    "clarification_question": draft.get(
        "clarification_question", ""
    ),
}

errors = []

# Normalize strings and reject unexpected types.
for name, value in fields.items():
    if not isinstance(value, str):
        errors.append("Invalid field type: " + name)
        fields[name] = ""
    else:
        fields[name] = value.strip()

transcript = fields["transcript"]
recipient = fields["recipient"]
subject = fields["subject"]
body = fields["body"]
clarification_question = fields["clarification_question"]

if not parse_ok:
    errors.append("Gemini returned invalid JSON.")

if not is_email_request:
    errors.append("Audio is not a recognized email request.")

if needs_clarification:
    errors.append("The request needs clarification.")

# Basic email-address format check without importing re.
if not recipient:
    errors.append("Recipient email address is missing.")
else:
    parts = recipient.split("@")

    if (
        len(parts) != 2
        or not parts[0]
        or not parts[1]
        or " " in recipient
        or "." not in parts[1]
        or parts[1].startswith(".")
        or parts[1].endswith(".")
    ):
        errors.append("Recipient email address has an invalid format.")

if not subject:
    errors.append("Email subject is missing.")
elif len(subject) > 200:
    errors.append("Email subject exceeds 200 characters.")

if not body:
    errors.append("Email body is missing.")
elif len(body) > 10000:
    errors.append("Email body exceeds 10,000 characters.")

valid = len(errors) == 0

return {
    "json": {
        "parse_ok": parse_ok,
        "is_email_request": is_email_request,
        "needs_clarification": needs_clarification,
        "clarification_question": clarification_question,
        "transcript": transcript,
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "valid": valid,
        "errors": errors
    }
}
