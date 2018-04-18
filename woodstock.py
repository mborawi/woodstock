from flask import Flask, render_template,send_from_directory, session
from flask import request
from flask import jsonify
from models import Employee

app = Flask(__name__)

@app.route('/api/woodstock/list/<int:id>')
def employee(id):
	employee = Employee.query.filter(Employee.id==id).first()
	return jsonify(employee.serialize())