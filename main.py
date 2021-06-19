from flask import Flask, request
import os
import thought_classifier
import db
import predictor

app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'thoughtbubbles.sqlite')
)
db.init_app(app)
port = (os.environ.get("PORT", 80))

predictor.init_predictor()

@app.route("/")
def hello():
    return {
        "status" : "Your application is running"
    }

@app.route('/findRelatedThoughts', methods=['POST'])
def findRelatedThoughts():
    content = request.json
    thought = content['thoughtText']
    return thought_classifier.classify_and_return_related_thoughts(thought)

if __name__ == '__main__':
    app.run(debug=True, port=port, host="0.0.0.0")
