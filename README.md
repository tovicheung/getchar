# getchar

Cross-platform non-blocking stdin reading.

Variant of the `readchar` module (which is blocking).

## Installation

```
pip install getchar
```

## How to use

```python
from getchar import getkeys

while True:
    keys = getkeys()
    if len(keys) > 0:
        print(keys)
```

`getkeys()` is non-blocking and returns a list of keys. An empty list is returned if there is no input.
