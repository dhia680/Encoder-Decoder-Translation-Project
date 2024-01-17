# app.py
from flask import Flask, render_template, request, jsonify
from keras.preprocessing.sequence import pad_sequences
import Vectorizers_Models
import numpy as np


app = Flask(__name__)

# Load the model (after choosing 'model_number' in Vectorizers_Models.py)
model = Vectorizers_Models.model

# Calling the vectorizers
english_vectorizer = Vectorizers_Models.eng_vectorization
french_vectorizer = Vectorizers_Models.fre_vectorization


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

    return translated_text.capitalize()


def translate_text(input_text):
    translated_text = translate_sentence(
        model,
        input_text,
        english_vectorizer,
        french_vectorizer,
        Vectorizers_Models.sequence_length,
    )
    return translated_text


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    input_text = request.form["input_text"]
    translated_text = translate_text(input_text)
    cleaned_text = translated_text.replace("[start]", "").replace("[end]", "").strip()
    return jsonify({"translated_text": cleaned_text})


if __name__ == "__main__":
    app.run(debug=False)


#
#
#
#
# ##-----------VERSION utilisant les Vectorizers téléchargés (mais posant problème car ne récupère pas exactement le même Vectorizer)---------------------------
# # app.py
# from flask import Flask, render_template, request, jsonify

# # import tensorflow as tf
# # from keras.models import load_model
# from keras.preprocessing.sequence import pad_sequences

# # from keras.layers import TextVectorization
# import Vectorizers_Models

# # import joblib
# import numpy as np

# # import re, string

# app = Flask(__name__)

# # # Load the models
# # model_number = 1
# # model_path_v6 = "my_translation_model_gpu_v6.h5"
# # model_path_v80 = "my_translation_model_gpu_v80.h5"
# # model_v6 = load_model(model_path_v6)  # model number 0
# # model_v80 = load_model(model_path_v80)  # model number 1
# # seq_len = [14, 20][model_number]
# # model = [model_v6, model_v80][model_number]
# model = Vectorizers_Models.model

# # # Load the TextVectorization trained instances (config & weights) #MUST BE IN THE SAME PATH AS THE PROJECT
# # eng_vectorization_data_v6 = joblib.load("text_vectorizer_eng_data.joblib")
# # fre_vectorization_data_v6 = joblib.load("text_vectorizer_fr_data.joblib")
# # eng_vectorization_data_v80 = joblib.load("text_vectorizer_eng_20k-vocab20(v80).joblib")
# # fre_vectorization_data_v80 = joblib.load("text_vectorizer_fr_20k-vocab20(v80).joblib")

# # # Remove custom standardization from configurations (why : because otherwise weights loading may raise errors)
# # eng_vectorization_data_v6["config"]["standardize"] = None
# # fre_vectorization_data_v6["config"]["standardize"] = None
# # eng_vectorization_data_v80["config"]["standardize"] = None
# # fre_vectorization_data_v80["config"]["standardize"] = None

# # # redefine custom_standardization of the french vectorizer:
# # strip_chars = list(string.punctuation)
# # strip_chars.remove("[")
# # strip_chars.remove("]")
# # strip_chars = "".join(strip_chars)


# # def custom_standardization(input_string):
# #     lowercase = tf.strings.lower(input_string)
# #     return tf.strings.regex_replace(lowercase, "[%s]" % re.escape(strip_chars), "")


# # # Create the TextVectorization layers by taking the configs of the loaded instances
# # english_vectorizer = [
# #     TextVectorization.from_config(eng_vectorization_data_v6["config"]),
# #     TextVectorization.from_config(eng_vectorization_data_v80["config"]),
# # ][model_number]
# # french_vectorizer = [
# #     TextVectorization.from_config(fre_vectorization_data_v6["config"]),
# #     TextVectorization.from_config(fre_vectorization_data_v80["config"]),
# # ][model_number]

# # # Reassign the custom standardization function to the french vectorizer
# # french_vectorizer._custom_standardization = custom_standardization

# # # Set the weights for the layers
# # english_vectorizer.set_weights(
# #     [eng_vectorization_data_v6["weights"], eng_vectorization_data_v80["weights"]][
# #         model_number
# #     ]
# # )
# # french_vectorizer.set_weights(
# #     [fre_vectorization_data_v6["weights"], fre_vectorization_data_v80["weights"]][
# #         model_number
# #     ]
# # )

# ## RUN the file Vectorizers_Models before (once) !
# english_vectorizer = Vectorizers_Models.eng_vectorization
# french_vectorizer = Vectorizers_Models.fre_vectorization


# def translate_sentence(
#     model, eng_text, eng_vectorization, fre_vectorization, sequence_length=14
# ):
#     # Tokenize and pad the English input sentence
#     eng_sequence = eng_vectorization(np.array([eng_text]))
#     eng_sequence = pad_sequences(eng_sequence, maxlen=sequence_length, padding="post")

#     # Initialize the decoder input with the start token
#     fre_sequence = np.zeros((1, sequence_length), dtype=np.int32)
#     fre_sequence[0, 0] = fre_vectorization.get_vocabulary().index("[start]")

#     # Inference loop
#     for i in range(1, sequence_length):
#         predictions = model.predict([eng_sequence, fre_sequence])
#         predicted_token_index = np.argmax(predictions[0, i - 1, :])
#         fre_sequence[0, i] = predicted_token_index

#         # Check for the end token
#         if fre_vectorization.get_vocabulary()[predicted_token_index] == "[end]":
#             break

#     # Convert the predicted indices to French text
#     translated_text = " ".join(
#         [fre_vectorization.get_vocabulary()[idx] for idx in fre_sequence[0] if idx > 0]
#     )
#     if not ("[end]" in translated_text):
#         translated_text += " [end]"

#     return translated_text


# def translate_text(input_text):
#     translated_text = translate_sentence(
#         model,
#         input_text,
#         english_vectorizer,
#         french_vectorizer,
#         Vectorizers_Models.sequence_length,
#     )
#     return translated_text


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/translate", methods=["POST"])
# def translate():
#     input_text = request.form["input_text"]
#     translated_text = translate_text(input_text)
#     cleaned_text = translated_text.replace("[start]", "").replace("[end]", "").strip()
#     return jsonify({"translated_text": cleaned_text})


# if __name__ == "__main__":
#     app.run(debug=False)
#
#
#
#
# ##-----------------CODE POUR UN CHATBOT UTILISANT LES APIs DE GPT3 (FAIT LES IMPORTS NECESSAIRES)
# from flask_sqlalchemy import SQLAlchemy
# # Autres import
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
