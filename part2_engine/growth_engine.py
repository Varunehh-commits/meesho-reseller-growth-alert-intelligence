import csv


# ============================================================
# PART 2: PYTHON GUARDRAIL & GROWTH-DETECTION ENGINE
# ============================================================


# ============================================================
# FUNCTION 1
# Month-on-Month Growth
# ============================================================

def mom_growth(previous: float, current: float) -> float:
    """
    Calculate Month-on-Month growth percentage.

    Formula:
        ((current - previous) / previous) * 100

    The result is rounded to 2 decimal places.
    """

    return round((current - previous) / previous * 100, 2)


# ============================================================
# FUNCTION 2
# Flag significant movement
# ============================================================

def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """
    Classify Month-on-Month growth.

    Returns:
        "flagged"                  -> abs(mom_pct) > threshold
        "not_flagged"              -> abs(mom_pct) < threshold
        "escalate_exact_boundary"  -> abs(mom_pct) == threshold
    """

    if abs(mom_pct) > threshold:
        return "flagged"

    if abs(mom_pct) < threshold:
        return "not_flagged"

    return "escalate_exact_boundary"


# ============================================================
# FUNCTION 3
# Validate monthly revenue feed
# ============================================================

def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """
    Validate a month,category,revenue,n_orders CSV file.

    Returns:
        (True, []) when there are no validation errors.
        (False, errors) when one or more validation errors exist.
    """

    errors = []

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for line_number, row in enumerate(reader, start=2):

            month = row.get("month", "")
            category = row.get("category", "")
            revenue = row.get("revenue", "")

            # ------------------------------------------------
            # Missing category
            # ------------------------------------------------

            if not category:
                errors.append(
                    f"line {line_number}: missing category (month={month})"
                )

            # ------------------------------------------------
            # Missing revenue
            # ------------------------------------------------

            if revenue == "":
                errors.append(
                    f"line {line_number}: missing revenue "
                    f"(category={category})"
                )
                continue

            # ------------------------------------------------
            # Revenue must be numeric
            # ------------------------------------------------

            try:
                revenue_value = float(revenue)

            except ValueError:
                errors.append(
                    f"line {line_number}: revenue not numeric: {revenue!r}"
                )
                continue

            # ------------------------------------------------
            # Revenue cannot be negative
            # ------------------------------------------------

            if revenue_value < 0:
                errors.append(
                    f"line {line_number}: negative revenue "
                    f"({revenue}) for category={category}"
                )

    if len(errors) == 0:
        return True, []

    return False, errors