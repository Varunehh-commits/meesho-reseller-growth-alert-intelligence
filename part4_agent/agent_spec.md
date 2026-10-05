# Part 4 — Agentic Workflow Specification

## Goal

Keep category managers informed of any category moving beyond the 8% Month-on-Month threshold, while requiring human approval before any message goes out.

The agent must operate as a guarded, repeatable workflow using verified Part 2 calculations and Part 3's narrative template.

No message is ever automatically sent.

---

## Tools

The agent uses the following existing project functions:

- `validate_feed()` from `part2_engine/growth_engine.py`
- `mom_growth()` from `part2_engine/growth_engine.py`
- `is_flagged()` from `part2_engine/growth_engine.py`
- Part 3's template-fill logic for drafting stakeholder messages

The Part 2 functions are imported and reused without reimplementing their logic.

No external API, paid service, email service, SMTP integration, or API key is required.

---

## Memory / State

The agent keeps the previous month's verified revenue per category.

This state is required to calculate the next month's Month-on-Month revenue change.

For each category, the workflow uses:

- previous month's revenue
- current month's revenue
- current run month
- previous month
- calculated MoM percentage
- flag status

---

## Planner

The agent follows this exact ordered sequence.

### Step 1 — Load the monthly revenue feed

Load the monthly category revenue CSV produced by Part 1.

The expected columns are:

- `month`
- `category`
- `revenue`
- `n_orders`

### Step 2 — Validate the feed

Run:

`validate_feed()`

The feed must pass validation before any further processing occurs.

### Step 3 — Hard Stop if invalid

If validation returns `False`:

- report the validation errors
- do not calculate MoM
- do not run the flagging workflow
- do not draft messages
- emit the required structured JSON object with `action_taken` set to `"hard_stop"`

### Step 4 — Compute MoM

If the feed is valid, compute:

`mom_growth(previous_revenue, current_revenue)`

for every category against the previous month's verified revenue.

### Step 5 — Run the growth guardrail

Run:

`is_flagged(mom_pct)`

for every category.

Possible results are:

- `flagged`
- `not_flagged`
- `escalate_exact_boundary`

### Step 6 — Sort and draft

Sort flagged categories by:

`abs(mom_pct)`

in descending order.

Draft messages for **at most the top 3 flagged categories by magnitude**, using the Part 3 narrative template.

### Step 6b — Suppress remaining flagged categories

Any flagged category beyond the top-3 drafting limit must be recorded as:

`suppressed, review manually`

These categories must not be silently dropped.

### Step 7 — Escalate exact boundaries separately

Any category whose `is_flagged()` result is:

`escalate_exact_boundary`

must be added to `escalated_categories`.

Exact-boundary categories must not be merged into either `flagged_categories` or `suppressed_categories`.

No narrative is drafted for an exact-boundary category.

### Step 8 — Emit structured JSON

Emit exactly one structured JSON object for every run.

The object must contain exactly these seven top-level keys:

```json
{
  "run_month": "...",
  "validation_status": "valid",
  "validation_errors": [],
  "flagged_categories": [],
  "suppressed_categories": [],
  "escalated_categories": [],
  "action_taken": "drafted_and_held_for_approval"
}