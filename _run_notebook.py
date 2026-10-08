# -*- coding: utf-8 -*-
"""Execute po_leadtime_hgboost.ipynb and save outputs back into the file."""
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

path = Path(__file__).resolve().parent / "po_leadtime_hgboost.ipynb"
nb = nbformat.read(path, as_version=4)


def _label(cell):
    source = cell.source if isinstance(cell.source, str) else "".join(cell.source)
    lines = source.strip().splitlines()
    return lines[0][:100] if lines else "(empty)"


def _on_start(cell, cell_index):
    print(f"START {cell_index:02d} {time.strftime('%H:%M:%S')} {_label(cell)}", flush=True)


def _on_executed(cell, cell_index, execute_reply):
    print(f"DONE  {cell_index:02d} {time.strftime('%H:%M:%S')} {execute_reply.get('status')}", flush=True)
    nbformat.write(nb, path)


client = NotebookClient(
    nb,
    timeout=None,
    kernel_name="python3",
    resources={"metadata": {"path": str(path.parent)}},
    on_cell_start=_on_start,
    on_cell_executed=_on_executed,
)
client.execute()
print("NOTEBOOK FINISHED", time.strftime("%H:%M:%S"), flush=True)
