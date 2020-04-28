
import pymysql


conn = None

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
		elif (choice == "x"):
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
    finally:
        cursor.close()
    

if __name__ == "__main__":
	# execute only if run as a script 
	main()
