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



def REPL():
    usr_in = 0
    while usr_in != 'q':
        usr_in = input('Enter Command: ')


main()
