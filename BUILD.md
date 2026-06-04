# Building & Publishing the C964 Site

This repo builds with [Jupyter Book](https://jupyterbook.org/) inside a
[uv](https://docs.astral.sh/uv/)-managed Python environment, defined by
`pyproject.toml` + `uv.lock` (both committed), so it reproduces identically on any
machine — no manual Python or pip setup.

## One-time, per machine

Install **uv**: <https://docs.astral.sh/uv/getting-started/installation/>
(Windows: `winget install astral-sh.uv`.) That is the only prerequisite — uv fetches
the pinned Python (3.12) and all dependencies for you.

## Build & publish

Run the deploy script from this folder:

    update_C964_site.bat

It prepares the env (`uv sync`), pulls latest from GitHub, builds the book
(`uv run jupyter-book build .`), commits + pushes the source to `main`, then
publishes `_build/html` to the `gh-pages` branch (`uv run ghp-import ...`).

Build only, no publish:

    uv run jupyter-book build .

> **Note:** the build *executes the ML example notebooks* (`_config.yml` has
> `execute_notebooks: force`), so it needs the scientific stack (scikit-learn,
> pandas, numpy, matplotlib, seaborn — all pinned here) and **internet access**
> (the notebooks load the Iris dataset from a URL). A full build takes a few minutes.

## Notebook kernels (important — was the cross-machine gotcha)

VSCode stamps each `.ipynb` with a unique, machine-specific kernel name, which broke
builds on other machines ("No such kernel"). This repo no longer depends on that:
`_config.yml` sets

    sphinx:
      config:
        nb_kernel_rgx_aliases:
          ".*": python3

which makes myst-nb ignore whatever kernel name is baked into a notebook and always
use the env's standard `python3` kernel (provided by `ipykernel` in the uv env). You
do **not** need to re-register kernels or normalize notebook metadata per machine.

To re-run a notebook after editing its code (and save fresh outputs), you can use the
included helper:

    uv run python _run_nb.py path/to/notebook.ipynb

## Dependencies / "requirements file"

With uv the dependencies live in `pyproject.toml` and are pinned in `uv.lock` — those
are the "requirement files." Add or upgrade with `uv add <package>` (commit both).
The legacy `requirements.txt` / `requirements-c964.txt` pip freezes are superseded by
`pyproject.toml` + `uv.lock`.

- Jupyter Book is pinned **`<2`** — 2.x is the incompatible mystmd rewrite.
- Python is pinned to **3.12** via `.python-version`. uv fetches it automatically.
- `sphinx-sitemap` is required (used in `_config.yml` `sphinx.extra_extensions`).
