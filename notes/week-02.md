# Week 2 — Python Objects and Ticket Queue

## Attribute visibility by naming convention

- `tickets`: public; callers are free to use it.
- `_tickets`: internal implementation detail by convention. Python does not
  prevent access, but callers should normally avoid using it directly.
- `__tickets`: Python name-mangles it (for example,
  `_TicketQueue__tickets`) to reduce accidental access and subclass name
  collisions. It is still not truly private.

For this exercise, `_tickets` communicates the intended boundary clearly.

## Instance variables versus shared class variables

```python
class TicketQueue:
    shared_tickets = {}  # class attribute: shared by instances

    def __init__(self) -> None:
        self._tickets = {}  # instance attribute: a separate dict per instance
```

A mutable class attribute is shared state, but it does not make the class a
singleton. A singleton restricts creation or use to one instance; a class can
have many instances that happen to share a class attribute.

## `self`

`self` is the current object instance, similar to Kotlin's `this`. Python makes
it an explicit first method parameter:

```python
queue.add("T-1", "Login problem", Priority.HIGH)
```

is conceptually handled as:

```python
TicketQueue.add(queue, "T-1", "Login problem", Priority.HIGH)
```

## Lambdas and callables

A lambda is a small anonymous function:

```python
clock = lambda: now
```

It is equivalent to:

```python
def clock():
    return now
```

The lambda receives no arguments and returns the captured `now` value. Passing
it into `TicketQueue` lets tests control time. Calling `self._clock()` executes
the injected function and returns a `datetime`.

`Callable[[], datetime]` means: a callable taking no arguments and returning a
`datetime`. A class implementing `__call__` can also satisfy that shape.

## Iterables and iterators

- An **iterable**, such as a list or tuple, can produce an iterator.
- An **iterator** remembers its current position and produces one value at a
  time.
- `iter(value)` obtains an iterator.
- `next(iterator)` consumes its next value.
- An exhausted iterator raises `StopIteration`; a `for` loop handles this
  internally.

In `SequenceClock`, `*values` collects the arguments into a tuple and
`iter(values)` creates a stateful iterator over it:

```python
class SequenceClock:
    def __init__(self, *values: datetime) -> None:
        self._values = iter(values)

    def __call__(self) -> datetime:
        return next(self._values)
```

Each `clock()` call consumes and returns the next supplied time. This lets a
test provide predictable creation and closing times without using the real
system clock.

## Protocols and structural typing

```python
class Clock(Protocol):
    def __call__(self) -> datetime: ...
```

A `Protocol` is similar to a Kotlin interface, but it normally uses
**structural typing**: a class satisfies the protocol by having the required
members, without explicitly inheriting from it.

`SequenceClock` therefore does not inherit from `Clock`, but it conforms to the
contract because its instances are callable with no arguments and return a
`datetime`. This relationship is primarily checked by static type checkers; it
is not automatically enforced at runtime.

For this one-method example, `Clock` and `Callable[[], datetime]` describe
nearly the same capability. A named protocol becomes more useful when a
dependency requires several methods or properties.

## Deterministic ordering

A tuple key compares its components from left to right:

```python
(-ticket.priority, ticket.created_at, ticket.ticket_id)
```

- Negating an `IntEnum` priority makes larger priorities compare first.
- Creation time remains ascending, so older tickets compare first.
- The identifier breaks a remaining tie deterministically.

Store an optional result once before checking it:

```python
ticket = queue.next_open()
assert ticket is not None
assert ticket.ticket_id == "a"
```

Besides avoiding a second call, the `is not None` check lets a type checker
narrow `Ticket | None` to `Ticket` for the following statement.

## Algorithmic complexity

Big O describes how work grows as input size `n` grows; here, `n` is the number
of tickets being considered. It describes growth rather than exact execution
time, so constant factors are omitted.

- `min(items, key=...)` scans once and keeps only the best item: **O(n)** time.
- `sorted(items, key=...)` determines the complete order: generally
  **O(n log n)** time, and returns a new list.
- A list comprehension that filters all tickets is **O(n)** time.

Therefore:

```text
filter O(n) + min O(n)       = O(n)
filter O(n) + sort O(n log n) = O(n log n)
```

`O(n) + O(n)` becomes `O(n)`, not `O(2n)`, because Big O removes constant
multipliers. `O(n log n)` dominates an added `O(n)` term as `n` grows.

Use `min()` or `max()` when only one best element is required. Use `sorted()`
when the complete ordered collection is required. Python's sort can perform
better on already ordered data, but `O(n log n)` is the useful general-case
comparison here.

The current implementation first builds an `open_tickets` list, so that list
still uses **O(n)** additional memory. `min()` itself does not create another
fully ordered list.

## Docstrings and comments

The first string expression in a function is its docstring. Later standalone
triple-quoted strings are not comments; they are unnecessary expression
statements. Use `#` for a useful implementation comment, and prefer removing a
comment when the code and real docstring already communicate the behavior.

## Dataclasses and queue state

- `@dataclass` commonly generates `__init__`, `__repr__`, and value-based
  `__eq__`.
- It does not automatically generate Kotlin-style getters and setters.
- Mutable dataclasses are normally not hashable by default.
- `status=Status.OPEN` and `closed_at=None` describe the valid initial state of
  every new ticket.
- A dictionary keyed by `ticket_id` makes duplicate detection and lookup direct:
  `dict[str, Ticket]`.

## Current lesson

Design object state deliberately: decide what belongs to each instance, what
must remain an internal detail, and which dependencies—such as time—should be
injected so behavior can be tested deterministically.
