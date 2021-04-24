import json
from flask import Flask, jsonify
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='TodoMVC API', description='A simple TodoMVC API')

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, _id):
        for todo in self.todos:
            if todo['id'] == _id:
                return todo
        api.abort(404, f'Todo {_id} does not exist')

    # def create(self, data):
    #     todo = data
    #     todo['id'] = self.counter = self.counter + 1
    #     self.todos.append(todo)
    #     return todo

    def evaluate_answer(self, data):
        info = json.loads(data)
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

    def update(self, _id, data):
        todo = self.get(_id)
        todo.update(data)
        return todo


    def delete(self, _id):
        todo = self.get(_id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        """List all tasks"""
        return DAO.todos

    # @ns.doc('create_todo')
    # @ns.expect(todo)
    # @ns.marshal_with(todo, code=201)
    # def post(self):
    #     """Create a new task"""
    #     return DAO.create(api.payload), 201

    @ns.doc('evaluate_answer')
    @ns.expect(model_answer, student_answer)
    @ns.marshal_with(model_answer, student_answer, code=201)
    def post(self):
        """Evaluate answer"""
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    """Show a single todo item and lets you delete them"""

    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, _id):
        """Fetch a given resource"""
        return DAO.get(_id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, _id):
        """Delete a task given its identifier"""
        DAO.delete(_id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, _id):
        """Update a task given its identifier"""
        return DAO.update(_id, api.payload)


# @app.route('/similarity', methods=['POST'])
# def calc_score():
#     info = json.loads(request.data)
#     model_answer = info.get('model_answer', '')
#     student_answer = info.get('student_answer', '')
#     return jsonify({
#         'status': 200,
#         'data': {
#             'model_answer': model_answer,
#             'student_answer': student_answer,
#             'spelling': 9.0,
#             'grammar': 7.0,
#             'relatedness': 8.0,
#             'overall': 8.0
#         }
#     })


if __name__ == '__main__':
    app.run(debug=True)
