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

# continuation of agent chat that disrupted last time
› implemented and first test function passed,
  the flow is :
  enumerate to generate line number for every possible object->continue evey empty striped item(dont need to raise error , we just pass from it)->then we understood the
  item is not empty and we go with load function (which i need some explanation about this function, defenition of the function says :Deserialize s (a str, bytes or
  bytearray instance containing a JSON document) to a Python object.)->i assume if loads returned without exception then we have a valid json object ->we check this object
  is a dict -> yield item

