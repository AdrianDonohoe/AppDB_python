## Created by Adrian Donohoe 27/04/2020
# https://github.com/AdrianDonohoe/AppDB_python
import pymysql
import pandas as pd
import pymongo


conn = None  # Connection variable for MySQL
myclient = None # Connection variable for Mongo
df = pd.DataFrame() # Make empty DF, for storing DB query for menu 4 and 5.

# Main function
def main():

	display_menu() # Display the menu

	while True: #  keeps the menu displayed until x is entered
		choice = input("Choice: ") # query the user for their menu choice
		''' a bunch of if/elif statements which wiil run based on the users input. 
		Each one calls a diferent function
		'''
		if (choice == "1"):
			viewPeople()
			display_menu()
		elif (choice == "2"):
			getCountryByInYr()
			display_menu()
		elif (choice == "3"):
			addPerson()
			display_menu()
		elif (choice == "4"):
			getCountryByName()
			display_menu()
		elif (choice == "5"):
			getCountryByPop()
			display_menu()
		elif (choice == "6"):
			findStudentByAddress()
			display_menu()
		elif (choice == "7"):
			addNewCourse()
			display_menu()
		elif (choice == "x"):
			try:
				conn.close() # close the MySQL connection before exiting
				myclient.close() # close the Mongo connection
			except AttributeError:
				pass
			break;  # breaks out of the menu while loop, to exit the program
		else: # If anything other than required choices are made, display the menu again
			display_menu()
			

## Function to get people from mysql db and display 2 at a time			
def viewPeople():
    people = getPeopleDB() # Call the function to connect/read the DB and store result in people variable
    
    answer = '' # Used to hold answer to thje quit question 
    for i in range(0,len(people),2): # loop over the returned people table, in steps of 2
        print(people[i]['personID'],'|',people[i]['personname'],'|',people[i]['age']) # print 1 line
        try: # necessary to put this in a try block, so that we can print a table with odd rows without crashing
            print(people[i+1]['personID'],'|',people[i+1]['personname'],'|',people[i+1]['age']) # prints the 2nd line
        except: # will fail for odd numbered table
            pass # so we can just pass here
        answer = input('-- Quit (q) --') # Ask if user wants to quit
        if answer == 'q' or answer == 'Q': # quit if q or Q entered
            break # and break the for loop to exit function
        
## Function to get Country by Independence Year from mysql db
def getCountryByInYr():
    year = input('Enter Year : ') # Ask user to enter the year
    countries = getCountryByInYrDB(year) # Call the DB function with year and assign to countries variable

    for country in countries: # loop over the countries and print name, continent and Independence Year
        print(country['Name'],'|',country['Continent'],'|',country['IndepYear'])
             

## Function to add a new person to the DB
def addPerson():
    print('Add New Person')
    print('-' * 14)
    name = input('Name : ') # get the name
    age = input('Age : ') # get the age
    addPersonDB(name,age) # call  the DB function with name and age to be added

## Function to get Country by Name. Fetch all data once and store
def getCountryByName():
	global df # data will be stored in global Dataframe
	if df.empty: # if the DF is empty, fetch the data
		df = getCountryDB() # call the function to get the data and assign to the global DF
	
	print('')
	print('Countries by Name')
	print('-' * 17)
	sub = input('Enter Country Name : ') # the the string from the user to be searched
	# Search for the substring in the Name column, the location of the substring is put in the Found column. -1, if not found.
	df['Found'] = df['Name'].str.find(sub) # Adapted from https://www.geeksforgeeks.org/python-pandas-series-str-find/
	found = df.loc[df.loc[:,'Found'] != -1 ] # assign all rows where substring is found to found DF
	for index, row in found.iterrows(): # iterate over the rows and print Name, continent, population and head of state.
		print(row['Name'],' | ',row['Continent'],' | ',row['Population'],' | ',row['HeadOfState']) # The project spec doesnt specifically say what to print here, but this is what the example uses.

## Function to get Countries by Population	
def getCountryByPop():
	global df # data will be stored in global Dataframe
	if df.empty: # if the DF is empty, fetch the data
		df = getCountryDB() # call the function to get the data and assign to the global DF
	
	print('')
	print('Countries by Pop')
	print('-' * 16)
	operator = input('Enter < > or = : ') # get the operator for the query
	## This block will run until a valid number is put in
	while True:  # Adapted from https://docs.python.org/3/tutorial/errors.html
		try:
			pop = int(input('Enter population : ')) # convert the requested number from string to int
			break # break the while loop if number is input
		except ValueError: # Catch the invalid number
			print("Oops!  That was no valid number.  Try again...")
	# This block gets the answer from the DF
	if operator == '<': # if less than
		found = df.loc[df.loc[:,'Population'] < pop ] # get the data where population < pop
		for index, row in found.iterrows(): # iterate over the rows and print Code, Name, Continent and population
			print(row['Code'],' | ',row['Name'],' | ', row['Continent'],' | ',row['Population'])
	elif operator == '>': # if greater than
		found = df.loc[df.loc[:,'Population'] > pop ] # get the data where population > pop
		for index, row in found.iterrows(): # iterate over the rows and print Code, Name, Continent and population
			print(row['Code'],' | ',row['Name'],' | ', row['Continent'],' | ',row['Population'])
	elif operator == '=': # if equal to
		found = df.loc[df.loc[:,'Population'] == pop ] # get the data where population equal to pop
		for index, row in found.iterrows(): # iterate over the rows and print Code, Name, Continent and population
			print(row['Code'],' | ',row['Name'],' | ', row['Continent'],' | ',row['Population'])
	else:
		pass # exit if no operator given

