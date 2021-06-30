import errorHandling as Usr_In
import json
from assignments import NewCourse, NewProject
#Current To Do:
    #Store data in JSON
    #Manage JSON IO
    #Convert loggable info to dictionary
    #Convert dictionary to JSON
dataJSON = {}
loadedCourses = []
def saveJSON():
    with open('data.json',mode='w') as outfile:
        json.dump(dataJSON, outfile, indent=4)
        return

def loadJSON():
    with open('data.json',mode='r') as infile:
        data = json.load(infile)
        global dataJSON
        dataJSON.update(data)
        return

def main():
    try:
        data = open('data.json', 'r')
        data.close()
    except: 
        with open('data.json', 'w') as outfile:
            json.dump({'user': input('Please enter your name: ')}, outfile, indent=4)
    loadJSON()
    print('\n\n\nWelcome ' + dataJSON['user'])#Welcomes the loaded user
    print('Enter help for command list, or help [command] for an explanation of this command')
    
    usr_in = 0
    while usr_in != 'q':
        usr_in = input('Enter Command: ')
    print('Thank you for using my software!')

def add_course():
    print('Add a course to list')
    course_code = input('Enter Course Code: ')
    name = input('What is the name of the course?: ')
    note = input('Would you like to add a note/description of course? (leave empty if none)')


def REPL():
    while True:
        usr_in = input('Enter Command: ')


#main()
#classtest = NewCourse()
