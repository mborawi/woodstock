from flask import Flask, render_template,send_from_directory, session
from flask import request
from flask import jsonify
from models import Employee
from database import engine
from sqlalchemy.sql import text

app = Flask(__name__)

# Employee search endpoint
@app.route('/woodstock/api/search')
def search():
    keyword = "%%%s%%"%request.args.get('query', '')    
    all = Employee.query.filter(Employee.first_name.like(keyword) | Employee.last_name.like(keyword)).all()    
    return jsonify(query="unit",suggestions=[e.serializeSuggestion() for e in all])

@app.route('/woodstock/api/search2')
def search2():
	keyword = request.args.get('query', '') 
	c = engine.connect()
	stmt = text("SELECT  id, full_name, user_id, similarity(full_name, :x) as sml FROM employees ORDER BY sml DESC LIMIT :y")
	qresult = c.execute(stmt, {"x": "%s"%keyword, "y": 20})

	result = []
	for row in qresult:
		t = {
		'data': row['id'],
		'value': row['full_name']
		}
		result.append(t)
    
	c.close()
	return jsonify(suggestions=result)



# Employee select endpoint
@app.route('/woodstock/api/list/<int:id>')
def employee(id):
    employee = Employee.query.filter(Employee.id==id).first()
    return jsonify(employee.card())
