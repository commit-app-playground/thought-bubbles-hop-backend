from dao.sqlite_thoughts_dao import SQLiteThoughtsDao
from services.thought_predictor_service import ThoughtPredictorService
from models.classified_thought import ClassifiedThought

"""Service to classify thoughts"""


class ThoughtClassificationService:
    def __init__(self, dao: SQLiteThoughtsDao, predictor: ThoughtPredictorService):
        self.dao = dao
        self.predictor = predictor

    def classify_and_return_related_thoughts(self, thought_text):
        classified_thought = self.__classify_thought(thought_text)
        related_thoughts = self.__find_related_thoughts(classified_thought)
        self.__store_classified_thought(classified_thought)

        thoughts = [{"text": related_thought['content']}
                    for related_thought in related_thoughts]

        return {
            "thoughts": thoughts
        }

    def __classify_thought(self, thought_text):
        predicted_classification_ids = self.predictor.predict_classification_ids(
            thought_text)
        # Note that the thought ID will be overwritten by the SQL insert
        return ClassifiedThought(0, thought_text, predicted_classification_ids)

    def __find_related_thoughts(self, classified_thought):
        return self.dao.query_thoughts_by_classification_ids(classified_thought.classification_ids)

    def __store_classified_thought(self, classified_thought):
        self.dao.insert_thought_with_classifications(classified_thought)
