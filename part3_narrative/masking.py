# ============================================================
# PART 3: RESELLER NAME MASKING
# ============================================================

def alias_for(reseller_id: str) -> str:
    """
    Convert a reseller ID into an external-facing alias.

    Example:
        RS019 -> ALIAS-19
        RS006 -> ALIAS-06
    """
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(
    text: str,
    reseller_names: list[str]
) -> bool:
    """
    Return False if any raw reseller name appears verbatim
    inside the supplied text.
    """
    for reseller_name in reseller_names:
        if reseller_name in text:
            return False

    return True