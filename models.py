from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import Float, ForeignKey, DateTime, Boolean, PrimaryKeyConstraint
from sqlalchemy.dialects import postgresql
from datetime  import datetime
from database import Base, db_session


class Employee(Base):
	__tablename__ = 'employees'
	id = Column(Integer, primary_key = True )
	first_name = Column(String(25))
	pref_name = Column(String(25))
	last_name = Column(String(25))
	user_id = Column(String(5), index = True)
	position_id = Column(Integer)
	job_title = Column(String(40))
	classification = Column(String(12))
	building = Column(String(10))
	manager_id = Column( Integer, index = True)
	manager_position_id = Column(Integer)
	email = Column( String(60) )
	phone = Column ( String(15))
	floor = Column ( String(3))
	workpoint = Column( String(15))
	bsl = Column( String(12) )
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)
	deleted_at = Column(DateTime, index = True)


	def __init__(self, \
		id=None,\
		first_name = None,\
		pref_name  = None,\
		last_name  = None,\
		user_id = None,\
		position_id = None,\
		job_title = None,\
		classification = None,\
		building = None,\
		manager_id = None,\
		manager_position_id = None,\
		email = None,\
		phone = None,\
		floor = None,\
		workpoint = None,\
		bsl = None):

		self.id = id
		self.first_name = first_name
		self.pref_name = pref_name
		self.last_name = last_name
		self.user_id = user_id
		self.position_id = position_id
		self.job_title = job_title
		self.classification = classification
		self.building = building
		self.manager_id = manager_id
		self.manager_position_id = manager_position_id
		self.email = email
		self.phone = phone
		self.floor = floor
		self.workpoint = workpoint
		self.bsl = bsl

	def __str__(self):
		 return self.first_name + " " + self.last_name + ": " + self.job_title

	def card(self):
	    return {
	        'id': self.id,
	        'pref_name': self.pref_name,
	        'last_name': self.last_name,
	        'name':"{0} {1}".format(self.pref_name, self.last_name),
	        'job_title': self.job_title,
	        'email': self.email,
	        'phone': self.phone,
	        'building': self.building,
	        'floor': self.floor,
	        'workpoint': self.workpoint 
	    }
