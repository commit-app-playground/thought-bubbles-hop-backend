import unittest
from unittest.mock import patch, MagicMock
from services.thought_classification_service import ThoughtClassificationService


class ThoughtClassificationServiceSpec(unittest.TestCase):
    @patch('dao.sqlite_thoughts_dao.SQLiteThoughtsDao')
    @patch('services.thought_predictor_service.ThoughtPredictorService')
    def test_should_classify_and_return_all_related_thoughts(self, mock_dao, mock_predictor):
        test_thought_text = 'This is a happy happy thought'
        test_user_id = '1234'
        test_classification_ids = [0]
        test_first_related_thought = 'This is a joyful thought'
        test_second_related_thought = 'This is an ecstatic thought'
        test_related_thoughts = [
            {'content': test_first_related_thought},
            {'content': test_second_related_thought}
        ]
        mock_predictor.predict_classification_ids = MagicMock(
            return_value=test_classification_ids)
        mock_dao.query_thoughts_by_classification_ids = MagicMock(
            return_value=test_related_thoughts)

        result = ThoughtClassificationService(
            mock_dao, mock_predictor).classify_and_return_related_thoughts(test_user_id, test_thought_text)

        mock_predictor.predict_classification_ids.assert_called_with(
            test_thought_text)
        mock_dao.query_thoughts_by_classification_ids.assert_called_with(
            test_user_id, test_classification_ids)
        self.assertEqual(result, {
            'thoughts': [{
                'text': test_first_related_thought
            },
                {
                'text': test_second_related_thought
            }]
        })
