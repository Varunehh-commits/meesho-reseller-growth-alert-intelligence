# Part 3 — Reusable Narrative Prompt Pack

## Trigger

Start this prompt when a category's `is_flagged` result is `"flagged"`.

The narrative must use only verified values supplied by Part 2 and must not invent additional numbers or unsupported facts.

---

## Input list

The prompt requires these placeholder variables:

- `{category}` — flagged category name
- `{previous_revenue}` — previous month's verified revenue
- `{current_revenue}` — current month's verified revenue
- `{mom_pct}` — verified Month-on-Month percentage
- `{month}` — current month
- `{prev_month}` — previous month

If a reseller is referenced, use its coded alias rather than its raw reseller name.

---

## Prompt

Write a stakeholder-ready update for a regional manager using the following structure:

### Context

State what is being measured and explicitly name the comparison period as `{month}` vs. `{prev_month}`.

### Insight

State the verified result for `{category}` using the supplied `{mom_pct}` value.

Label the statement explicitly as a **Fact**.

### Implication

Give one specific and actionable next step based on the verified result.

If the recommendation proposes a possible cause or explanation that the supplied data does not prove, label it explicitly as a **Hypothesis**.

Do not state any number that is not one of the supplied placeholder values.

Do not invent causes, explanations, business facts, or additional metrics.

If a reseller is referenced, use only its coded alias and never expose its raw reseller name.

---

## Checklist

Before the narrative is used, verify:

- [ ] Every number in the draft matches a supplied placeholder value exactly.
- [ ] Every factual insight is explicitly labeled as a **Fact**.
- [ ] Any proposed cause or explanation is explicitly labeled as a **Hypothesis**.
- [ ] The recommendation is specific and actionable rather than vague.
- [ ] The comparison names both `{month}` and `{prev_month}`.
- [ ] Any reseller referenced uses a coded alias and never the raw reseller name.