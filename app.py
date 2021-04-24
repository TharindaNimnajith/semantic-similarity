import json

from flask import Flask, request, jsonify

app = Flask(__name__)


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


app.run(host='0.0.0.0', port=81, debug=True)
