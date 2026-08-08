# Week 1 Learning Notes

These notes record concepts investigated while implementing and testing the
transaction ledger. Add personal examples or corrections as understanding
deepens.

## `None`

- `None` is Python's singleton value for the absence of a value.
- Compare it with `is None`, not `== None`.
- `None` is falsy, but so are `0`, `False`, `""`, and empty collections. A
  generic truth check therefore cannot always distinguish missing data from a
  valid falsy value.
- Ledger connection: validate the original value and its type before converting
  it to `str`; otherwise `None` becomes the non-empty string `"None"`.

## NaN and Infinity

- NaN means "not a number" and represents an undefined numeric result.
- NaN and positive or negative infinity can be valid `float` or `Decimal`
  objects while still being invalid transaction amounts.
- NaN has unusual comparison behavior and is not equal to itself.
- `Decimal.is_finite()` rejects NaN and both infinities before an ordering
  comparison. The left side of `or` must come first so short-circuit evaluation
  avoids an invalid NaN comparison.

## Python Virtual Environments

- A virtual environment gives a project its own package installation directory
  and Python command context.
- Activation changes shell variables, especially `PATH`, so `python`, `pip`,
  and `pytest` resolve to `.venv/bin/...`.
- Activation is convenient but not required; `.venv/bin/python` and
  `.venv/bin/pytest` can always be invoked explicitly.
- Virtual environments isolate project dependencies from system Python and
  other projects.

## Test-Driven Development

TDD uses a short feedback loop:

1. **Red:** write a test describing missing behavior and observe it fail.
2. **Green:** implement the smallest change that makes it pass.
3. **Refactor:** improve the design while keeping the tests green.

Week 1 was partly test-first rather than full TDD because initial checks were
provided. Personally adding cases for `bool`, negative strings, floats, NaN,
infinity, invalid categories, empty input, and error propagation practiced the
TDD loop directly.

## `raise`

- `raise` creates or propagates an exception and stops the current normal
  control flow.
- An uncaught exception travels up through callers until something handles it.
- Raising `ValueError` defines a caller-facing contract for invalid values.
- `raise ValueError(...) from error` translates a lower-level exception while
  preserving the original cause for debugging.
- Catch only expected exceptions; broad `except Exception` blocks can hide
  unrelated programming errors.

## `__pycache__`

- `__pycache__` stores compiled Python bytecode files, normally ending in
  `.pyc`.
- CPython may reuse compatible cached bytecode during later imports instead of
  recompiling unchanged source.
- It is generated state, depends on the Python implementation/version, and can
  be recreated, so it belongs in `.gitignore` rather than Git.

## Python and Java Compilation

| Aspect | Python (CPython) | Java (`javac` + JVM) |
|---|---|---|
| Compile to bytecode | Implicit during import or execution | Usually an explicit `javac` or build-tool step |
| Bytecode format | Python bytecode, optionally cached as `.pyc` | JVM bytecode stored in `.class` files |
| Bytecode executed by | CPython virtual machine | JVM |
| Machine code/JIT | Traditional CPython generally interprets bytecode rather than applying a JVM-style JIT | JVM JIT-compiles frequently executed bytecode to native machine code |
| Typical compilation timing | Immediately before execution or while importing a module | Before program startup; build tools and IDEs often automate it |
| Source required at normal runtime | Usually yes for scripts; imported bytecode may be cached | No, compiled classes/JARs are normally sufficient |

The active learning environment uses CPython 3.10.12, so the traditional
non-JIT CPython model is the relevant one. Both languages compile to bytecode;
the major difference is when compilation occurs, how visible the step is, and
whether the runtime normally JIT-compiles hot bytecode to native code.

## Personal Takeaway

Validate each input independently before normalization, consider unusual
runtime values instead of only expected ones, and use tests to make the caller
contract executable.

