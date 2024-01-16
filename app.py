# from flask_sqlalchemy import SQLAlchemy

# app.py
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.layers import TextVectorization
import joblib
import numpy as np

app = Flask(__name__)

# Load the translation model
model_path = "my_translation_model_gpu_v6.h5"
model_v6 = load_model(model_path)

# Load the TextVectorization instances   #MUST BE IN THE RIGHT PATH OF THE PROJECT
english_vectorizer_path = (
    "text_vectorizer_eng_data.joblib"  # of v6 model (14k vocab and 14 seq_length)
)
french_vectorizer_path = (
    "text_vectorizer_eng_data.joblib"  # of v6 model (14k vocab and 14 seq_length)
)

english_vectorizer = joblib.load(english_vectorizer_path)
french_vectorizer = joblib.load(french_vectorizer_path)


def translate_sentence(
    model, eng_text, eng_vectorization, fre_vectorization, sequence_length=14
):
    # Tokenize and pad the English input sentence
    eng_sequence = eng_vectorization(np.array([eng_text]))
    eng_sequence = pad_sequences(eng_sequence, maxlen=sequence_length, padding="post")

    # Initialize the decoder input with the start token
    fre_sequence = np.zeros((1, sequence_length), dtype=np.int32)
    fre_sequence[0, 0] = fre_vectorization.get_vocabulary().index("[start]")

    # Inference loop
    for i in range(1, sequence_length):
        predictions = model.predict([eng_sequence, fre_sequence])
        predicted_token_index = np.argmax(predictions[0, i - 1, :])
        fre_sequence[0, i] = predicted_token_index

        # Check for the end token
        if fre_vectorization.get_vocabulary()[predicted_token_index] == "[end]":
            break

    # Convert the predicted indices to French text
    translated_text = " ".join(
        [fre_vectorization.get_vocabulary()[idx] for idx in fre_sequence[0] if idx > 0]
    )
    if not ("[end]" in translated_text):
        translated_text += " [end]"

    # further processing (without the trained model) of the sentence....
    # to think about (ex. change cest with c'est in the french sentence)  (renverse preprocessing)

    return translated_text


def translate_text(input_text):
    translated_text = translate_sentence(
        model_v6, input_text, english_vectorizer, french_vectorizer, 14
    )

    return translated_text


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    input_text = request.form["input_text"]
    translated_text = translate_text(input_text)
    return jsonify({"translated_text": translated_text})


if __name__ == "__main__":
    app.run(debug=True)

# ##-----------------CODE POUR UN CHATBOT UTILISANT LES APIs DE GPT3
# # (Faut adapter les fichier js et css)-----------------##

# app = Flask(__name__)
# # create the extension
# db = SQLAlchemy()
# # create the app
# # configure the SQLite database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ma_database.db"
# # initialize the app with the extension
# db.init_app(app)


# class ChatExchange(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_message = db.Column(db.String(255))
#     assistant_response = db.Column(db.String(255))


# with app.app_context():
#     db.create_all()


# # from app.models import ChatExchange


# # Dans votre vue Flask pour afficher les échanges
# @app.route("/chat-history")  # Route pour afficher l'historique des échanges
# def show_chat_history():
#     chat_history = ChatExchange.query.all()
#     return render_template("index.html", chat_history=chat_history)


# q_list = []
# r_list = []


# @app.route("/hello/")
# def hello_world():
#     return "<p>Hello, World!</p>"


# @app.route("/")
# def hello():
#     return render_template("index.html")  # , messages=messages)


# @app.route("/prompt", methods=["POST"])
# def prompt():
#     message = {}
#     data = request.form["prompt"]
#     message["answer"] = ask_question_to_pdf.gpt3_completion(data)
#     # Enregistrez l'échange dans la base de données dès que la réponse d'OpenAI est générée
#     exchange = ChatExchange(user_message=data, assistant_response=message["answer"])
#     db.session.add(exchange)
#     db.session.commit()
#     return message


# @app.route("/question", methods=["GET"])
# def question():
#     q = ask_question_to_pdf.ask_question_to_pdf(
#         "Pose moi une question au hasard sur le texte", ask_question_to_pdf.filename
#     )
#     q_list.append(q)

#     return {"answer": q}


# @app.route("/answer", methods=["POST"])
# def reponse():
#     r = request.form["prompt"]
#     answer = ask_question_to_pdf.verif(q_list[-1], r, ask_question_to_pdf.filename)
#     exchange = ChatExchange(
#         user_message=q_list[-1],
#         assistant_response="Ma réponse : " + r + "; Correction : " + answer,
#     )
#     db.session.add(exchange)
#     db.session.commit()
#     return {"answer": answer}


# @app.route("/upload", methods=["POST"])
# def upload():
#     f = request.files["background"]
#     f.save("filename.pdf")
#     return "file uploaded"
