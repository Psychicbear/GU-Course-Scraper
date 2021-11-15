import errorHandling as Usr_In, json, re
from assignments import Course, Project
dataJSON = {}
loadedCourses = []
user = ''
def saveJSON():
    global dataJSON
    for i in loadedCourses:
        dataJSON.update(i.export())
    with open('data.json',mode='w') as outfile:
        json.dump(dataJSON, outfile, indent=4)
        return

def loadJSON():
    with open('data.json',mode='r') as infile:
        data = json.load(infile)
        global dataJSON, loadedCourses, user
        dataJSON.update(data)
        loadedCourses = []
        for key in dataJSON:
            if key == 'user':
                user = dataJSON[key]
                continue
            course = Course(dataJSON[key])
            loadedCourses.append(course) 

def main():
    global dataJSON, loadedCourses
    try:
        loadJSON()
    except: 
        with open('data.json', 'w') as outfile:
            json.dump({'user': input('Please enter your name: ')}, outfile, indent=4)
        loadJSON()
    print('\n\n\nWelcome ' + user)#Welcomes the loaded user
    print('Enter help for command list, or help [command] for an explanation of this command')
    
    while True:
        usr_in = input('?: ')
        split_input = usr_in.strip().split()
        if usr_in == 'save':
            saveJSON()
        elif usr_in == 'load':
            loadJSON()
        elif usr_in == 'add course':
            load = Course()
            loadedCourses.append(load)
        elif re.search('^(view) \d{4}\w{3}$', usr_in):
            course = split_input[1]
            found = False
            for i in loadedCourses:
                if i.code == course:
                    course = i
                    found = True
                    break
            if found is True:
                view_course(course)
            else: print('Course not found')
        elif usr_in == 'quit':
            break
        else: print('Invalid command')
    print('Thank you for using my software!')

def view_course(course):
    #Show total amount of assignments
    #Show completed assignments
    #Show if weekly assignment submitted
    #Show current estimated grade
    while True:
        total_assign = 0
        complete_assign = 0
        course.info()
        for i in course.assignments:
            i.info()
            total_assign += 1
            if i.submitted is True:
                complete_assign += 1
        print(f'Completed assignments: {complete_assign}/{total_assign}')
        usr_in = input('Enter command or type back to go back: ')
        if re.search('^(view) \d$', usr_in):
            index = int(''.join(usr_in[5:]))
            view_assignment(course.assignment[index])

def view_assignment(assign):
    pass

#main()
print(re.search('(\d) (\d\d)', '2 54 64 234 1 2'))