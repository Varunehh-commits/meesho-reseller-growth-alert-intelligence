from growth_engine import mom_growth, is_flagged, validate_feed
import os


# ============================================================
# PART 2: REQUIRED TESTS
# ============================================================

# Test 1: April -> May Ethnic Wear
previous = 104520.77
current = 185107.61

growth = mom_growth(previous, current)

assert growth == 77.10
assert is_flagged(growth) == "flagged"


# Test 2: May -> June Beauty & Personal Care
previous = 35542.11
current = 37559.07

growth = mom_growth(previous, current)

assert growth == 5.67
assert is_flagged(growth) == "not_flagged"


# Test 3: Exact 8% boundary
previous = 100000
current = 108000

growth = mom_growth(previous, current)

assert growth == 8.0
assert is_flagged(growth) == "escalate_exact_boundary"


# Test 4: Corrupted feed validation
base_dir = os.path.dirname(os.path.abspath(__file__))
fixture_path = os.path.join(
    base_dir,
    "fixtures",
    "corrupted_feed.csv"
)

valid, errors = validate_feed(fixture_path)

assert valid is False

assert len(errors) == 3

assert errors[0] == (
    "line 3: negative revenue (-4200.00) "
    "for category=Western Wear"
)

assert errors[1] == (
    "line 4: missing category (month=July)"
)

assert errors[2] == (
    "line 6: missing revenue (category=Home & Kitchen)"
)


print("All Part 2 tests passed successfully.")