import data_store
import predictor

"""Service to classify thoughts"""


def classify_and_return_related_thoughts(thought_text):
    classified_thought = __classify_thought(thought_text)
    related_thoughts = __find_related_thoughts(classified_thought)
    __store_classified_thought(classified_thought)

    thoughts_json = [{"text": related_thought['content']}
                     for related_thought in related_thoughts]

    return {
        "thoughts": thoughts_json
    }


def __classify_thought(thought_text):
    predicted_classification_ids = predictor.predict_classification_ids(
        thought_text)
    # Note that the thought ID will be overwritten by the SQL insert
    return ClassifiedThought(0, thought_text, predicted_classification_ids)


def __find_related_thoughts(classified_thought):
    return data_store.query_thoughts_by_classification_ids(classified_thought.classification_ids)


def __store_classified_thought(classified_thought):
    data_store.insert_thought_with_classifications(classified_thought)


class ClassifiedThought:
    def __init__(self, id, text, classification_ids):
        self.id = id
        self.text = text
        self.classification_ids = classification_ids
