## An english to french Machine Translation Web Tool based on LSTM based Seq2Seq Model

### Install
- when opening VSCode, install the suggested extensions (Python, Black Formatter and Pylance)
- create your python environment `python3 -m venv .venv`. Make sure to have a python version that tensorflow supports (ex. 3.11.4)
- Use Gitbush terminal
- activate your environment with `source activate path\to\activation\file`
- run the server with `python app.py`

The server should answer on http://localhost:5000

You can deactivate the environment with `deactivate`.

## Adding librairies
if you need to use new librairies, you can do it with pip
`pip install [library name]` or `pip3 install [library name]` or 'conda install'


## The Project
- This is an academic project in the context of a "introduction to software development" course at Ecole des Ponts.
- The dataset exists in the folder Dataset and was taken from Kaggle open datasets.
- The provided python notebook contains data preprocessing and vectorization, model definition and training and inference.
- The web interface is developed using python for backend and html/js/css for frontend.

