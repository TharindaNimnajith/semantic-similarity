import json

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Semantic Similarity API',
          description='Semantic Similarity API By Tharinda',
          )

ns = api.namespace('semantic_similarity', description='Answer operations')

answer = api.model('Answer', {
    'model_answer': fields.String(required=True, description='The task unique identifier'),
    'student_answer': fields.String(required=True, description='The task details')
})


@ns.route('/')
class Semantic(Resource):
    @ns.doc('evaluate_answer')
    @ns.expect(answer)
    def post(self):
        return calc_score()


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


#
# app.run()


if __name__ == '__main__':
    app.run(debug=True)
