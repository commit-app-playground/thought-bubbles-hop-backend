from flask import Flask, request
import os
import thought_classifier
import db
import predictor
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
    predictor.init_predictor()

port = (os.environ.get("PORT", 80))


@app.route("/")
def hello():
    return {
        "status": "Your application is running"
    }


@app.route('/findRelatedThoughts', methods=['POST'])
def findRelatedThoughts():
    thought = request.json['thoughtText']
    return thought_classifier.classify_and_return_related_thoughts(thought)


if __name__ == '__main__':
    app.run(debug=True, port=port, host="0.0.0.0")
