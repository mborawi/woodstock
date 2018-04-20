# RoadMap

## Backend
### Build ORM
* [mborawi] Build the rest of the models reflecting the tables in proton, and relationships between them.
* [mborawi] Generate fake data to reflect metrics etc

### Build The following Endpoints:
* [gpra8449] Search for Employees
	* HTTP POST: /woodstock/api/search payload: query="text supplied"
	* RETURNS: an array of json objects [{first_name:x, last_name:y, userId:z}, ...]
	* given a query as input
	* If less than 3 dont search, return error of less than 3
	* If not found return not found
	* Search several columns, first name, last name, AGS, User_ID etc
	* Could use fuzzy searching, postgres has simialr function that could work
	* return a Json array of names sorted and ordered (order by name, or maybe similarity)
	* this list will show up as suggestions for user to choose from, should return the fields that will be used to build those suggestions plus user ids.
* [Trentham3269] List an employee
	* HTTP GET: /woodstock/api/list/:id
	* Returns Json Object: {first_name:x, last_name:y, floor:z, email: d, other business card info}
	* Given a user id, return information about employee that would show like a business card.
	* This endpoint and next are tied together. (build together?)
	* Add id to session (Basket)
* [Trentham3269] List Metrics
	* HTTP GET: /woodstock/api/metrics/:id
	* given a user id return metrics
* Export Metrics
	* HTTP POST: /woodstock/api/export payload: ids=[id1,id2], metricGroups=[mg_id1,mg_id2,..]
	* Given a list of ids of employees, build an xlxs file and return it.
	* List of ids will be taken from session (Basket)
* List Employees
	* HTTP GET: /woodstock/api/basket/
	* Return array of json objects [{first_name:x, last_name:y, Job Title:z, ...}]
	* Find employee ids from session and return names
* Remove Employee
	* HTTP GET: /woodstock/api/basket/remove/:id
	* return success or failure
	* Given an id remove them from session list (Basket)
* Login
	* HTTP POST: /woodstock/api/login payload: username="", password=""
	* builds cookie and returns {username, usedid}
	* Given a userId, and password, authenticate with Goth, create a user session if success
* Logout
	* HTTP GET: /woodstock/api/logout	
	* return success or failure
	* Clear Session


## Frontend
### To be decided by team.
### AngularJs, JQuery, ReactJs, Or VueJs in alphabetical order 
