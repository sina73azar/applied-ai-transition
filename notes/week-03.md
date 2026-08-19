# Week 3 — Iterators, JSON, and Operation Events

## JSON and Python values

JSON is a text format for exchanging structured data. A JSON parser converts
JSON text into the corresponding Python value.

| JSON value | Example JSON text | Python value after parsing |
|---|---|---|
| Object | `{"level": "error"}` | `dict`, for example `{"level": "error"}` |
| Array | `["a", "b"]` | `list`, for example `["a", "b"]` |
| String | `"hello"` | `str`, for example `"hello"` |
| Number | `42` or `3.5` | `int` or `float` |
| Boolean | `true` or `false` | `True` or `False` |
| Null | `null` | `None` |

JSON requires double quotes for strings and object keys. Its boolean and null
literals are lowercase. Whitespace around JSON syntax is insignificant.

## Syntax versus application contract

- Invalid JSON has invalid syntax, such as `{'level': 'error'}` because it uses
  single quotes.
- Valid JSON can still violate an application contract. `[]` is valid JSON,
  but it is an array rather than the top-level object required by
  `iter_json_events`.
- `dict[str, Any]` means a Python dictionary with string keys and values of
  any Python type. `Any` does not convert a value or reject an empty string.

## Iterator contract

An iterable can produce an iterator. An iterator yields one value at a time;
calling `next()` consumes its next value. A function containing `yield` returns
a generator iterator, so work begins when the caller consumes it rather than
when the function is called.

For `iter_json_events`, each nonblank source line is parsed, checked to be a
dictionary, and then yielded as one event.

## Iterable, iterator, and generator

These concepts are related but not identical:

- An **iterable** can create an iterator. Lists, tuples, dictionaries, files,
  and ranges are iterable.
- An **iterator** remembers a traversal position and returns the next value
  through `next()`. When no values remain, it raises `StopIteration`.
- A **generator function** is a function whose body contains `yield`.
- Calling a generator function creates a **generator object**. That object is
  an iterator.

```python
numbers = [10, 20]          # iterable
iterator = iter(numbers)    # iterator

next(iterator)              # 10
next(iterator)              # 20
next(iterator)              # raises StopIteration
```

A `for` loop performs the `iter()` and repeated `next()` calls automatically
and stops when it receives `StopIteration`.

## What `yield` changes

A normal function runs immediately when called and finishes when it returns or
raises. Calling a generator function does not initially execute its body. It
returns a generator object that can be consumed later.

```python
def count_up_to(limit: int):
    print("generator started")
    current = 1
    while current <= limit:
        print("producing", current)
        yield current
        current += 1


counts = count_up_to(2)  # prints nothing
next(counts)              # prints messages, then returns 1
next(counts)              # resumes after the first yield and returns 2
next(counts)              # raises StopIteration
```

At each `yield`, Python:

1. produces one value for the consumer;
2. suspends the generator at that exact location;
3. preserves its local variables and current instruction position;
4. resumes immediately after that `yield` on the next request.

`yield` therefore means “produce a value and pause.” `return` means “finish
the generator.” Reaching the end of its body also finishes it, which appears to
the consumer as `StopIteration`.

## The connected-gears mental model

A generator pipeline is like connected gears, with one important detail: it is
normally **pull-driven and synchronous**. The gears do not turn in the
background. The downstream consumer initiates the movement by asking for a
value.

```text
consumer
   │ next()
   ▼
iter_error_events
   │ requests upstream values until one matches
   ▼
iter_json_events
   │ requests one source line at a time
   ▼
input lines
```

For example:

```python
parsed = iter_json_events(lines)
errors = iter_error_events(parsed)

first_error = next(errors)
```

That final `next()` pulls the pipeline:

1. `iter_error_events` requests an event from `iter_json_events`.
2. `iter_json_events` requests and parses one input line.
3. If the event is not an error, the filter requests another event.
4. When an error matches, it is yielded to the caller and the entire pipeline
   pauses.

There is no automatic thread, coroutine, parallelism, or background execution
in this pipeline. Every step runs on the caller's thread until a value is
yielded or the source is exhausted.

## Why the error-filter test proves laziness

The test's source records each item it produces:

```python
consumed: list[int] = []

def source():
    for index, level in enumerate(("info", "ERROR", "warning")):
        consumed.append(index)
        yield {"level": level, "index": index}
```

