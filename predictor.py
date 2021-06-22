import tensorflow as tf
from tensorflow import keras
import numpy as np
from transformers import AutoTokenizer
from flask import current_app
from prometheus_client import Counter

"""Service to run thoughts through the trained ML model and get predictions"""


class ThoughtClassificationPredictor:
    SEQ_LEN = 80  # Note that this was based on the dataset where the max number of words in across all the phrases was ~80

    label_dict = {
        0: 'joy',
        1: 'fear',
        2: 'anger',
        3: 'sadness',
        4: 'disgust',
        5: 'shame',
        6: 'guilt'
    }
    predicted_emotion_counter = Counter(
        'predicted_emotion_total', 'Total Count of Predicted Emotions', ['prediction'])

    def __init__(self):
        self.model = keras.models.load_model("thought_classifier_model")
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')

    def predict_classification_ids(self, thought_text):
        prepped_data = self.__prep_data(thought_text)
        predictions = self.model.predict(prepped_data)

        self.__print_predictions(thought_text, predictions)

        # Only return the top one for now
        prediction = np.argmax(predictions[0])
        self.__record_prediction(prediction)
        # TODO: Support returning multiple classifications above a certain threshold
        return [prediction]

    def __prep_data(self, text):
        tokens = self.tokenizer.encode_plus(text,
                                            max_length=self.SEQ_LEN,
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

    def __record_prediction(self, prediction):
        prediction_label = self.label_dict[prediction]
        self.predicted_emotion_counter.labels(prediction_label).inc()

    def __print_predictions(self, thought_text, predictions):
        with current_app.app_context():  # TODO: There has to be a better way to log from the app context
            log_string = ""  # Build up the log string and log once such that it does not get clobbered from concurrent requests
            log_string += f"printing predictions for thought '{thought_text}'\n"

            for result in predictions:
                max_i = 0
                max_probability = 0
                for i, probability in enumerate(result):
                    log_string += f"emotion: {self.label_dict[i]}\nprobability: {probability}\n"

                    if probability > max_probability:
                        max_probability = probability
                        max_i = i

                log_string += f"predicted predominant emotion: {self.label_dict[max_i]}"
                current_app.logger.info(log_string)
