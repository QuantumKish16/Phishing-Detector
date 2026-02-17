import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'http\S+', 'URL', text)
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

suspicious_keywords = [
    "verify",
    "urgent",
    "immediately",
    "action required",
    "limited time",
    "72 hours",
    "account suspended",
    "security alert",
    "confirm password",
    "click below"
]
brand_domains = {
    "paypal": "paypal.com",
    "amazon": "amazon.com",
    "apple": "apple.com",
    "bank": "bank.com"
}


def keyword_score(text):
    text = text.lower()
    return sum(1 for word in suspicious_keywords if word in text)


def extract_domain(sender_text):
    if not isinstance(sender_text, str):
        return ""

    # Extract email inside < >
    match = re.search(r"<([^>]+)>", sender_text)
    if match:
        email = match.group(1)
    else:
        email = sender_text

    if "@" in email:
        return email.split("@")[-1].lower()

    return ""


def sender_domain_mismatch(text, sender_email):
    text = text.lower()
    sender_domain = extract_domain(sender_email)

    for brand, official_domain in brand_domains.items():
        if brand in text:
            if official_domain not in sender_domain:
                return 1   # Mismatch detected

    return 0


def extract_url_features(text, sender_email=None):
    text_lower = text.lower()
    features = []

    features.append(len(text))
    features.append(text.count("."))
    features.append(1 if "@" in text else 0)
    features.append(1 if re.search(r"\d+\.\d+\.\d+\.\d+", text) else 0)

    shorteners = ["bit.ly", "tinyurl.com", "goo.gl", "t.co"]
    features.append(1 if any(s in text_lower for s in shorteners) else 0)

    # 🔥 Add sender mismatch feature
    if sender_email:
        features.append(sender_domain_mismatch(text, sender_email))
    else:
        features.append(0)

    return features

