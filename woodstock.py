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
    keywords = request.args.get('query', '').strip()
    if (' ' in keywords):
    	k0 = '%%%s%%'%keywords.split()[0]
    	k1 = '%%%s%%'%keywords.split()[1]
    	all = Employee.query.filter(Employee.first_name.ilike(k0) | Employee.pref_name.ilike(k0), Employee.last_name.ilike(k1)).all()
    else:
    	keyword = '%%%s%%'%keywords
    	all = Employee.query.filter(Employee.first_name.ilike(keyword) | Employee.last_name.ilike(keyword) | Employee.user_id.ilike(keyword)).all()
    return jsonify(suggestions=[e.serializeSuggestion() for e in all])

@app.route('/woodstock/api/search2')
def search2():
	keyword = request.args.get('query', '') 
	c = engine.connect()
	stmt = text("SELECT  id, pref_name, last_name, user_id, similarity('pref_name', :x)+similarity('last_name', :x) as sml FROM employees ORDER BY sml DESC LIMIT :y")
	# SELECT  pref_name, last_name, user_id, similarity(pref_name,'rob')+similarity(last_name,'rob') as sml  FROM employees ORDER BY sml DESC LIMIT 10
	qresult = c.execute(stmt, {"x": "%s"%keyword, "y": 20})

	result = []
	for row in qresult:
		t = {
		'data': row['id'],
		'value': "{0} {1}".format(row['pref_name'],row['last_name'])
		}
		result.append(t)
	print(result)
    
	c.close()
	return jsonify(query='unit',suggestions=result)



# Employee select endpoint
@app.route('/woodstock/api/list/<int:id>')
def employee(id):
    employee = Employee.query.filter(Employee.id==id).first()
    return jsonify(employee.card())
