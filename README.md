# Plugin System

A type-safe plugin system built with Protocol, Generic, and dataclass.

## Package Structure

```
src/plugin_system/
├── protocol.py       # Plugin protocol (contract)
├── models.py         # dataclass Record with validation
├── registry.py       # Generic Registry[T]
├── core.py           # Dispatcher (core logic)
├── plugins/          # Plugin implementations
│   ├── json_fmt.py
│   ├── csv_fmt.py
│   └── text_fmt.py
└── cli.py            # Assembly point (registers plugins)
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
plugin-system --format json --name "Alice" --value 42
```

## Quality Checks

```bash
mypy --strict src
pytest
pytest --cov=plugin_system
```

## How to Add Your Own Plugin

1. Create a new file in `src/plugin_system/plugins/`, e.g. `xml_fmt.py`.

2. Implement two things (no imports of protocol, no inheritance):
   ```python
   from plugin_system.models import Record

   class XmlFormatter:
       @property
       def name(self) -> str:
           return "xml"

       def format(self, record: Record) -> str:
           return f"<record><name>{record.name}</name></record>"
   ```

3. Register it in `cli.py`:
   ```python
   registry.register("xml", XmlFormatter())
   ```

4. Done. The core (`core.py`) is not modified.