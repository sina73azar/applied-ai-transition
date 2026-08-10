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
