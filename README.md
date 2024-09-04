# getchar

Cross-platform non-blocking stdin reading.

Variant of the `readchar` module (which is blocking).

## How to use

```python
from getchar import getkeys

while True:
    keys = getkeys()
    if len(keys) > 0:
        print(keys)
```

`getkeys()` returns a list of keys. Length = 0 if no input.
