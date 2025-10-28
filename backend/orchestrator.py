import random

def call_orchestrator(prompt: str, mode: str, document=None) -> str:
    """
    Mocked call to orchestrator. In production, replace this
    with an HTTP POST to your real orchestrator endpoint.
    """
    # Simulate stochastic variation in LLM output
    endings = [
        "with high confidence.",
        "after careful review.",
        "considering relevant factors.",
        "based on extracted key details.",
    ]
    return f"[{mode.upper()}] {prompt.strip()} {random.choice(endings)}"