Creating the pipeline does not execute `source()`:

```python
errors = iter_error_events(source())
assert consumed == []
```

Requesting the first error consumes index `0`, rejects its `"info"` level,
then consumes and yields index `1`. The generator pauses there, so index `2`
has not been requested:

```python
assert next(errors) == {"level": "ERROR", "index": 1}
assert consumed == [0, 1]
```

An event without `level` produces `None` from `event.get("level")`. A non-string
level such as `123` also fails the `isinstance(level, str)` check. Both are
skipped safely without calling `.lower()` on an incompatible value.

## Lazy sequence versus lazy initialization

Kotlin's delegated lazy initialization computes and normally caches one value:

```kotlin
val configuration by lazy { loadConfiguration() }
```

A Python generator represents a sequence of values computed incrementally. It
is closer to Kotlin's `Sequence` builder or a Java `Stream`:

```kotlin
fun counts() = sequence {
    yield(1)
    yield(2)
}
```

```python
def counts():
    yield 1
    yield 2
```

The common principle is deferred computation on demand. The difference is
what is deferred:

- Kotlin `lazy`: usually one value, computed once and cached.
- Python generator/Kotlin `Sequence`: a stream of values, computed as the
  consumer advances.

Generators do not cache all previously yielded values. They are normally
one-shot: after exhaustion, iterating the same generator again produces
nothing. Call the generator function again to create a fresh traversal.

```python
values = counts()
list(values)  # [1, 2]
list(values)  # [] — the same generator is exhausted
list(counts())  # [1, 2] — a new generator
```

## Generator lifecycle, exhaustion, and `close()`

A generator object moves through a small lifecycle:

```text
created → running → suspended → running → ... → closed
```

- **Created:** the generator function has been called, but its body has not
  started.
- **Running:** Python is currently executing its body.
- **Suspended:** it yielded a value and retained its execution state.
- **Closed:** it returned, reached the end, raised an uncaught exception, or
  was explicitly closed.

`list(generator)` repeatedly requests values until the generator is exhausted.
The produced values belong to the new list; the generator does not retain them
for replay.

```python
values = (number * 2 for number in range(3))

list(values)  # [0, 2, 4]
next(values)  # raises StopIteration
list(values)  # []
```

`close()` asks a suspended generator to terminate by raising `GeneratorExit`
inside it. Closing is permanent, and calling `close()` on an already closed
generator is harmless. Printing the generator afterward still shows an object
because the variable retains a reference to that closed object.

The state can be inspected while experimenting:

```python
from inspect import getgeneratorstate

getgeneratorstate(values)  # "GEN_CLOSED"
```

## Sending values into a generator

`send(value)` is not equivalent to sending into a channel. It resumes a
suspended generator and makes its paused `yield` expression evaluate to the
sent value.

```python
def receiver():
    value = yield "ready"
    while value is not None:
        value = yield value * 2


worker = receiver()
next(worker)       # yields "ready" and pauses
worker.send(5)     # sends 5 inward; yields 10 outward
worker.send(7)     # sends 7 inward; yields 14 outward
worker.send(None)  # finishes and raises StopIteration
```

The same `yield` expression communicates in two directions:

```text
generator --yield output--> caller
generator <--send input----- caller
```

A newly created generator must first advance to its initial `yield`.
`send(None)` is equivalent to `next(generator)` for this purpose. Sending a
non-`None` value before the first suspension raises `TypeError`. Sending to an
exhausted generator raises `StopIteration`.

A generator expression has no explicit variable receiving sent values, so
`send()` is not a useful way to append data to it. For independently running
producers and consumers, a queue or channel is the appropriate abstraction.

## Generator expressions and eager lists

A generator expression uses parentheses and computes values on demand:

```python
squares = (number * number for number in range(1_000_000))
first = next(squares)
```

A list comprehension uses brackets and constructs every result immediately:

```python
squares = [number * number for number in range(1_000_000)]
```

For a simple streaming pipeline, a generator can use roughly constant
additional memory because it retains only its state and current values. A list
of all results requires O(n) memory. Total processing is still O(n) if every
source value is eventually consumed, but a consumer may stop early and avoid
processing the remainder entirely.

Calling `list(generator)` deliberately removes that streaming advantage for
the result: it pulls until exhaustion and stores every yielded item.

## Exception timing and propagation

