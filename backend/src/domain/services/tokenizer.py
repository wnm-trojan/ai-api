"""Domain service – approximate token counting."""


def estimate_tokens(text: str) -> int:
    """Rough token estimate (~4 chars per token for English)."""
    if not text:
        return 0
    return max(1, len(text) // 4)


def estimate_messages_tokens(messages: list[tuple[str, str]]) -> int:
    """Estimate tokens for a list of (role, content) pairs."""
    return sum(estimate_tokens(content) + 4 for _, content in messages)