## Function to get Student by Address
def findStudentByAddress():
	print('')
	print('Find Students by Address')
	print('-' * 24)
	address = input('Enter Address : ') # get the users input, the address to find
	findStudentByAddressDB(address) # call the DB function

## Function to add a new course
def addNewCourse():
	print('')
	print('Add New Course')
	print('-' * 14)
	iD = input('_id : ') # get the MongoDB _id from user
	name = input('Name : ') # get the Course Name from user
	level = input('Level : ') # get the course level
	addNewCourseDB(iD,name,level) # call the DB function

## Function to display the main menu
def display_menu():
    print('\n')
    print('World DB')
    print('-' * 7)
    print('')
    print('MENU')
    print('=' * 4)
    print("1 - View People")
    print("2 - View Countries by Independence Year")
    print("3 - Add New Person")
    print("4 - View Countries by name")
    print("5 - View Countries by population")
    print("6 - Find Students by Address")
    print("7 - Add New Course")
    print("x - Exit application")



# MySQL connect function
def connect():
    global conn # using the global conn variable
    conn = pymysql.connect(host="localhost",user="root",password="", db="world",cursorclass=pymysql.cursors.DictCursor) # Defines the db connection details

# MongoDB connect function    
def mongo_connect():
    global myclient # using the global myclient variable
    myclient = pymongo.MongoClient() # use mongo client
    myclient.admin.command('ismaster')

# DB Functin to get people from the DB
def getPeopleDB():
    if (not conn): # check if not connected
        connect() # then connect if not connected already
    else:
        pass # was using this block for debugging connection. Just left it in with a pass

    
    query = "SELECT * FROM person" # the query to be sent to MySQL

    try:
        with conn:
            cursor = conn.cursor() # make a mysql cursor
            cursor.execute(query) # execute the query
            x = cursor.fetchall() # fetch results from cursor
            return x # return the results
    finally:
        cursor.close() # Close the cursor.

## DB Function to get the country by Independence year
def getCountryByInYrDB(year):
    if (not conn): # check if not connected
        connect() # then connect if not connected already
    else:
        pass

    
    query = "SELECT Name,Continent,IndepYear FROM country where IndepYear = %s" # the MySQL query

    try:
        with conn:
            cursor = conn.cursor() # make a mysql cursor
            cursor.execute(query,year) # execute the query
            x = cursor.fetchall() # fetch results from cursor
            return x # return the results
    finally:
        cursor.close() # Close the cursor.

## DB Function to add a person to the person table
def addPersonDB(name,age):
	if (not conn): # check if not connected
		connect() # then connect if not connected already
	else:
		pass

	query = "INSERT into person (personname,age) values (%s,%s)" # the MySQL query

	try:
		with conn:
			cursor = conn.cursor() # make a mysql cursor
			cursor.execute(query,(name,age)) # execute the query, passing name,age -> (%s,%s)
	except pymysql.err.IntegrityError:  # Cath Integrity Error for adding a personname that already exists
		print('*** ERROR ***: ', name, ' already exists')
	except pymysql.err.InternalError: # Catch Internal Error, not enteringt a valid integer
		print('Please add valid age, must be an integer')
	finally:
		cursor.close() # Close the cursor.

## DB Function to get country table
def getCountryDB():
    if(not conn): # check if not connected
        connect() # then connect if not connected already
    else:
        pass
    query = "SELECT * FROM country" # the MySQL query

    df = pd.read_sql(query, conn) # Pandas method to run sql and read into pandas DataFrame
    return df # return the DF

## DB Function to find student by Address
def findStudentByAddressDB(address):
	if (not myclient): # check if not connected
		try:
			mongo_connect() # Connect to Mongo
		except Exception as e:
			print('Error ', e) # print any exception
		
	mydb = myclient["proj20DB"] # Use this DB
	docs = mydb["docs"]  # define collection

	query = {"details.address": address} # set the find query
	project = {"details.address": 0} # set the find projection
	qs = docs.find(query,project) # run the query command
	for x in qs: # iterate over results
		try:
			print(x["_id"],' | ', x["details"]["name"],' | ', x["details"]["age"],' | ', x["qualifications"]) # try print with qualifications if it exists
		except KeyError:
			print(x["_id"],' | ', x["details"]["name"],' | ', x["details"]["age"]) # Otherwise catch Error and print without qualifications

## DB Function to add a new course
def addNewCourseDB(iD,name,level):
	if (not myclient): # check if not connected
		try:
			mongo_connect() # Connect to Mongo
		except Exception as e:
			print('Error ', e) # print any exception
		
	mydb = myclient["proj20DB"] # Use this DB
	docs = mydb["docs"] # define collection

	query = {"_id": iD, "name": name, "level": level} # set the query for the insert_one
	try:
		docs.insert_one(query) # try run the insert query
	except pymongo.errors.DuplicateKeyError:  # Catch the error if a duplicate exists.
		print('*** ERROR ***: _id DATA already exists') # Print an error

if __name__ == "__main__":
	# execute only if run as a script 
	main()