Because execution is deferred, an exception inside a generator occurs when
the consumer reaches the failing operation, not when the generator object is
created:

```python
def values():
    yield 1
    raise RuntimeError("source failed")


items = values()  # no exception
next(items)       # returns 1
next(items)       # raises RuntimeError
```

Unless the generator deliberately catches an exception, it propagates through
the pipeline to the consumer. This matters for `iter_json_events`: malformed
input may not raise until `next(events)` or `list(events)` asks the parser to
reach that line.

## Generator-based context managers

`@contextmanager` adapts a generator into an object that follows the context
manager protocol used by `with`. Its single `yield` divides setup from cleanup:

```text
before yield → enter the `with` block
at yield     → run the caller's block
after yield  → leave the block normally
finally      → cleanup on both success and failure
```

For `measure_operation`, execution starts by reading the start time and pauses
at `yield`. The body of the caller's `with` statement then runs.

On normal completion, the generator resumes immediately after `yield`, so the
code assigns the `ok` status. If the body raises, `contextmanager` throws that
exception into the generator at the suspended `yield`. The surrounding
`except` path assigns `error`, and a bare `raise` propagates the original
exception. The `finally` block records the duration in either path.

```text
                    `with` body
                   /           \
             completes         raises
                |                 |
          status = "ok"     status = "error"
                |            re-raise original
                 \               /
                  `finally`: record event
```

A generator-based context manager must yield exactly once. Yielding zero times
or attempting to yield again while exiting violates the context-manager
contract.

## What `Iterator[None]` means

The annotation describes what the generator yields, not what an ordinary
function returns:

```python
def values() -> Iterator[int]:
    yield 1


@contextmanager
def measured() -> Iterator[None]:
    yield  # equivalent to `yield None`
```

`Iterator[None]` means that the generator yields `None`. With
`@contextmanager`, that yielded type becomes the type after `as`:

```python
with measured() as value:
    assert value is None
```

A context manager that exposes a resource instead uses that resource type:

```python
@contextmanager
def connection() -> Iterator[Connection]:
    resource = Connection()
    try:
        yield resource
    finally:
        resource.close()
```

Although the undecorated generator body is annotated as an iterator, the
decorated function is used by callers as a context manager.

## Python, Kotlin, and Java comparison

These are conceptual counterparts, not exact one-to-one equivalents:

| Purpose | Python | Kotlin | Java | Main behavior |
|---|---|---|---|---|
| Eager collection | `list` | `List` | `List` | Values are already materialized. |
| Lazy synchronous pipeline | Generator, generator expression, iterator | `Sequence` | `Stream` | Consumer pulls values; no background execution by itself. |
| Deferred single value | `cached_property` or explicit memoization | `lazy` delegate | `Supplier` plus memoization | Compute one value later, commonly cache it. |
| Asynchronous lazy stream | Async generator | `Flow` | `Flow.Publisher` or a reactive-streams publisher | Values may arrive across suspension/asynchronous boundaries; exact hot/cold rules differ. |
| Producer/consumer handoff | `asyncio.Queue` or `queue.Queue` | `Channel` | `BlockingQueue` | Producers put/send values that consumers receive; buffering is possible. |
| Resume a suspended computation with input | `generator.send(value)` | No direct `Sequence` equivalent; use coroutines/channels | No direct `Stream` equivalent | Synchronous two-way interaction at a specific suspension point. |
| Scoped setup and cleanup | Context manager with `with` | `use`, `try/finally` | `try-with-resources` | Cleanup occurs when the scope exits, including exceptional exits. |

The closest comparison for the current event functions is Python generator ↔
Kotlin `Sequence` ↔ Java `Stream`: all model lazy processing pipelines, not
independent message producers. Kotlin `Flow` and `Channel`, Java reactive
publishers and queues, and Python async generators and queues introduce
asynchronous or producer-driven behavior that this Week 3 pipeline does not
have.

## Practical tradeoffs

Generators are useful when:

- input may be large or even infinite;
- results can be processed one at a time;
- the consumer may stop early;
- pipeline stages should compose without materializing intermediate lists.

An eager list is often simpler when:

- all values are small and needed immediately;
- values require repeated traversal;
- random access, indexing, or `len()` is required;
- retaining a stable snapshot is more important than streaming.

The key design question is not “is lazy always faster?” It is “does the caller
need all results now, or can values flow through the system on demand?”
