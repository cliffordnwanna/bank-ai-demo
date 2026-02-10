import re

KNOWLEDGE_KEYWORDS = [
    "policy", "procedure", "guideline", "requirement",
    "how to", "steps", "process", "rule", "regulation",
    "cbn", "compliance", "kYC", "kyc", "aml", "memo", "circular"
]

DATA_KEYWORDS = [
    "balance", "account", "customer", "transaction",
    "opened", "last debit", "last credit", "bvn",
    "phone number", "email", "turnover", "branch",
    "show", "list", "find", "get", "retrieve"
]

ACTION_KEYWORDS = [
    "send", "generate message", "compose", "write message",
    "birthday wish", "email customer", "notify"
]


def classify_query(query: str) -> str:
    q = query.lower()

    if any(k in q for k in ACTION_KEYWORDS):
        return "ACTION"

    if any(k in q for k in DATA_KEYWORDS):
        return "DATA"

    if any(k in q for k in KNOWLEDGE_KEYWORDS):
        return "KNOWLEDGE"

    # default safe behavior
    return "KNOWLEDGE"
