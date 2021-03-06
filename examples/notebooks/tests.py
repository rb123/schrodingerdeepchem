import os
import subprocess
import tempfile

import nbformat


def _notebook_read(path):
  """
  Parameters
  ----------
  path: str
  path to ipython notebook

  Returns
  -------
  nb: notebook object
  errors: list of Exceptions
  """

  with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
    args = [
        "jupyter-nbconvert", "--to", "notebook", "--execute",
        "--ExecutePreprocessor.timeout=60", "--output", fout.name, path
    ]
    subprocess.check_call(args)

    fout.seek(0)
    nb = nbformat.read(fout, nbformat.current_nbformat)

  errors = [output for cell in nb.cells if "outputs" in cell
            for output in cell["outputs"] \
            if output.output_type == "error"]

  return nb, errors


def test_protein_ligand_complex_notebook():
  nb, errors = _notebook_read("protein_ligand_complex_notebook.ipynb")
  assert errors == []
