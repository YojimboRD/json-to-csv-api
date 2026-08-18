# The constitution is enforced in code, not in the system prompt.
# These rules cannot be overridden by the agent's reasoning.

BLOCKED_ACTIONS = [
    # Financial
    "transfer all",
    "send all funds",
    "drain wallet",
    "withdraw all",
    # System destruction
    "delete all",
    "wipe database",
    "drop table",
    # Deception
    "pretend to be human",
    "deny being an ai",
    "hide this action",
    # Replication without approval
    "spawn child",
    "replicate self",
    "create child agent",
]

REQUIRES_HUMAN_APPROVAL = [
    "send email",
    "post to",
    "publish",
    "register domain",
    "deploy to production",
    "spend more than",
    "transfer funds",
]

MAX_SPEND_PER_TICK = 0.10  # max $0.10 per agent loop cycle
MAX_DAILY_SPEND = 1.00     # max $1.00 per day

def check_action(action: str) -> tuple[bool, str]:
    """
    Returns (is_allowed, reason).
    Hard blocks return False immediately.
    """
    action_lower = action.lower()

    for blocked in BLOCKED_ACTIONS:
        if blocked in action_lower:
            return False, f"CONSTITUTION BLOCK: '{blocked}' is not permitted"

    return True, "ok"

def requires_approval(action: str) -> tuple[bool, str]:
    """
    Returns (needs_approval, reason).
    These actions pause and wait for human confirmation.
    """
    action_lower = action.lower()

    for trigger in REQUIRES_HUMAN_APPROVAL:
        if trigger in action_lower:
            return True, f"APPROVAL REQUIRED: '{trigger}' needs human sign-off"

    return False, "ok"

def check_spend(amount: float, daily_total: float) -> tuple[bool, str]:
    """
    Returns (is_allowed, reason).
    Enforces spending caps per tick and per day.
    """
    if amount > MAX_SPEND_PER_TICK:
        return False, f"SPEND BLOCK: ${amount:.2f} exceeds per-tick limit of ${MAX_SPEND_PER_TICK:.2f}"

    if daily_total + amount > MAX_DAILY_SPEND:
        return False, f"SPEND BLOCK: would exceed daily limit of ${MAX_DAILY_SPEND:.2f}"

    return True, "ok"
