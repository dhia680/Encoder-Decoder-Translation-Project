## An english to french Machine Translation Web Tool - powered by an RNN (LSTM based Seq2Seq Model)

### Install
- when opening VSCode, install the suggested extensions (Python, Black Formatter and Pylance)
- create your python environment `python3 -m venv .venv`. Make sure to have a python version that tensorflow supports (ex. 3.11.4)
- use Gitbash terminal
- activate your environment with `source activate path\to\activation\file`
- run the server with `python app.py`

The server should answer on http://localhost:5000

You can deactivate the environment with `deactivate`.

## Adding librairies
If you need to use new librairies, you can do it with pip
`pip install [library name]` or `pip3 install [library name]` or 'conda install'


## The Project
- This is an academic project in the context of a "introduction to software development" course at Ecole des Ponts et Chaussées.
- The dataset exists in the folder Dataset and was taken from Kaggle open datasets.
- The provided python notebook contains data preprocessing and vectorization, model definition and training and inference. It's the main part of the project.
- The web interface is developed using python (flask toolkit) for backend and html/js/css for frontend.

### Requirements :
- Actually, not all the packages in the file requirements.txt are required for this project. This file will be soon updated.

### N.B:
This is my 1st NLP project. So it means something to me. <br>
It was trained on a single T4 GPU for less than 1h, on a vocabulary size of around 10K and a maximum sequence length of 20. <br>
Hence, you shouldn't expect it to perform very well eventhough it showed descent results 😁. <br>
I will add a transformer-based new version and scale compute and data budget.
