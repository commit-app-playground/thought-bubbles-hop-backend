from flask import Flask, request
import os
from services.thought_classification_service import ThoughtClassificationService
from dao.sqlite_thoughts_dao import SQLiteThoughtsDao
import db
from services.thought_predictor_service import ThoughtPredictorService
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'thoughtbubbles.sqlite')
)
with app.app_context():
    db.init_app(app)
    db.init_db()

port = (os.environ.get("PORT", 80))

# Instantiate dependencies
thoughts_dao = SQLiteThoughtsDao()
thoughts_predictor = ThoughtPredictorService()


@app.route("/")
def hello():
    return {
        "status": "Your application is running"
    }


@app.route('/findRelatedThoughts', methods=['POST'])
def findRelatedThoughts():
    thought = request.json['thoughtText']
    return ThoughtClassificationService(thoughts_dao, thoughts_predictor).classify_and_return_related_thoughts(thought)


if __name__ == '__main__':
    app.run(debug=True, port=port, host="0.0.0.0")
