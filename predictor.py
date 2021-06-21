import tensorflow as tf
from tensorflow import keras
import numpy as np
from transformers import AutoTokenizer
from flask import current_app

SEQ_LEN = 80 # Note that this was based on the dataset where the max number of words in across all the phrases was ~80
__model = None
__tokenizer = None

def init_predictor():
    global __model
    global __tokenizer

    __model = keras.models.load_model("thought_classifier_model")
    __tokenizer = AutoTokenizer.from_pretrained('bert-base-cased') # Case matters for sentiment in general, e.g. when shouting on the internet

def predict_classification_ids(thought_text):
    global __model

    prepped_data = __prep_data(thought_text)
    predictions = __model.predict(prepped_data)

    __print_predictions(thought_text, predictions)

    # Only return the top one for now
    return [np.argmax(predictions[0])] # TODO: Support returning multiple classifications above a certain threshold

def __prep_data(text):
    global __tokenizer
    SEQ_LEN = 80 # Based on analysis of the PsychEXP dataset, the max length of any phrase was 80 words

    tokens = __tokenizer.encode_plus(text,
                               max_length=SEQ_LEN,
                               truncation=True,
                               padding="max_length",
                               add_special_tokens=True,
                               return_token_type_ids=False,
                               return_attention_mask=True,
                               return_tensors='tf')
    return {
        'input_ids': tf.cast(tokens['input_ids'], tf.float64),
        'attention_mask': tf.cast(tokens['attention_mask'], tf.float64)
    }

def __print_predictions(thought_text, predictions):
    with current_app.app_context(): # TODO: There has to be a better way to log from the app context
        log_string = "" # Build up the log string and log once such that it does not get clobbered from concurrent requests

        label_dict = {
            0: 'joy',
            1: 'fear',
            2: 'anger',
            3: 'sadness',
            4: 'disgust',
            5: 'shame',
            6: 'guilt'
        }

        log_string += f"printing predictions for thought '{thought_text}'\n"

        for result in predictions:
            max_i = 0
            max_probability = 0
            for i, probability in enumerate(result):
                log_string += f"emotion: {label_dict[i]}\nprobability: {probability}\n"

                if probability > max_probability:
                    max_probability = probability
                    max_i = i

            log_string += f"predicted predominant emotion: {label_dict[max_i]}"
            current_app.logger.info(log_string)