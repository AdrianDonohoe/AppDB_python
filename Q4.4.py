import pymysql
import pandas as pd
import pymongo


conn = None  # Connection variable for MySQL
myclient = None # Connection variable for Mongo
df = pd.DataFrame()

# Main function
def main():

	display_menu()

	while True:
		choice = input("Choice: ")

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
				conn.close()
			except AttributeError:
				pass
			break;
		else:
			display_menu()
			
			
def viewPeople():
    people = getPeopleDB()
    
    answer = ''
    for i in range(0,len(people),2):
        print(people[i]['personID'],'|',people[i]['personname'],'|',people[i]['age'])
        try:
            print(people[i+1]['personID'],'|',people[i+1]['personname'],'|',people[i+1]['age'])
        except:
            pass
        answer = input('-- Quit (q) --')
        if answer == 'q' or answer == 'Q':
            break
        

def getCountryByInYr():
    year = input('Enter Year : ')
    countries = getCountryByInYrDB(year)

    for country in countries:
        print(country['Name'],'|',country['Continent'],'|',country['IndepYear'])
             


def addPerson():
    print('Add New Person')
    print('-' * 14)
    name = input('Name : ')
    age = input('Age : ')
    addPersonDB(name,age)

def getCountryByName():
	global df
	if df.empty:
		df = getCountryDB()
	
	print('')
	print('Countries by Name')
	print('-' * 17)
	sub = input('Enter Country Name : ')
	df['Found'] = df['Name'].str.find(sub) # Adapted from https://www.geeksforgeeks.org/python-pandas-series-str-find/
	found = df.loc[df.loc[:,'Found'] != -1 ]
	for index, row in found.iterrows():
		print(row['Name'],' | ',row['Continent'],' | ',row['Population'],' | ',row['HeadOfState']) # The project spec doesnt specifically say what to print here, but this is what the example uses.

	
def getCountryByPop():
	global df
	if df.empty:
		df = getCountryDB()
	
	print('')
	print('Countries by Pop')
	print('-' * 16)
	operator = input('Enter < > or = : ')
	while True:  # Adapted from https://docs.python.org/3/tutorial/errors.html
		try:
			pop = int(input('Enter population : '))
			break
		except ValueError:
			print("Oops!  That was no valid number.  Try again...")
	if operator == '<':
		found = df.loc[df.loc[:,'Population'] < pop ]
		for index, row in found.iterrows():
			print(row['Code'],' | ',row['Name'],' | ', row['Continent'],' | ',row['Population'])
	elif operator == '>':
		found = df.loc[df.loc[:,'Population'] > pop ]
		for index, row in found.iterrows():
			print(row['Code'],' | ',row['Name'],' | ', row['Continent'],' | ',row['Population'])
	elif operator == '=':
		found = df.loc[df.loc[:,'Population'] == pop ]
		for index, row in found.iterrows():
			print(row['Code'],' | ',row['Name'],' | ', row['Continent'],' | ',row['Population'])
	else:
		pass

def findStudentByAddress():
	print('')
	print('Find Students by Address')
	print('-' * 24)
	address = input('Enter Address : ')
	findStudentByAddressDB(address)


def addNewCourse():
	print('')
	print('Add New Course')
	print('-' * 14)
	iD = input('_id : ')
	name = input('Name : ')
	level = input('Level : ')
	addNewCourseDB(iD,name,level)


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




def connect():
    global conn
    conn = pymysql.connect(host="localhost",user="root",password="1solari2", db="world",cursorclass=pymysql.cursors.DictCursor)
    
def mongo_connect():
    global myclient
    myclient = pymongo.MongoClient()
    myclient.admin.command('ismaster')

def getPeopleDB():
    if (not conn):
        connect()
    else:
        pass

    
    query = "SELECT * FROM person"

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query)
            x = cursor.fetchall()
            return x
    finally:
        cursor.close()

def getCountryByInYrDB(year):
    if (not conn):
        connect()
    else:
        pass

    
    query = "SELECT Name,Continent,IndepYear FROM country where IndepYear = %s"

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query,year)
            x = cursor.fetchall()
            return x
    finally:
        cursor.close()

def addPersonDB(name,age):
	if (not conn):
		connect()
	else:
		pass

	query = "INSERT into person (personname,age) values (%s,%s)"

	try:
		with conn:
			cursor = conn.cursor()
			cursor.execute(query,(name,age))
	except pymysql.err.IntegrityError:
		print('*** ERROR ***: ', name, ' already exists')
	except pymysql.err.InternalError:
		print('Please add valid age, must be an integer')
	finally:
		cursor.close()

def getCountryDB():
    if(not conn):
        connect()
    else:
        pass
    query = "SELECT * FROM country"

    df = pd.read_sql(query, conn)
    return df

def findStudentByAddressDB(address):
	if (not myclient):
		try:
			mongo_connect()
		except Exception as e:
			print('Error ', e)
		
	mydb = myclient["proj20DB"]
	docs = mydb["docs"]

	query = {"details.address": address}
	project = {"details.address": 0}
	qs = docs.find(query,project)
	for x in qs:
		try:
			print(x["_id"],' | ', x["details"]["name"],' | ', x["details"]["age"],' | ', x["qualifications"])
		except KeyError:
			print(x["_id"],' | ', x["details"]["name"],' | ', x["details"]["age"])

def addNewCourseDB(iD,name,level):
	if (not myclient):
		try:
			mongo_connect()
		except Exception as e:
			print('Error ', e)
		
	mydb = myclient["proj20DB"]
	docs = mydb["docs"]

	query = {"_id": iD, "name": name, "level": level}
	try:
		docs.insert_one(query)
	except pymongo.errors.DuplicateKeyError:
		print('*** ERROR ***: _id DATA already exists')

if __name__ == "__main__":
	# execute only if run as a script 
	main()
