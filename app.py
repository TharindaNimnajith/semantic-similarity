import json

from flask import Flask, request, jsonify
from flask_swagger import swagger

app = Flask(__name__)


@app.route('/spec')
def spec():
    return jsonify(swagger(app))


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
