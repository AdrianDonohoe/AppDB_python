
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
			print(array)
			display_menu()
		elif (choice == "3"):
			find_gt_in_array(array)
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
        print(people[i+1]['personID'],'|',people[i+1]['personname'],'|',people[i+1]['age'])
        answer = input('-- Quit (q) --')
        if answer == 'q' or answer == 'Q':
            break
        

        






def display_menu():
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
        print("Already connected")

    
    query = "SELECT * FROM person"

    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        x = cursor.fetchall()
        return x
    

if __name__ == "__main__":
	# execute only if run as a script 
	main()
