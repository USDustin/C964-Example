"""Dev helper: execute notebooks with the env's python3 kernel, save outputs on
success, report first error on failure. Not part of the site build. Usage:
    uv run python _run_nb.py <notebook.ipynb> [more.ipynb ...]
"""
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

for path in sys.argv[1:]:
    p = Path(path)
    nb = nbformat.read(p, as_version=4)
    client = NotebookClient(
        nb, timeout=300, kernel_name="python3",
        resources={"metadata": {"path": str(p.parent)}},
    )
    try:
        client.execute()
        nbformat.write(nb, p)
        print(f"PASS  {path}")
    except CellExecutionError:
        # surface the failing cell's exception (last line of the traceback)
        lines = [l for l in (str(client.__dict__) and "") .splitlines()]  # noop
        # pull from the notebook's recorded error output
        err = "unknown"
        for cell in nb.cells:
            for o in cell.get("outputs", []):
                if o.get("output_type") == "error":
                    err = f'{o.get("ename")}: {o.get("evalue")}'
        print(f"FAIL  {path} :: {err[:200]}")
    except Exception as e:
        print(f"FAIL  {path} :: {type(e).__name__}: {str(e)[:180]}")
