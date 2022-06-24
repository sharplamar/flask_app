from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# create an instance of flask
app = Flask(__name__)
# creating an API object
api = Api(app)
# creating database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///emp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# sqlalchemy_mapper
db = SQLAlchemy(app)

# add a class
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float)

    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.gender} - {self.salary}"

# for GET request to http://localhost:5000/
class GetEmployee(Resource):
    def get(self):
        employees = Employee.query.all()
        emp_list = []
        for emp in employees:
            emp_data = {'id': emp.id, 'FirstName': emp.firstname, 'LastName': emp.lastname, 'Gender': emp.gender,
                        'salary': emp.salary}
            emp_list.append(emp_data)
        return {"Employees": emp_list}, 200

# For post request to http://localhost:5000/employee
class AddEmployee(Resource):
    def post(self):
        if request.is_json:
            emp = Employee(firstname=request.json['Firstname'], lastname=request.json['LastName'],
                           gender=request.json['Gender'], salary=request.json['salary'])
            db.session.add(emp)
            db.session.commit()
            # return a json response
            return make_response(jsonify({'id': emp.id, 'First Name': emp.firstname, 'Last Name': emp.lastname,
                                          'Gender': emp.gender, 'Salary': emp.salary}), 201)
        else:
            return {'error': 'request must ne JSON'}, 400

# For put request to http://localhost:5000/update/?
class UpdateEmployee(Resource):
    def put(self, id):
        if request.is_json:
            emp = Employee.querry.get(id)
            if emp is None:
                return {'error': 'not found'}, 404
            else:
                emp.firstname = request.json['FirstName']
                emp.lastname = request.json['LastName']
                emp.gender = request.json['Gender']
                emp.salary = request.json['Salary']
                db.session.commit()
                return 'updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400

# For delete request to http://localhost:5000/delete/?
class DeleteEmployee(Resource):
    def delete(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'error': 'not found'}, 404
        db.session.delete(emp)
        db.session.commit()
        return f'{id} id deleted', 200

api.add_resource(GetEmployee, '/')
api.add_resource(GetEmployee, '/add')
api.add_resource(GetEmployee, '/update/<int:id>')
api.add_resource(DeleteEmployee, '/delete/<int:id>')

#
if __name__ == '__main__':
    app.run(debug=True)

if_name_ == '_main_'