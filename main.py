from flask import Flask
import ask_question_to_pdf
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import render_template

app = Flask(__name__)


# create the extension
db = SQLAlchemy()
# create the app
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ma_database.db"
# initialize the app with the extension
db.init_app(app)


class ChatExchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(255))
    assistant_response = db.Column(db.String(255))


with app.app_context():
    db.create_all()


# from app.models import ChatExchange


# Dans votre vue Flask pour afficher les échanges
@app.route("/chat-history")  # Route pour afficher l'historique des échanges
def show_chat_history():
    chat_history = ChatExchange.query.all()
    return render_template("index.html", chat_history=chat_history)


q_list = []
r_list = []


@app.route("/hello/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/")
def hello():
    return render_template("index.html")  # , messages=messages)


@app.route("/prompt", methods=["POST"])
def prompt():
    message = {}
    data = request.form["prompt"]
    message["answer"] = ask_question_to_pdf.gpt3_completion(data)
    # Enregistrez l'échange dans la base de données dès que la réponse d'OpenAI est générée
    exchange = ChatExchange(user_message=data, assistant_response=message["answer"])
    db.session.add(exchange)
    db.session.commit()
    return message


@app.route("/question", methods=["GET"])
def question():
    q = ask_question_to_pdf.ask_question_to_pdf("Pose moi une question au hasard sur le texte",ask_question_to_pdf.filename)
    q_list.append(q)
    return {"answer": q}


@app.route("/answer", methods=["POST"])
def reponse():
    r = request.form["prompt"]
    answer = ask_question_to_pdf.verif(q_list[-1], r, ask_question_to_pdf.filename)
    return {"answer": answer}


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["background"]
    f.save("filename.pdf")
    return "file uploaded"
