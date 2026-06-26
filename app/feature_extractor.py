from urllib.parse import urlparse
import re

def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    if domain.startswith("www."):
        domain = domain[4:]

    features = {}

    # Basic URL counts
    features["qty_dot_url"] = url.count(".")
    features["qty_hyphen_url"] = url.count("-")
    features["qty_underline_url"] = url.count("_")
    features["qty_slash_url"] = url.count("/")
    features["qty_questionmark_url"] = url.count("?")
    features["qty_equal_url"] = url.count("=")
    features["qty_at_url"] = url.count("@")
    features["qty_and_url"] = url.count("&")
    features["qty_exclamation_url"] = url.count("!")
    features["qty_space_url"] = url.count(" ")

    # Length features
    features["length_url"] = len(url)
    features["length_domain"] = len(domain)
    features["length_path"] = len(path)

    # Counts
    features["qty_digits_url"] = sum(c.isdigit() for c in url)
    features["qty_letters_url"] = sum(c.isalpha() for c in url)
    features["qty_special_url"] = len(re.findall(r"[^a-zA-Z0-9]", url))

    # Ratios
    total_len = len(url) if len(url) > 0 else 1
    features["digit_ratio_url"] = features["qty_digits_url"] / total_len
    features["special_ratio_url"] = features["qty_special_url"] / total_len

    # Domain structure
    features["qty_subdomains"] = max(domain.count(".") - 1, 0)
    features["https"] = 1 if parsed.scheme == "https" else 0
    features["is_ip"] = 1 if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", domain) else 0

    # URL shortening
    shorteners = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "is.gd", "cutt.ly"]
    features["url_shortened"] = 1 if any(s in url for s in shorteners) else 0

    # Suspicious keywords
    suspicious_keywords = [
        "login", "verify", "secure", "update", "account",
        "bank", "password", "signin", "confirm", "wallet"
    ]
    lower_url = url.lower()
    features["qty_suspicious_words"] = sum(word in lower_url for word in suspicious_keywords)

    # Suspicious TLD
    suspicious_tlds = [".xyz", ".top", ".club", ".online", ".site", ".ru", ".tk"]
    features["suspicious_tld"] = 1 if any(domain.endswith(tld) for tld in suspicious_tlds) else 0

    return features