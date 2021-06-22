from db import get_db

"""Code to query for and insert records into the SQLite DB"""


def query_thoughts_by_classification_ids(classification_ids):
    db = get_db()

    formatted_classification_ids = ([str(id) for id in classification_ids])
    sql = 'SELECT t.* FROM thoughts t INNER JOIN thought_classifications tc ON t.id = tc.thought_id WHERE tc.classification_id IN (%s)' % ','.join(
        '?'*len(formatted_classification_ids))
    return db.execute(sql, formatted_classification_ids).fetchall()


def insert_thought_with_classifications(classified_thought):
    stored_thought = ThoughtRecord(
        classified_thought.id, classified_thought.text)
    inserted_thought_id = __insert_thought(stored_thought)
    __insert_thought_classifications(classified_thought, inserted_thought_id)


def __insert_thought(stored_thought):
    db = get_db()

    sql = ''' INSERT INTO thoughts (content) VALUES (?) '''
    cur = db.cursor()
    cur.execute(sql, (stored_thought.text,))
    db.commit()

    return cur.lastrowid


def __insert_thought_classifications(classified_thought, inserted_thought_id):
    db = get_db()

    thought_classifications = [ThoughtClassificationRecord(inserted_thought_id, int(
        classification_id)) for classification_id in classified_thought.classification_ids]
    for thought_classification in thought_classifications:
        db.execute(
            'INSERT INTO thought_classifications (thought_id, classification_id) VALUES (?, ?)', (
                thought_classification.thought_id, thought_classification.classification_id)
        )
        db.commit()


class ThoughtRecord:
    def __init__(self, id, text):  # TODO: Add created date
        self.id = id
        self.text = text


class ThoughtClassificationRecord:
    def __init__(self, thought_id, classification_id):
        self.thought_id = thought_id
        self.classification_id = classification_id
