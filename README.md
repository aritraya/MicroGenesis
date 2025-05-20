# MicroGenesis

A Python project template.

## Installation

```bash
pip install -e .
```

## Usage

```python
from microgenesis.example import Example

example = Example(name="World")
print(example.greet())  # Output: Hello from World!
```

## Development

### Setup Development Environment

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
python tests/run_tests.py
```