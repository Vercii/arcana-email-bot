import json

response_text = _item["json"]["candidates"][0]["content"]["parts"][0]["text"]
parsed = json.loads(response_text)

return {
    "json": {
        "is_email_request": parsed.get("is_email_request"),
        "transcript": parsed.get("transcript", ""),
        "recipient": parsed.get("recipient", ""),
        "subject": parsed.get("subject", ""),
        "body": parsed.get("body", ""),
        "needs_clarification": parsed.get("needs_clarification", False),
        "clarification_question": parsed.get("clarification_question", "")
    }
}
