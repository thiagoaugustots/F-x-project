"""
Started with an existing project that uses Flask with sqlite to do simple get operations with public data
[https://impythonist.wordpress.com/2015/07/12/build-an-api-under-30-lines-of-code-with-python-and-flask/]

Read the tutorial to understand the concepts and made the application work first in the given form

Made a duplicate file and changed each item to correspond for example added dependencies for pymongo
and the mongo client connection

Because doing numeric operations on the data, first had to clean data to change the Salary field to be
numeric not strings. (Generally, numbers should be saved as numbers not strings)
Use regex find/replace to clean out "$" symbol and " for example: "$50,000.00" to 50,000.00 (searched for
similar regex and modified)

Imported the data using mongoimport
Import command:
mongoimport --db salaries --type csv --headerline --file employee_chicago_salaries.csv

First implemented the simple case:
    list all the departments
Then implemented more complex cases:
    Show average salary of each department
    Show average salary of -specific- department
    Tax a given employee by given tax rate (employee names found in CSV file)

The program uses GET, POST, and PUT

Assumptions:
1) We exclude all generated IDs with {"_id": False} to make the view better
2) There is no error checking; we assume the person is giving the right types
3) Most Importantly -- With more training and apprenticeship, I can certainly make this better and
    learn many other tasks!!

"""

from flask import Flask, request, json
from flask_restful import Resource, Api
from pymongo import MongoClient

# Create client for connecting to mongo db
client = MongoClient()

app = Flask(__name__)
api = Api(app)


# should return a list of all the departments
class Departments_Meta(Resource):
    def get(self):
        # Connect to mongo database
        db = client['salaries']
        collection = db['employee_chicago_salaries']
        # Use mongo "distinct" function to get list of all the departments
        return list(collection.distinct("Department"))


class Departmental_Salary_Average(Resource):
    def get(self):
        db = client['salaries']
        collection = db['employee_chicago_salaries']
        # perform an aggregation to get the average salary of every department using GET
        return list(collection.aggregate([ {"$group":{"_id": "$Department", "Average Salary": { "$avg": '$Salary'}}}]))

    def post(self):
        db = client['salaries']
        collection = db['employee_chicago_salaries']
        department = json.loads(request.data)['Department']
        # perform an aggregation to get the average salary BY department using POST
        return list(collection.aggregate([{"$match": {"Department": department}}, {
            "$group": {"_id": "$Department", "Average Salary": {"$avg": "$Salary"}}}]))


class Tax_Worker(Resource):
    def put(self):
        db = client['salaries']
        collection = db['employee_chicago_salaries']
        request_data = json.loads(request.data)
        person_to_tax = request_data['Employee']
        tax_rate = float(request_data['Tax Rate'])

        # We are going to set the tax based on the data request
        return list(collection.aggregate([
            { "$project": {"_id": False}},
            {"$match":{"Name": person_to_tax}},
            {"$addFields":
                {
                    "Taxes Owed": {"$multiply":  [ "$Salary", tax_rate]}
                }
            }
        ]))


# GET shows list of all the departments
api.add_resource(Departments_Meta, '/departments')

# GET shows the salary average for each department
# POST {"Department" : "Department Name"} shows average for specific department
api.add_resource(Departmental_Salary_Average, '/dept_avg')

# PUT charge a tax on users. Simple case of retrieve, modify and insert.
api.add_resource(Tax_Worker, '/tax_employee')


if __name__ == '__main__':
    app.run(debug=True)
