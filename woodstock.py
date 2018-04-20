from flask import Flask, render_template,send_from_directory, session
from flask import request
from flask import jsonify
from models import Employee

app = Flask(__name__)

# Employee search endpoint
@app.route('/woodstock/api/search')
def search():
    keyword = "%%%s%%"%request.args.get('query', '')    
    all = Employee.query.filter(Employee.first_name.like(keyword) | Employee.last_name.like(keyword)).all()    
    return jsonify(query="unit",suggestions=[e.serializeSuggestion() for e in all])

# Employee select endpoint
@app.route('/woodstock/api/list/<int:id>')
def employee(id):
    employee = Employee.query.filter(Employee.id==id).first()
    return jsonify(employee.card())
