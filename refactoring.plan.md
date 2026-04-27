# Overview

This project is a dictionary-based Pygame simulation where squares move, bounce on window boundaries, flee from bigger squares, and can chase smaller squares. The main logic is in `main_dict.py`, especially inside `run()`.

The code already works as a solid prototype, but it can be improved in beginner-friendly ways: clearer naming, reduced duplication, less “magic numbers,” and simpler function boundaries. The goal is to improve readability and maintainability **without redesigning the architecture**.

# Refactoring Goals

1. Improve readability with clearer names and grouped constants.
2. Reduce duplicated calculations (especially square-center and speed formula).
3. Keep behavior logic easier to follow by extracting small helper functions.
4. Improve type clarity using beginner-safe typing improvements.
5. Keep the same runtime behavior while making the code easier to test and debug.
6. Ensure final refactored code includes concise inline comments explaining what changed and why.

# Step-by-Step Refactoring Plan

## Step 1 — Group and name behavior constants clearly

**What to do**
- Keep existing constants, but add explicit behavior constants near them:
  - `FLEE_RADIUS = 120`
  - `CHASE_RADIUS = 200`
  - `CHASE_SPEED_BOOST = 1.1`
  - Optionally `MIN_LIFESPAN_MS` and `MAX_LIFESPAN_MS` for current lifespan range.
- Replace hardcoded values in logic with these constant names.

**Why this helps**
- Beginners can understand intent quickly (“flee radius” is clearer than raw `120`).
- Tuning behavior becomes safer because values are edited in one place.

**Inline comment requirement for final code**
- Add short comments near new constants, e.g.:
  - “Changed: replaced magic numbers with named constants.”
  - “Why: makes game behavior easier to read and tune.”

**Optional before/after snippet**
- Before: `if is_close_enough(small, big, 120):`
- After: `if is_close_enough(small, big, FLEE_RADIUS):`

---

## Step 2 — Extract a helper for square center position

**What to do**
- Add a small helper function, for example:
  - `get_square_center(square: dict) -> tuple[float, float]`
- Use it in `is_close_enough`, `flee_away`, and `chase_towards`.

**Why this helps**
- Removes repeated center-calculation code.
- Reduces mistakes when changing position logic in multiple places.

**Inline comment requirement for final code**
- Add a concise comment in the helper:
  - “Changed: extracted repeated center math into one function.”
  - “Why: avoids duplication and makes behavior functions shorter.”

**Optional before/after snippet**
- Before: repeated `x + size / 2`, `y + size / 2` blocks.
- After: `small_pos = get_square_center(small_square)`.

---

## Step 3 — Extract a helper for size-based speed calculation

**What to do**
- Add `compute_speed_from_size(size: float) -> float` with current formula.
- Reuse in `create_square`, `flee_away`, and `chase_towards`.
- Keep current gameplay behavior (same formula, same outputs).

**Why this helps**
- The same formula appears multiple times; one helper keeps it consistent.
- Easier for students to test one function and trust results everywhere.

**Inline comment requirement for final code**
- Add a brief comment near the helper:
  - “Changed: centralized speed formula.”
  - “Why: one source of truth improves maintainability and correctness.”

**Optional before/after snippet**
- Before: repeated speed expression in three functions.
- After: `speed = compute_speed_from_size(square["size"])`.

---

## Step 4 — Improve type hints incrementally (without advanced patterns)

**What to do**
- Keep dictionary approach, but improve signatures gradually:
  - Add explicit return type for `chase_towards` (`-> None`).
  - Add simple type alias like `Square = dict[str, object]` (beginner-safe step).
- If comfortable, as a later mini-step, move to `TypedDict` (optional in this light plan).

**Why this helps**
- Better editor hints and easier debugging.
- Introduces typing concepts progressively without overwhelming complexity.

**Inline comment requirement for final code**
- Add concise comment where type clarity is improved:
  - “Changed: added clearer type hints for square data.”
  - “Why: helps IDE and readers understand expected structure.”

---

## Step 5 — Extract one small behavior pass from `run()`

**What to do**
- Create a helper such as `apply_interactions(squares: list[dict]) -> None`.
- Move only the nested flee/chase loop into this helper.
- Keep call order in `run()` unchanged:
  1. events
  2. lifespan filtering/respawn
  3. behavior pass
  4. movement update
  5. drawing

**Why this helps**
- `run()` becomes easier to read for first-year students.
- Behavior logic can be discussed/tested separately.

**Inline comment requirement for final code**
- At helper call site and helper definition, add short comments:
  - “Changed: extracted pairwise interaction loop.”
  - “Why: keeps main loop readable and separates responsibilities.”

---

## Step 6 — Clarify lifecycle handling with a helper function

**What to do**
- Extract lifespan maintenance to a helper:
  - e.g., `refresh_population(squares: list[dict], target_count: int) -> list[dict]`
- Internally keep existing logic: filter expired, then respawn until count target.

**Why this helps**
- Makes the rebirth/respawn idea explicit.
- Easier to reason about and debug lifecycle behavior independently.

**Inline comment requirement for final code**
- Add concise comment in helper:
  - “Changed: grouped expiration + respawn into one lifecycle function.”
  - “Why: improves readability and keeps count-stability logic in one place.”

---

## Step 7 — Add short defensive comments for edge cases

**What to do**
- Keep existing zero-distance guards in `flee_away` and `chase_towards`.
- Add brief inline comments explaining why early return exists.

**Why this helps**
- Reinforces important concept: avoid division by zero during normalization.
- Helps beginners connect math and runtime safety.

**Inline comment requirement for final code**
- Example comment:
  - “Changed: documented zero-distance guard.”
  - “Why: prevents division-by-zero and undefined velocity direction.”

---

## Step 8 — Verify behavior after each small step

**What to do**
- After each refactor step, run the game and verify:
  - squares still move and bounce,
  - flee/chase still activate,
  - expired squares are replaced,
  - FPS text and square count still render.

**Why this helps**
- Teaches safe incremental refactoring.
- Prevents multiple hidden bugs from accumulating.

**Inline comment requirement for final code**
- Add one short note near major refactor blocks if needed:
  - “Changed in small steps; behavior kept equivalent.”
  - “Why: safer refactoring process.”

# Final Output Requirements (Mandatory)

When this plan is executed, the output MUST:

1. Contain **only the refactored code**.
2. Include **inline comments** that explain:
   - what changed,
   - why the change improves readability/maintainability/correctness,
   - important related programming concepts.
3. Keep all explanations **concise and beginner-friendly**.
4. Preserve original behavior and overall structure as much as possible.

# Key Concepts for Students

- **Single Responsibility Principle (light version):** each function should do one clear job.
- **DRY (Don’t Repeat Yourself):** repeated formulas and coordinate logic should be centralized.
- **Magic Numbers vs Named Constants:** names communicate intent better than raw numbers.
- **Incremental Refactoring:** make one small change, test, then continue.
- **Defensive Programming:** guard against edge cases like zero distance before normalization.
- **Type Hints for Clarity:** improve readability and tooling support without changing runtime behavior.

# Safety Notes

- Do not change multiple systems at once (movement + behavior + rendering together).
- Keep one refactor per commit or checkpoint so rollback is easy.
- Test after every step to confirm behavior is unchanged.
- If behavior changes unexpectedly, revert the last small step and re-test.
- Avoid introducing advanced abstractions (inheritance hierarchies, complex patterns) in this light refactor.
