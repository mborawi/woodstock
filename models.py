from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import Float, ForeignKey, DateTime, Boolean, PrimaryKeyConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship, aliased
from database import Base, db_session
from datetime import datetime



class Employee(Base):
	__tablename__ = 'employees'
	id = Column(Integer, primary_key=True)
	first_name = Column(String(25))
	pref_name = Column(String(25))
	last_name = Column(String(25))
	full_name = Column(String(51))
	user_id = Column(String(5), index = True)
	position_id = Column(Integer)
	job_title = Column(String(40))
	classification = Column(String(12))
	building = Column(String(10))
	manager_id = Column(Integer, index = True)
	manager_position_id = Column(Integer)
	email = Column( String(60) )
	phone = Column( String(15) )
	floor = Column( String(3) )
	workpoint = Column ( String(15) )
	bsl = Column( String(12) )
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)
	deleted_at = Column(DateTime, index = True)
	metrics = relationship("Metric", backref = "employees", order_by="Metric.topic_id")

	def __init__(self, \
				id=None,\
				first_name=None,\
				pref_name=None,\
				last_name=None,\
				full_name=None,\
				user_id=None,\
				position_id=None,\
				job_title=None,\
				classification=None,\
				building=None,\
				manager_id=None,\
				manager_position_id=None,\
				email = None,\
				phone = None,\
				floor = None,\
				workpoint = None,\
				bsl = None\
				):

		self.id = id
		self.first_name = first_name
		self.pref_name = pref_name
		self.last_name = last_name
		self.full_name = full_name
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

	def __repr__(self):
		return "Employee [ name='%s %s', userId='%s' ]" % (self.first_name, self.last_name, self.user_id )
	
	def __str__(self):
		 return self.first_name + " " + self.last_name + ": " + self.job_title

	def serializeSuggestion(self):
		return {
			'data': self.id,
			'value': "{0} {1}, {2}".format(self.pref_name,self.last_name,self.user_id)
		}

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

	def serialize(self):
		return {
			'employee': {
				'id': 			self.id,
				'name': 		"{0} {1}".format(self.pref_name,self.last_name).title(),
				'userid': 		self.user_id,
				'position': 	self.position_id,
				'title': 		self.job_title,
				'class': 		self.classification,
				'building': 	self.building,
				'email': 		self.email,
				'phone': 		self.phone,
				'floor': 		self.floor,
				'workpoint': 	self.workpoint,
				'bsl': 			self.bsl,
			},
		}

association_table = Table('metric_groups', Base.metadata,
    Column('metric_id', Integer, ForeignKey('metrics.id'), nullable=False),
    Column('group_id', Integer, ForeignKey('groups.id'), nullable=False),
    PrimaryKeyConstraint('metric_id', 'group_id')
)


class Metric(Base):
	__tablename__ = 'metrics'
	id = Column(Integer, primary_key = True)
	num_val = Column(Float)
	str_val = Column(String(50))
	string_format = Column(Boolean, default = False)
	employee_id = Column(Integer, ForeignKey('employees.id'), index = True)
	topic_id = Column(Integer, ForeignKey('topics.id'), index = True)
	topic = relationship("Topic")
	type_id = Column(Integer, ForeignKey('types.id'), index = True)
	Type = relationship("Type")
	division_id = Column(Integer, ForeignKey('divisions.id'), index = True)
	division = relationship("Division")
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)
	deleted_at = Column(DateTime, index = True)
	groups = relationship("Group",
		secondary=association_table,
		backref='group_metrics'
		)

	def __repr__(self):
		Val = self.str_val if self.string_format else self.num_val
		m = "Topic: {0}, {1}, Unit {3}, {3}\n".format(self.Topic.name, self.Division.name, self.Type.name, Val)
		# m = "Topic: {0}, {1}\n".format(self.Topic.Name, Val)
		return m
	def serialize(self, CodeCache):
		Val = self.str_val if self.string_format else self.num_val
		key = "{0}:{1}".format(self.TopicId, self.DivisionId)
		entry = CodeCache[key]
		code = entry["Code"]
		return {
			'c':code,
			'v' : Val,
		}


class Group(Base):
	__tablename__ = 'groups'
	id = Column(Integer, primary_key=True)
	name = Column(String(40))
	desc = Column(String(100))
	order = Column(Integer)
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)
	deleted_at = Column(DateTime)
	metrics = relationship("Metric",
		secondary=association_table,
		backref='metric_groups'
		)

	def __repr__(self):
		return "[Group (id = '%d',name='%s') ]" %\
		 (self.id, self.name)

	def serialize(self):
		return {
			'name': 	self.name,
			'order':	self.order,
		}

class Topic(Base):
	__tablename__ = 'topics'
	id = Column(Integer, primary_key=True)
	order = Column(Integer)
	name = Column(String(100))
	desc = Column(String(1000))
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)
	deleted_at = Column(DateTime)
	def __repr__(self):
		return "< Topic (id = '%d',name='%s', Description='%s'>" %\
		 (self.id, self.name, self.desc)

class Type(Base):
	__tablename__ = 'types'
	id = Column(Integer, primary_key=True)
	name = Column(String(40))
	desc = Column(String(200))
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)
	deleted_at = Column(DateTime)
	def __repr__(self):
		return "< Type (id = '%d',name='%s', Description='%s'>" %\
		 (self.id, self.name, self.desc)

class Division(Base):
	__tablename__ = 'divisions'
	id = Column(Integer, primary_key=True)
	name = Column(String(40))
	desc = Column(String(200))
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)
	deleted_at = Column(DateTime)

	def __repr__(self):
		return "< Division(id = '%d',name='%s', Description='%s'>" %\
		 (self.id, self.name, self.desc)

class Activity(Base):
	__tablename__ = 'activities'
	id = Column(Integer, primary_key=True)
	refresh_time = Column(DateTime, default=datetime.now)
	data_time  = Column(DateTime)
	records_no = Column(Integer)
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now)
	deleted_at = Column(DateTime)

	def __init__(self,data_time, records_no, refresh_time=datetime.now):
		self.refresh_time = refresh_time
		self.data_time = data_time
		self.records_no = records_no

	def serialize(self):
		return {
			'refresh_date':self.refresh_time,
			'update_date':self.data_time,
			'records':self.records_no
		}
	def __repr__(self):
		return "<activity: refreshed: '%s', snapshotted: '%s', records: '%d'>"%\
		(self.refresh_time, self.data_time, self.records_no) 
	
	def __str__(self):
		return self.__repr__()

	
