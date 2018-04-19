# RoadMap

## Backend
### Build The following Endpoints:
* Search for Employees
	* given a query as input
	* If less than 3 dont search, return error of less than 3
	* If not found return not found
	* Search several columns, first name, last name, AGS, User_ID etc
	* Could use fuzzy searching, postgres has simialr function that could work
	* return a Json array of names sorted and ordered (order by name, or maybe similarity)
	* this list will show up as suggestions for user to choose from, should return the fields that will be used to build those suggestions plus user ids.
* List an employee
	* Given a user id, return information about employee that would show like a business card.
	* This endpoint and next are tied together. (build together?)
	* Add id to session (Basket)
* List Metrics
	* given a user id return metrics
* Export Metrics
	* Given a list of ids of employees, build an xlxs file and return it.
	* List of ids will be taken from session (Basket)
* List Employees
	* Find employee ids from session and return names
* Remove Employee
	* Given an id remove them from session list (Basket)
* Login
	* Given a userId, and password, authenticate with Goth, create a user session if success
* Logout
	* Clear Session


## Frontend
### To be decided by team.
### AngularJs, JQuery, ReactJs, Or VueJs in alphabetical order 