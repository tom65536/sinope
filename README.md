# sinope
Test Project for a Jupyter Kernel

## How To Run (as a Developer)

### Install the Kernel
```bash
poetry install
poetry run python -m sinope.sinope_kernel install --user
```

### Run your local Jupyter Lab Instance
```bash
python -m venv jupyterlab.venv
. jupyterlab.venv/bin/activate
pip install jupyterlab
jupyterlab.venv/bin/jupyter lab
```
