from database import db_session, Base, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from datetime import datetime
import csv

from models import *

from faker import Faker
import random

def createDivisions():
	divDict = {\
				'SELF':'Individual Details',\
				'CHOC': 'Chain of command (direct reports)',\
				'SPOC': 'Span of Control (all subordinates)',\
			}
	divs = {}
	try: 
		for k in divDict:
			div = Division(name=k, desc=divDict[k])
			db_session.add(div)
			db_session.flush()
			divs[k] = div
		db_session.commit()
	except Exception as e:
		print(e)
		db_session.rollback()
	return divs

def createTypes():
	typs = {}
	names = ['Category', 'Count', 'Indicator', 'Mean', 'Mode', 'Percent', 'Rate', 'Sum','Permillage']
	# names = ['Average', 'Rate', 'Mode', 'Sum', 'Benchmark', 'Count', 'Rate per 1k']
	try: 
		for nm in names:
			typ = Type( name = nm)
			db_session.add(typ)
			db_session.flush()
			typs[nm] = typ
		db_session.commit()
	except Exception as e:
		print(e)
		db_session.rollback()
	return typs

def createGroups():
	grps = {}
	names = ['Team Information',
			'Flexible Arrangements',
			'Leave',
			'Career Progression',
			'People & Health',
			'Training',
			'Diversity']
	try: 
		for idx, nm in enumerate(names):
			grp = Group( name = nm, order = ( idx + 1 ) )
			db_session.add(grp)
			db_session.flush()
			grps[nm] = grp
		db_session.commit()
	except Exception as e:
		print(e)
		db_session.rollback()
	return grps

def createTopics():
	tpcs= {}
	try:
		# too many topics to be written here
		with open('data/topics.csv') as csvfile:
			rdr = csv.reader(csvfile)
			for row in rdr:
				tpc = Topic(order = row[0], name = row[1], desc = row[2])
				db_session.add(tpc)
				db_session.flush()
				tpcs[row[0]]= tpc
			db_session.commit()
	except Exception as e:
		print(e)
		db_session.rollback()
	return tpcs


def generateEmps(N):
	
	for i in range(1, N+1):
		r = random.randint(0,i)
		fn = fake.first_name()
		ln = fake.last_name()
		p = Employee(first_name = fn,\
			pref_name  = fn,\
			last_name  = ln,\
			full_name = fn + " " + ln,\
			user_id = "u" + fake.sha1()[0:4],\
			position_id = i,\
			job_title = fake.job()[0:40],\
			classification = random.randint(1,13),\
			building = random.randint(1,25),\
			email = fake.email(),\
			phone = fake.numerify(text="#####"),\
			floor = random.randint(1,8),\
			workpoint = random.randint(1,150),\
			manager_id = 0 if i==1 else random.randint(1,i),\
			bsl = random.randint(1,20))
		print("adding: ", p , " to db")
		db_session.add(p)

	db_session.commit()

def generateEmployeeAndMetrics(N, topics, groups, divisions, types):
	fake = Faker()
	metricsFile =  open('data/metrics.csv')
	mtrcFilelst = list(csv.DictReader(metricsFile, delimiter=','))
	for i in range(1, N+1):
		r = random.randint(0,i)
		fn = fake.first_name()
		ln = fake.first_name()
		emp = Employee(first_name = fn,\
			pref_name  = fn,\
			last_name  = ln,\
			full_name = fn + " " + ln,\
			user_id = "u" + fake.sha1()[0:4],\
			position_id = i,\
			job_title = fake.job()[0:40],\
			classification = random.randint(1,13),\
			building = random.randint(1,25),\
			email = fake.email(),\
			phone = fake.numerify(text="#####"),\
			floor = random.randint(1,8),\
			workpoint = random.randint(1,150),\
			manager_id = 0 if i==1 else random.randint(1,i),\
			bsl = random.randint(1,20))

		mets = []
		for line in mtrcFilelst:
			m = Metric(
				topic=topics[ line['Order'] ],
				division = divisions[ line['Division'] ],
				Type = types[ line['Type'] ],
				groups = [ groups[ line['Groups'] ] ]
				)
			if line['StrFormat'] == 'N':
				m.num_val = random.randint(0,100)
				m.string_format = False
			else:
				m.str_val = fake.month_name()
				m.string_format = True
			mets.append(m)
		emp.metrics = mets
		print("adding: ", emp , " to db")
		db_session.add(emp)
	db_session.commit()

if __name__ == "__main__":

	# drop all the table existing in the db with all data in them.
	Base.metadata.drop_all(bind=engine)

	# create new empty tables as per models.py defintions. 
	Base.metadata.create_all(bind=engine)

	# populate divisions
	ds = createDivisions()

	# populate types
	ts = createTypes()
	gs = createGroups()
	tps = createTopics()

	# populate employees with random staff and metrics
	generateEmployeeAndMetrics(N=100, topics=tps, groups=gs, divisions=ds, types=ts) 

	try:
		# ensure simialrity extension is enabled to do fuzzy word searches
		res = engine.execute("CREATE EXTENSION pg_trgm CASCADE")
		res = engine.execute("SELECT set_limit(0.5)")
	except Exception as e:
		print(e)




