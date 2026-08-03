#!/bin/bash
sh setup/ubuntu/font_setup.sh
sh setup/ubuntu/libs.sh

python3.8 -m venv venv_dre

source venv_dre/bin/activate
pip install --upgrade pip
pip install ipykernel
python3.8 -m ipykernel install --user --name venv_dre --display-name "Python 3.8 (DRE-Project)"

pip install "dask[diagnostics]"