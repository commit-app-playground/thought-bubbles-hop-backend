from prometheus_client import Counter

""" Service to record classified thoughts to Prometheus """

class PrometheusThoughtRecordingService:
    predicted_emotion_counter = Counter(
        'predicted_emotion_total', 'Total Count of Predicted Emotions', ['prediction'])

    def record(self, prediction_label):
        self.predicted_emotion_counter.labels(prediction_label).inc()
