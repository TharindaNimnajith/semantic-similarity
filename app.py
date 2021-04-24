import json

from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app-name': 'semantic-similarity-flask'})


@app.route('/', methods=['POST'])
def calc_score():
    info = json.loads(request.data)
    model_answer = info.get('model_answer', '')
    student_answer = info.get('student_answer', '')
    return jsonify({
        'status': 200,
        'data': {
            'model_answer': model_answer,
            'student_answer': student_answer,
            'spelling': 9.0,
            'grammar': 7.0,
            'relatedness': 8.0,
            'overall': 8.0
        }
    })


app.run()
