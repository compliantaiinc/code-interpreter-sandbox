# code-interpreter-sandbox

Daytona snapshot for running user code safely — focused on document generation (DOCX/PDF via LibreOffice, PPTX via python-pptx).

## Setup

You'll need a Daytona account and API key. Create one at [app.daytona.io](https://app.daytona.io).

Copy the example env file and add your key:

```bash
cp .env.example .env
# edit .env and set DAYTONA_API_KEY
```

Optional overrides can go in `.env.local` (also gitignored).

Install dependencies:

```bash
pip install -r requirements.txt
```

## Building

Development snapshot:

```bash
make build-dev
```

Production snapshot:

```bash
make build-prod
```

Or run the Python scripts directly:

```bash
python build_dev.py
python build_prod.py
```

Builds register pre-built snapshots (`stepscale-sandbox-dev` and `stepscale-sandbox`) with 2 vCPU, 4 GiB RAM, and 3 GiB disk. Snapshot creation logs stream to stdout; set `timeout=0` so large image builds are not cut off.

## Usage

```python
from daytona import CreateSandboxFromSnapshotParams

from daytona_client import get_daytona

daytona = get_daytona()
sandbox = daytona.create(
    CreateSandboxFromSnapshotParams(snapshot="stepscale-sandbox")
)
response = sandbox.process.code_run('print("hello")')
print(response.result)
```

## Files

- `daytona_client.py` - loads `.env` / `.env.local` and returns a configured Daytona client
- `template.py` - declarative image definition (apt + pip packages)
- `build_dev.py` - dev snapshot build script
- `build_prod.py` - prod snapshot build script
- `Makefile` - build shortcuts
- `requirements.txt` - Python dependencies

## Docs

See [daytona.io/docs](https://www.daytona.io/docs) for sandbox, snapshot, and SDK details.
