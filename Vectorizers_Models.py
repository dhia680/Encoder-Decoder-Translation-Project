# IMPORTS
import pandas as pd
import string
import re
import time
import tensorflow as tf
from keras.layers import TextVectorization
from keras.models import load_model

# import numpy as np
# from keras.preprocessing.sequence import pad_sequences
# import joblib

# DATA Extraction (Have to be in the project folder)
data_path = "Dataset/fra_160K.txt"

df_raw1 = pd.read_csv(
    data_path,
    delimiter="\t",
    encoding="utf-8",
    header=None,
    names=["en", "fr"],
    index_col=False,
)
# df_raw1.head()

lang1 = "en"
lang2 = "fr"
# print(f"Number of sentences : {df_raw1.count()[0]}")


# Returning a list of tuples (corresponding eng-fre sentences)
def Create_pairs(dataframe):
    text_pairs = [
        (row["en"], "[start] " + row["fr"] + " [end]")
        for index, row in dataframe.iterrows()
    ]
    return text_pairs


# Create the pairs
text_pairs = Create_pairs(df_raw1)

# Define custom_standardization of the french vectorizer:
strip_chars = list(string.punctuation)
strip_chars.remove("[")
strip_chars.remove("]")
strip_chars = "".join(strip_chars)


def custom_standardization(input_string):
    lowercase = tf.strings.lower(input_string)
    return tf.strings.regex_replace(
        lowercase, "[%s]" % re.escape("".join(strip_chars)), ""
    )


# Parameters
model_number = 1  # 0-->v6 and 1-->v80
params = [[14, 14000], [20, 20000]]  # list of [seq_len, vocab_size]
sequence_length = params[model_number][0]
vocab_size = params[model_number][1]

# Default standardization for eng (strip string.punctuations)
eng_vectorization = TextVectorization(
    max_tokens=vocab_size,
    output_mode="int",
    output_sequence_length=sequence_length,
)
# Customized for french (strip specific punctuations)
fre_vectorization = TextVectorization(
    max_tokens=vocab_size,
    output_mode="int",
    output_sequence_length=sequence_length + 1,
    standardize=custom_standardization,
)

# Adapting (fitting) Vectorizers to the data :
train_eng_texts = [pair[0] for pair in text_pairs]
train_fre_texts = [pair[1] for pair in text_pairs]
start = time.time()
eng_vectorization.adapt(train_eng_texts)  # fitting the text vectorization layer to data
fre_vectorization.adapt(train_fre_texts)  # same (but unchanged data)
end = time.time()
print(f"Adapting both vectorizers execution time : {end - start:.2f}")

# Load the models
model_path_v6 = "my_translation_model_gpu_v6.h5"
model_path_v80 = "my_translation_model_gpu_v80.h5"
model_v6 = load_model(model_path_v6)  # model number 0
model_v80 = load_model(model_path_v80)  # model number 1
model = [model_v6, model_v80][model_number]


#
#
#
#
# --------------------------------------Commented code from the chatbot hackathon (I may use API) -------------------------
# from io import StringIO
# import os
# import fitz
# # import openai
# from dotenv import load_dotenv
# from nltk.tokenize import sent_tokenize
# # import aspose.words as aw

# load_dotenv()


# def open_file(filepath):
#     with open(filepath, "r", encoding="utf-8") as infile:
#         return infile.read()


# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.organization = os.getenv("OPENAI_ORGANIZATION")


# def read_pdf(filename):
#     context = ""

#     # Open the PDF file
#     with fitz.open(filename) as pdf_file:
#         # Get the number of pages in the PDF file
#         num_pages = pdf_file.page_count

#         # Loop through each page in the PDF file
#         for page_num in range(num_pages):
#             # Get the current page
#             page = pdf_file[page_num]

#             # Get the text from the current page
#             page_text = page.get_text().replace("\n", "")

#             # Append the text to context
#             context += page_text
#     return context


# def split_text(text, chunk_size=5000):
#     """
#     Splits the given text into chunks of approximately the specified chunk size.

#     Args:
#     text (str): The text to split.

#     chunk_size (int): The desired size of each chunk (in characters).

#     Returns:
#     List[str]: A list of chunks, each of approximately the specified chunk size.
#     """

#     chunks = []
#     current_chunk = StringIO()
#     current_size = 0
#     sentences = sent_tokenize(text)
#     for sentence in sentences:
#         sentence_size = len(sentence)
#         if sentence_size > chunk_size:
#             while sentence_size > chunk_size:
#                 chunk = sentence[:chunk_size]
#                 chunks.append(chunk)
#                 sentence = sentence[chunk_size:]
#                 sentence_size -= chunk_size
#                 current_chunk = StringIO()
#                 current_size = 0
#         if current_size + sentence_size < chunk_size:
#             current_chunk.write(sentence)
#             current_size += sentence_size
#         else:
#             chunks.append(current_chunk.getvalue())
#             current_chunk = StringIO()
#             current_chunk.write(sentence)
#             current_size = sentence_size
#     if current_chunk:
#         chunks.append(current_chunk.getvalue())
#     return chunks


# filename = os.path.join(os.path.dirname(__file__), "filename.pdf")
# document = read_pdf(filename)
# chunks = split_text(document)


# def gpt3_completion(txt):
#     a = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": txt},
#         ],
#     )
#     return a["choices"][0]["message"]["content"]


# text = "Brahim le crétin est une légende de l'école des ponts"


# def ask_question_to_pdf(txt, filename):
#     document = read_pdf(filename)
#     chunks = split_text(document)
#     a = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": chunks[0]},
#             {"role": "user", "content": txt},
#         ],
#     )
#     return a["choices"][0]["message"]["content"]


# def verif(question, response, filename):
#     document = read_pdf(filename)
#     chunks = split_text(document)
#     a = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": chunks[0]},
#             {
#                 "role": "system",
#                 "content": "si ma réponse n'a pas de lien avec la question dis moi que j'ai tout faux",
#             },
#             {"role": "assistant", "content": question},
#             {"role": "user", "content": response},
#             {
#                 "role": "user",
#                 "content": "est ce que ma réponse est correcte et sinon quelle était la bonne réponse",
#             },
#         ],
#     )
#     return a["choices"][0]["message"]["content"]


# def fichier_txt(path):
#     f = open_file(
#         path, "r"
#     )  # Essai est mon fichier.txt que vous pouvez voir juste au dessus )
#     readlines = f.readlines()
#     f.close()
#     final_text = readlines.replace("\n", "")
#     return final_text
