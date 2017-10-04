# F-x-project
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


