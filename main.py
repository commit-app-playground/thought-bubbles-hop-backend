from flask import Flask, request, g
import os

from flask.ctx import after_this_request
from services.thought_classification_service import ThoughtClassificationService
from dao.sqlite_thoughts_dao import SQLiteThoughtsDao
import db
from services.thought_predictor_service import ThoughtPredictorService
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
import uuid

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
thought_classification_service = ThoughtClassificationService(
    thoughts_dao,
    thoughts_predictor
)


# Note that this is a highly naive and error prone way to get/set the user ID for the purposes of the hackathon.
# It would be better to, for example, generate and sign an HTTP only JWT cookie encoded with the user ID.
@app.before_request
def get_user_id_from_cookie():
    user_id = request.cookies.get('user_id')

    if user_id is None:
        user_id = str(uuid.uuid4())

        @after_this_request
        def set_user_id_cookie(response):
            response.set_cookie('user_id', user_id)
            return response

    g.user_id = user_id


@app.route("/")
def hello():
    return {
        "status": "Your application is running"
    }


@app.route('/findRelatedThoughts', methods=['POST'])
def findRelatedThoughts():
    thought = request.json['thoughtText']
    user_id = g.user_id
    return thought_classification_service.classify_and_return_related_thoughts(user_id, thought)


if __name__ == '__main__':
    app.run(debug=True, port=port, host="0.0.0.0")
