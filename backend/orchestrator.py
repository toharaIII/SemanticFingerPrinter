import random

def call_orchestrator(prompt: str, plan: str, document=None) -> str:
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
    #[{plan.upper()}]
    return f"{prompt.strip()} {random.choice(endings)}"