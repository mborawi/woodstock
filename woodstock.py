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
    all = Employee.query.filter(Employee.first_name.ilike(keyword) | Employee.last_name.ilike(keyword)).all()    
    return jsonify(query="unit",suggestions=[e.serializeSuggestion() for e in all])

@app.route('/woodstock/api/search2', methods=['POST'])
def search2():
	c = engine.connect()
	keyword = request.args.get('query', '') 
	stmt = text("SELECT  id, pref_name, last_name, user_id, similarity(pref_name, :x)+similarity(last_name, :x) as sml FROM employees ORDER BY sml DESC LIMIT :y")
	# SELECT  pref_name, last_name, user_id, similarity(pref_name,'rob')+similarity(last_name,'rob') as sml  FROM employees ORDER BY sml DESC LIMIT 10
	qresult = c.execute(stmt, {"x": keyword, "y": 20})

	result = []
	for row in qresult:
		t = {
		'data': row['id'],
		'value': "{0} {1}".format(row['pref_name'],row['last_name'])
		}
		result.append(t)
	print(result)
    
	c.close()
	return jsonify(query="unit",suggestions=result)



# Employee select endpoint
@app.route('/woodstock/api/list/<int:id>')
def employee(id):
    employee = Employee.query.filter(Employee.id==id).first()
    return jsonify(employee.card())
