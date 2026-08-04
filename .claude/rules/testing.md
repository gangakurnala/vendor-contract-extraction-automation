# Testing Rules

## Building from a spec — RED-GREEN (YOU MUST)

**Applies to:** Any feature implementation with a corresponding spec in `docs/specs/`

**Workflow:**

1. **RED** - Write a failing test
   - Take the next acceptance criterion from the spec
   - Write a test that captures this criterion
   - Do NOT write any implementation yet
   - Run the test and SHOW it fails for the right reason (behavior missing, not a typo)

2. **GREEN** - Write minimum code to pass
   - Write only the minimum code needed to pass the test
   - Run the failing test → it should pass
   - Run the full test suite → ensure no regressions
   - SHOW both test runs passing

3. **REFACTOR** - Clean up if useful
   - Refactor code for clarity/maintainability while keeping tests green
   - Run full suite again to verify no regressions
   - Skip this step if no refactoring is needed

4. **REPEAT** - Move to next criterion
   - Go back to step 1 with the next acceptance criterion
   - Continue until all acceptance criteria are covered

**Critical Rules:**

- ✅ Test first, implementation second
- ✅ Never modify a test to make it pass
- ⛔ Never skip the RED phase (don't write code without a failing test first)
- ⛔ Never modify tests just to make them pass

**If a criterion is ambiguous or a test looks wrong:**
- STOP implementation
- Ask the user for clarification
- Do NOT proceed until criterion is clear

**Reporting:**

After each RED and GREEN phase, show:
1. The test code
2. The test failure output (RED phase)
3. The implementation code (GREEN phase)
4. The test passing output (GREEN phase)
5. Full test suite results (GREEN phase)

---

## Related Files

- Specs are located in: `docs/specs/`
- Test files are in: `tests/`
- Test runner: `pytest`
