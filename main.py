#Current To Do:
    #Store data in JSON
    #Manage JSON IO
    #Convert loggable info to dictionary
    #Convert dictionary to JSON
    
cmdlist = {'help': ': Why did you request this?',
        'profile': ': Loads profile with the input name',
        'add': '[course code]: adds the attached course to your course list',
        'view': '[course code]: Views current assessments attached to course',
        '': ''}

class manualCourse():
    def __init__(self,code,name,note):
        self.code = code
        self.name = name
        self.note = note
    
    def add_assignment(self):
        assignment = {}
        while True:
            try:
                assignment_type = input('''What type of assignment would you like to add? (project/workshop/multipart)
                if you don't know what the types are, enter "help"
                type: ''')
                if assignment_type in ('project','workshop','multipart'):
                    assignment.update({'type': assignment_type})
                    break
                elif assignment_type is 'help':
                    print('''project: an assignment with one due date
                    workshop: multiple assessment tasks to be completed each week
                    multipart: assignment with multiple parts that are to be submitted on different dates''')
                    continue
                else: raise Exception('IncorrectInput')
            except: print('Incorrect input, try again (tip: type is case sensitive)')
        if assignment_type is 'project':
            name = input()

        

def main():
    try:
        config = open('settings.txt', 'r')
    except: 
        firstStartup() 
        config = open('settings.txt', 'r')
    profile = open(loadProfile(config) + '.pf', 'r')
    print('Welcome ' + profile.readlines()[0])#Welcomes the loaded user
    print('Enter help for command list, or help [command] for an explanation of this command')
    
    usr_in = 0
    while usr_in != 'q':
        usr_in = input('Enter Command: ')
    print('Thank you for using my software!')

        
#On first startup, creates a config file containing the main user's profile name
#It also creates a pf file with the profile's name which will later contain courses
def firstStartup():
    config = open('settings.txt', 'w')
    user = input('Enter your name: ')
    config.write(f'Profile:{user}\n').close()
    newProfile = open(f'{user}.pf', 'w')
    newProfile.write(user).close()

def loadProfile(cfg):
    loaduser = cfg.readline().strip().split(':')[1]
    return loaduser


def add_course():
    print('Add a course to list')
    course_code = input('Enter Course Code: ')
    name = input('What is the name of the course?: ')
    note = input('Would you like to add a note/description of course? (leave empty if none)')


def REPL():
    usr_in = 0
    while usr_in != 'q':
        usr_in = input('Enter Command: ')


main()
