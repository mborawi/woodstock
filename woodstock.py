from flask import Flask, render_template,send_from_directory, session
from flask import request
from flask import jsonify
from models import Employee
from database import engine
from sqlalchemy.sql import text
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'mySessionSecret'

@app.route('/')
@app.route('/woodstock')
@app.route('/woodstock/')
def index():
	return send_from_directory(directory='static', filename='index.html')

# Employee search endpoint
@app.route('/woodstock/api/search')
def search():
    keyword = "%%%s%%"%request.args.get('query', '')    
    all = Employee.query.filter(Employee.first_name.like(keyword) | Employee.last_name.like(keyword)).all()    
    return jsonify(query="unit",suggestions=[e.serializeSuggestion() for e in all])

@app.route('/woodstock/api/search2')
def search2():
	# if 'username' not in session:
	if False:
		return jsonify(username=None,suggestions=None)

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


@app.route('/woodstock/api/login', methods=['POST'])
def login():
	content = request.json
	username = content['username']
	password = content['password']
	if username == "uc123":
		session['username'] = username
		session['loginTime'] = datetime.now()
		print(username,":::::::::::",session)
		return jsonify({"verified":True})
	else:
		return jsonify({"verified":False})
	return username

@app.route('/woodstock/api/logout')
def logout():
	session.pop('username', None)
	session.pop('loginTime', None)
	return jsonify({"verified":False})
