from flask import Flask
from utils import ask_question_to_pdf

app = Flask(__name__)
q_list = []
r_list = []
@app.route("/hello/")
def hello_world():
    return "<p>Hello, World!</p>"

from flask import render_template

@app.route('/')
def hello():
    return render_template('index.html')


from flask import request
@app.route('/prompt', methods=['POST'])

def prompt():
    message = {}
    data = request.form['prompt']
    message['answer']= ask_question_to_pdf.gpt3_completion(data)
    return message

@app.route("/question", methods=["GET"])
def question():
    q = ask_question_to_pdf.ask_question_to_pdf("Pose moi une question sur le texte")
    q_list.append(q)
    return {"question" : q}

@app.route("/reponse", methods=["POST"])
def reponse():
    r = request.form["prompt"]
    r_list.append(r)
    return {"reponse" : r}

@app.route("/correct", methods=["GET"])
def correct():
    c = ask_question_to_pdf.verif(q_list[-1],r_list[-1])
    return {"correct" : c}
