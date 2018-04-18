from database import db_session, Base, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from datetime import datetime

from models import Employee

from faker import Faker
import random



fake = Faker()

def generateEmps(N):
	for i in range(1, N+1):
		r = random.randint(0,i)
		fn = fake.first_name()
		p = Employee(first_name = fn,\
			pref_name  = fn,\
			last_name  = fake.last_name(),\
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

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
generateEmps(100)



