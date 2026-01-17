# ifc

E2B sandbox template used as the code interpreter for the main IFC project. Provides an isolated environment for executing user code safely.

## Setup

You'll need an E2B account and API key. Grab one from [e2b.dev/dashboard](https://e2b.dev/dashboard).

Set your API key:
```bash
export E2B_API_KEY=your_api_key_here
```

Or throw it in a `.env` file if you prefer.

Install the E2B CLI:
```bash
pip install e2b
```

## Building

Development build:
```bash
make e2b-build-dev
```

Production build:
```bash
make e2b-build-prod
```

Or run the Python scripts directly:
```bash
python build_dev.py
python build_prod.py
```

## Usage

```python
from e2b import Sandbox

sandbox = Sandbox.create('ifc')
# do stuff with your sandbox
```

## Files

- `template.py` - sandbox configuration
- `build_dev.py` - dev build script
- `build_prod.py` - prod build script
- `Makefile` - build shortcuts

## Docs

Check [e2b.dev/docs](https://e2b.dev/docs) for more details on working with E2B sandboxes.
