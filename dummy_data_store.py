"""Dummy data store to test storing thoughts in-memory without a database"""

__current_next_id = 1

stored_thoughts = []
stored_thought_classifications = []


def get_next_id():
    global __current_next_id
    next_id = __current_next_id
    __current_next_id += 1
    return next_id


def query_thoughts_by_classification_ids(classification_ids):
    matched_classified_thoughts = list(filter(lambda thought_classification: (
        thought_classification.classification_id in classification_ids), stored_thought_classifications))
    matched_thought_ids = list(map(lambda classified_thought: (
        classified_thought.thought_id), matched_classified_thoughts))  # TODO: Should only be the unique IDs
    matched_thoughts = list(filter(lambda thought: (
        thought.id in matched_thought_ids), stored_thoughts))

    return matched_thoughts


def insert_thought_with_classifications(classified_thought):
    stored_thought = StoredThought(
        classified_thought.id, classified_thought.text)
    stored_thoughts.append(stored_thought)

    thought_classifications = [ThoughtClassification(
        classified_thought.id, classification_id) for classification_id in classified_thought.classification_ids]
    for thought_classification in thought_classifications:
        stored_thought_classifications.append(thought_classification)


class StoredThought:
    def __init__(self, id, text):
        self.id = id
        self.text = text


class ThoughtClassification:
    def __init__(self, thought_id, classification_id):
        self.thought_id = thought_id
        self.classification_id = classification_id
